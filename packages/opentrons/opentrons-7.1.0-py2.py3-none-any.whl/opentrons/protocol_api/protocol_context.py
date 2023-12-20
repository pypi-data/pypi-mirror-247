from __future__ import annotations

import logging
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Type,
    Union,
    Mapping,
    cast,
)

from opentrons_shared_data.labware.dev_types import LabwareDefinition
from opentrons_shared_data.pipette.dev_types import PipetteNameType

from opentrons.types import Mount, Location, DeckLocation, DeckSlotName, StagingSlotName
from opentrons.legacy_broker import LegacyBroker
from opentrons.hardware_control import SyncHardwareAPI
from opentrons.hardware_control.modules.types import MagneticBlockModel
from opentrons.commands import protocol_commands as cmds, types as cmd_types
from opentrons.commands.publisher import CommandPublisher, publish
from opentrons.protocols.api_support import instrument as instrument_support
from opentrons.protocols.api_support.deck_type import (
    NoTrashDefinedError,
    should_load_fixed_trash_for_python_protocol,
)
from opentrons.protocols.api_support.types import APIVersion
from opentrons.protocols.api_support.util import (
    AxisMaxSpeeds,
    requires_version,
    APIVersionError,
)

from ._types import OffDeckType
from .core.common import ModuleCore, LabwareCore, ProtocolCore
from .core.core_map import LoadedCoreMap
from .core.engine.module_core import NonConnectedModuleCore
from .core.module import (
    AbstractTemperatureModuleCore,
    AbstractMagneticModuleCore,
    AbstractThermocyclerCore,
    AbstractHeaterShakerCore,
    AbstractMagneticBlockCore,
)
from .core.engine import ENGINE_CORE_API_VERSION
from .core.legacy.legacy_protocol_core import LegacyProtocolCore

from . import validation
from ._liquid import Liquid
from ._trash_bin import TrashBin
from ._waste_chute import WasteChute
from .deck import Deck
from .instrument_context import InstrumentContext
from .labware import Labware
from .module_contexts import (
    MagneticModuleContext,
    TemperatureModuleContext,
    ThermocyclerContext,
    HeaterShakerContext,
    MagneticBlockContext,
    ModuleContext,
)


logger = logging.getLogger(__name__)


ModuleTypes = Union[
    TemperatureModuleContext,
    MagneticModuleContext,
    ThermocyclerContext,
    HeaterShakerContext,
    MagneticBlockContext,
]


class HardwareManager(NamedTuple):
    """Back. compat. wrapper for a removed class called `HardwareManager`.

    This interface will not be present in PAPIv3.
    """

    hardware: SyncHardwareAPI


class ProtocolContext(CommandPublisher):
    """The Context class is a container for the state of a protocol.

    It encapsulates many of the methods formerly found in the Robot class,
    including labware, instrument, and module loading, as well as core
    functions like pause and resume.

    Unlike the old robot class, it is designed to be ephemeral. The lifetime
    of a particular instance should be about the same as the lifetime of a
    protocol. The only exception is the one stored in
    ``.legacy_api.api.robot``, which is provided only for back
    compatibility and should be used less and less as time goes by.

    .. versionadded:: 2.0

    """

    def __init__(
        self,
        api_version: APIVersion,
        core: ProtocolCore,
        broker: Optional[LegacyBroker] = None,
        core_map: Optional[LoadedCoreMap] = None,
        deck: Optional[Deck] = None,
        bundled_data: Optional[Dict[str, bytes]] = None,
    ) -> None:
        """Build a :py:class:`.ProtocolContext`.

        :param api_version: The API version to use.
        :param core: The protocol implementation core.
        :param labware_offset_provider: Where this protocol context and its child
                                        module contexts will get labware offsets from.
        :param broker: An optional command broker to link to. If not
                      specified, a dummy one is used.
        :param bundled_data: A dict mapping filenames to the contents of data
                             files. Can be used by the protocol, since it is
                             exposed as
                             :py:attr:`.ProtocolContext.bundled_data`
        """
        super().__init__(broker)
        self._api_version = api_version
        self._core = core
        self._core_map = core_map or LoadedCoreMap()
        self._deck = deck or Deck(
            protocol_core=core, core_map=self._core_map, api_version=api_version
        )

        # With the introduction of Extension mount type, this dict initializes to include
        # the extension mount, for both ot2 & 3. While it doesn't seem like it would
        # create an issue in the current PAPI context, it would be much safer to
        # only use mounts available on the robot.
        self._instruments: Dict[Mount, Optional[InstrumentContext]] = {
            mount: None for mount in Mount
        }
        self._bundled_data: Dict[str, bytes] = bundled_data or {}

        # With the addition of Moveable Trashes and Waste Chute support, it is not necessary
        # to ensure that the list of "disposal locations", essentially the list of trashes,
        # is initialized correctly on protocols utilizing former API versions prior to 2.16
        # and also to ensure that any protocols after 2.16 intialize a Fixed Trash for OT-2
        # protocols so that no load trash bin behavior is required within the protocol itself.
        # Protocols prior to 2.16 expect the Fixed Trash to exist as a Labware object, while
        # protocols after 2.16 expect trash to exist as either a TrashBin or WasteChute object.

        self._load_fixed_trash()
        if should_load_fixed_trash_for_python_protocol(self._api_version):
            self._core.append_disposal_location(self.fixed_trash)
        elif (
            self._api_version >= APIVersion(2, 16)
            and self._core.robot_type == "OT-2 Standard"
        ):
            _fixed_trash_trashbin = TrashBin(
                location=DeckSlotName.FIXED_TRASH, addressable_area_name="fixedTrash"
            )
            self._core.append_disposal_location(_fixed_trash_trashbin)

        self._commands: List[str] = []
        self._unsubscribe_commands: Optional[Callable[[], None]] = None
        self.clear_commands()

    @property  # type: ignore
    @requires_version(2, 0)
    def api_version(self) -> APIVersion:
        """Return the API version supported by this protocol context.

        The supported API version was specified when the protocol context
        was initialized. It may be lower than the highest version supported
        by the robot software. For the highest version supported by the
        robot software, see ``protocol_api.MAX_SUPPORTED_VERSION``.
        """
        return self._api_version

    @property
    def _hw_manager(self) -> HardwareManager:
        # TODO (lc 01-05-2021) remove this once we have a more
        # user facing hardware control http api.
        logger.warning(
            "This function will be deprecated in later versions."
            "Please use with caution."
        )
        return HardwareManager(hardware=self._core.get_hardware())

    @property  # type: ignore
    @requires_version(2, 0)
    def bundled_data(self) -> Dict[str, bytes]:
        """Accessor for data files bundled with this protocol, if any.

        This is a dictionary mapping the filenames of bundled datafiles, with
        extensions but without paths (e.g. if a file is stored in the bundle as
        ``data/mydata/aspirations.csv`` it will be in the dict as
        ``'aspirations.csv'``) to the bytes contents of the files.
        """
        return self._bundled_data

    def cleanup(self) -> None:
        """Finalize and clean up the protocol context."""
        if self._unsubscribe_commands:
            self._unsubscribe_commands()
            self._unsubscribe_commands = None

    def __del__(self) -> None:
        if getattr(self, "_unsubscribe_commands", None):
            self._unsubscribe_commands()  # type: ignore

    @property  # type: ignore
    @requires_version(2, 0)
    def max_speeds(self) -> AxisMaxSpeeds:
        """Per-axis speed limits when moving this instrument.

        Changing this value changes the speed limit for each non-plunger
        axis of the robot, when moving this pipette. Note that this does
        only sets a limit on how fast movements can be; movements can
        still be slower than this. However, it is useful if you require
        the robot to move much more slowly than normal when using this
        pipette.

        This is a dictionary mapping string names of axes to float values
        limiting speeds. To change a speed, set that axis's value. To
        reset an axis's speed to default, delete the entry for that axis
        or assign it to ``None``.

        For instance,

        .. code-block:: py

            def run(protocol):
                protocol.comment(str(right.max_speeds))  # '{}' - all default
                protocol.max_speeds['A'] = 10  # limit max speed of
                                               # right pipette Z to 10mm/s
                del protocol.max_speeds['A']  # reset to default
                protocol.max_speeds['X'] = 10  # limit max speed of x to
                                               # 10 mm/s
                protocol.max_speeds['X'] = None  # reset to default

        .. caution::
            This property is not yet supported on
            :ref:`API version <v2-versioning>` 2.14 or higher.
        """
        if self._api_version >= ENGINE_CORE_API_VERSION:
            # TODO(mc, 2023-02-23): per-axis max speeds not yet supported on the engine
            # See https://opentrons.atlassian.net/browse/RCORE-373
            raise APIVersionError(
                "ProtocolContext.max_speeds is not supported at apiLevel 2.14 or higher."
                " Use a lower apiLevel or set speeds using InstrumentContext.default_speed"
                " or the per-method 'speed' argument."
            )

        return self._core.get_max_speeds()

    @requires_version(2, 0)
    def commands(self) -> List[str]:
        """Return the run log.

        This is a list of human-readable strings representing what's been done in the protocol so
        far. For example, "Aspirating 123 µL from well A1 of 96 well plate in slot 1."

        The exact format of these entries is not guaranteed. The format here may differ from other
        places that show the run log, such as the Opentrons App.
        """
        return self._commands

    @requires_version(2, 0)
    def clear_commands(self) -> None:
        self._commands.clear()
        if self._unsubscribe_commands:
            self._unsubscribe_commands()

        def on_command(message: cmd_types.CommandMessage) -> None:
            payload = message.get("payload")

            if payload is None:
                return

            text = payload.get("text")

            if text is None:
                return

            if message["$"] == "before":
                self._commands.append(text)

        self._unsubscribe_commands = self.broker.subscribe(
            cmd_types.COMMAND, on_command
        )

    @requires_version(2, 0)
    def is_simulating(self) -> bool:
        return self._core.is_simulating()

    @requires_version(2, 0)
    def load_labware_from_definition(
        self,
        labware_def: "LabwareDefinition",
        location: Union[DeckLocation, OffDeckType],
        label: Optional[str] = None,
    ) -> Labware:
        """Specify the presence of a piece of labware on the OT2 deck.

        This function loads the labware definition specified by `labware_def`
        to the location specified by `location`.

        :param labware_def: The labware definition to load
        :param location: The slot into which to load the labware,
                         such as ``1``, ``"1"``, or ``"D1"``. See :ref:`deck-slots`.
        :type location: int or str or :py:obj:`OFF_DECK`
        :param str label: An optional special name to give the labware. If
                          specified, this is the name the labware will appear
                          as in the run log and the calibration view in the
                          Opentrons app.
        """
        load_params = self._core.add_labware_definition(labware_def)

        return self.load_labware(
            load_name=load_params.load_name,
            namespace=load_params.namespace,
            version=load_params.version,
            location=location,
            label=label,
        )

    @requires_version(2, 0)
    def load_labware(
        self,
        load_name: str,
        location: Union[DeckLocation, OffDeckType],
        label: Optional[str] = None,
        namespace: Optional[str] = None,
        version: Optional[int] = None,
        adapter: Optional[str] = None,
    ) -> Labware:
        """Load a labware onto a location.

        For labware already defined by Opentrons, this is a convenient way
        to collapse the two stages of labware initialization (creating
        the labware and adding it to the protocol) into one.

        This function returns the created and initialized labware for use
        later in the protocol.

        :param str load_name: A string to use for looking up a labware definition.
            You can find the ``load_name`` for any standard labware on the Opentrons
            `Labware Library <https://labware.opentrons.com>`_.

        :param location: Either a :ref:`deck slot <deck-slots>`,
            like ``1``, ``"1"``, or ``"D1"``, or the special value :py:obj:`OFF_DECK`.

            .. versionchanged:: 2.15
                You can now specify a deck slot as a coordinate, like ``"D1"``.

        :type location: int or str or :py:obj:`OFF_DECK`

        :param str label: An optional special name to give the labware. If specified, this
            is the name the labware will appear as in the run log and the calibration
            view in the Opentrons app.

        :param str namespace: The namespace that the labware definition belongs to.
            If unspecified, will search both:

              * ``"opentrons"``, to load standard Opentrons labware definitions.
              * ``"custom_beta"``, to load custom labware definitions created with the
                `Custom Labware Creator <https://labware.opentrons.com/create>`_.

            You might need to specify an explicit ``namespace`` if you have a custom
            definition whose ``load_name`` is the same as an Opentrons standard
            definition, and you want to explicitly choose one or the other.

        :param version: The version of the labware definition. You should normally
            leave this unspecified to let the implementation choose a good default.
        :param adapter: Load name of an adapter to load the labware on top of. The adapter
            will be loaded from the same given namespace, but version will be automatically chosen.
        """
        if isinstance(location, OffDeckType) and self._api_version < APIVersion(2, 15):
            raise APIVersionError(
                "Loading a labware off-deck requires apiLevel 2.15 or higher."
            )

        load_name = validation.ensure_lowercase_name(load_name)
        load_location: Union[OffDeckType, DeckSlotName, StagingSlotName, LabwareCore]
        if adapter is not None:
            if self._api_version < APIVersion(2, 15):
                raise APIVersionError(
                    "Loading a labware on an adapter requires apiLevel 2.15 or higher."
                )
            loaded_adapter = self.load_adapter(
                load_name=adapter,
                location=location,
                namespace=namespace,
            )
            load_location = loaded_adapter._core
        elif isinstance(location, OffDeckType):
            load_location = location
        else:
            load_location = validation.ensure_and_convert_deck_slot(
                location, self._api_version, self._core.robot_type
            )

        labware_core = self._core.load_labware(
            load_name=load_name,
            location=load_location,
            label=label,
            namespace=namespace,
            version=version,
        )

        labware = Labware(
            core=labware_core,
            api_version=self._api_version,
            protocol_core=self._core,
            core_map=self._core_map,
        )
        self._core_map.add(labware_core, labware)

        return labware

    @requires_version(2, 0)
    def load_labware_by_name(
        self,
        load_name: str,
        location: DeckLocation,
        label: Optional[str] = None,
        namespace: Optional[str] = None,
        version: int = 1,
    ) -> Labware:
        """
        .. deprecated:: 2.0
            Use :py:meth:`load_labware` instead.
        """
        logger.warning("load_labware_by_name is deprecated. Use load_labware instead.")
        return self.load_labware(load_name, location, label, namespace, version)

    @requires_version(2, 15)
    def load_adapter_from_definition(
        self,
        adapter_def: "LabwareDefinition",
        location: Union[DeckLocation, OffDeckType],
    ) -> Labware:
        """Specify the presence of an adapter on the deck.

        This function loads the adapter definition specified by ``adapter_def``
        to the location specified by ``location``.

        :param adapter_def: The adapter's labware definition.
        :param location: The slot into which to load the labware,
                         such as ``1``, ``"1"``, or ``"D1"``. See :ref:`deck-slots`.
        :type location: int or str or :py:obj:`OFF_DECK`
        """
        load_params = self._core.add_labware_definition(adapter_def)

        return self.load_adapter(
            load_name=load_params.load_name,
            namespace=load_params.namespace,
            version=load_params.version,
            location=location,
        )

    @requires_version(2, 16)
    def load_trash_bin(self, location: DeckLocation) -> TrashBin:
        """Load a trash bin on the deck of a Flex.

        See :ref:`configure-trash-bin` for details.

        If you try to load a trash bin on an OT-2, the API will raise an error.

        :param location: The :ref:`deck slot <deck-slots>` where the trash bin is. The
            location can be any unoccupied slot in column 1 or 3.

            If you try to load a trash bin in column 2 or 4, the API will raise an error.
        """
        slot_name = validation.ensure_and_convert_deck_slot(
            location,
            api_version=self._api_version,
            robot_type=self._core.robot_type,
        )
        if not isinstance(slot_name, DeckSlotName):
            raise ValueError("Staging areas not permitted for trash bin.")
        addressable_area_name = validation.ensure_and_convert_trash_bin_location(
            location,
            api_version=self._api_version,
            robot_type=self._core.robot_type,
        )
        trash_bin = TrashBin(
            location=slot_name, addressable_area_name=addressable_area_name
        )
        self._core.append_disposal_location(trash_bin)
        return trash_bin

    @requires_version(2, 16)
    def load_waste_chute(
        self,
    ) -> WasteChute:
        """Load the waste chute on the deck.

        See :ref:`configure-waste-chute` for details, including the deck configuration
        variants of the waste chute.

        The deck plate adapter for the waste chute can only go in slot D3. If you try to
        load another item in slot D3 after loading the waste chute, or vice versa, the
        API will raise an error.
        """
        waste_chute = WasteChute()
        self._core.append_disposal_location(waste_chute)
        return waste_chute

    @requires_version(2, 15)
    def load_adapter(
        self,
        load_name: str,
        location: Union[DeckLocation, OffDeckType],
        namespace: Optional[str] = None,
        version: Optional[int] = None,
    ) -> Labware:
        """Load an adapter onto a location.

        For adapters already defined by Opentrons, this is a convenient way
        to collapse the two stages of adapter initialization (creating
        the adapter and adding it to the protocol) into one.

        This function returns the created and initialized adapter for use
        later in the protocol.

        :param str load_name: A string to use for looking up a labware definition for the adapter.
            You can find the ``load_name`` for any standard adapter on the Opentrons
            `Labware Library <https://labware.opentrons.com>`_.

        :param location: Either a :ref:`deck slot <deck-slots>`,
            like ``1``, ``"1"``, or ``"D1"``, or the special value :py:obj:`OFF_DECK`.

        :type location: int or str or :py:obj:`OFF_DECK`

        :param str namespace: The namespace that the labware definition belongs to.
            If unspecified, will search both:

              * ``"opentrons"``, to load standard Opentrons labware definitions.
              * ``"custom_beta"``, to load custom labware definitions created with the
                `Custom Labware Creator <https://labware.opentrons.com/create>`_.

            You might need to specify an explicit ``namespace`` if you have a custom
            definition whose ``load_name`` is the same as an Opentrons standard
            definition, and you want to explicitly choose one or the other.

        :param version: The version of the labware definition. You should normally
            leave this unspecified to let the implementation choose a good default.
        """
        load_name = validation.ensure_lowercase_name(load_name)
        load_location: Union[OffDeckType, DeckSlotName, StagingSlotName]
        if isinstance(location, OffDeckType):
            load_location = location
        else:
            load_location = validation.ensure_and_convert_deck_slot(
                location, self._api_version, self._core.robot_type
            )

        labware_core = self._core.load_adapter(
            load_name=load_name,
            location=load_location,
            namespace=namespace,
            version=version,
        )

        adapter = Labware(
            core=labware_core,
            api_version=self._api_version,
            protocol_core=self._core,
            core_map=self._core_map,
        )
        self._core_map.add(labware_core, adapter)

        return adapter

    # TODO(mm, 2023-06-07): Figure out what to do with this, now that the Flex has non-integer
    # slot names and labware can be stacked. https://opentrons.atlassian.net/browse/RLAB-354
    @property  # type: ignore
    @requires_version(2, 0)
    def loaded_labwares(self) -> Dict[int, Labware]:
        """Get the labwares that have been loaded into the protocol context.

        Slots with nothing in them will not be present in the return value.

        .. note::

            If a module is present on the deck but no labware has been loaded
            into it with ``module.load_labware()``, there will
            be no entry for that slot in this value. That means you should not
            use ``loaded_labwares`` to determine if a slot is available or not,
            only to get a list of labwares. If you want a data structure of all
            objects on the deck regardless of type, see :py:attr:`deck`.


        :returns: Dict mapping deck slot number to labware, sorted in order of
                  the locations.
        """
        labware_cores = (
            (core.get_deck_slot(), core) for core in self._core.get_labware_cores()
        )

        return {
            slot.as_int(): self._core_map.get(core)
            for slot, core in labware_cores
            if slot is not None
        }

    # TODO (spp, 2022-12-14): https://opentrons.atlassian.net/browse/RLAB-237
    @requires_version(2, 15)
    def move_labware(
        self,
        labware: Labware,
        new_location: Union[
            DeckLocation, Labware, ModuleTypes, OffDeckType, WasteChute
        ],
        use_gripper: bool = False,
        pick_up_offset: Optional[Mapping[str, float]] = None,
        drop_offset: Optional[Mapping[str, float]] = None,
    ) -> None:
        """Move a loaded labware to a new location. See :ref:`moving-labware` for more details.

        :param labware: The labware to move. It should be a labware already loaded
                        using :py:meth:`load_labware`.

        :param new_location: Where to move the labware to. This is either:

                * A deck slot like ``1``, ``"1"``, or ``"D1"``. See :ref:`deck-slots`.
                * A hardware module that's already been loaded on the deck
                  with :py:meth:`load_module`.
                * A labware or adapter that's already been loaded on the deck
                  with :py:meth:`load_labware` or :py:meth:`load_adapter`.
                * The special constant :py:obj:`OFF_DECK`.

        :param use_gripper: Whether to use the Flex Gripper for this movement.

                * If ``True``, will use the gripper to perform an automatic
                  movement. This will raise an error on an OT-2 protocol.
                * If ``False``, will pause protocol execution until the user
                  performs the movement. Protocol execution remains paused until
                  the user presses **Confirm and resume**.

        Gripper-only parameters:

        :param pick_up_offset: Optional x, y, z vector offset to use when picking up labware.
        :param drop_offset: Optional x, y, z vector offset to use when dropping off labware.

        Before moving a labware to or from a hardware module, make sure that the labware's
        current and new locations are accessible, i.e., open the Thermocycler lid or
        open the Heater-Shaker's labware latch.
        """

        if not isinstance(labware, Labware):
            raise ValueError(
                f"Expected labware of type 'Labware' but got {type(labware)}."
            )

        location: Union[
            ModuleCore,
            LabwareCore,
            WasteChute,
            OffDeckType,
            DeckSlotName,
            StagingSlotName,
        ]
        if isinstance(new_location, (Labware, ModuleContext)):
            location = new_location._core
        elif isinstance(new_location, (OffDeckType, WasteChute)):
            location = new_location
        else:
            location = validation.ensure_and_convert_deck_slot(
                new_location, self._api_version, self._core.robot_type
            )

        _pick_up_offset = (
            validation.ensure_valid_labware_offset_vector(pick_up_offset)
            if pick_up_offset
            else None
        )
        _drop_offset = (
            validation.ensure_valid_labware_offset_vector(drop_offset)
            if drop_offset
            else None
        )
        self._core.move_labware(
            labware_core=labware._core,
            new_location=location,
            use_gripper=use_gripper,
            pause_for_manual_move=True,
            pick_up_offset=_pick_up_offset,
            drop_offset=_drop_offset,
        )

    @requires_version(2, 0)
    def load_module(
        self,
        module_name: str,
        location: Optional[DeckLocation] = None,
        configuration: Optional[str] = None,
    ) -> ModuleTypes:
        """Load a module onto the deck, given its name or model.

        This is the function to call to use a module in your protocol, like
        :py:meth:`load_instrument` is the method to call to use an instrument
        in your protocol. It returns the created and initialized module
        context, which will be a different class depending on the kind of
        module loaded.

        A map of deck positions to loaded modules can be accessed later
        by using :py:attr:`loaded_modules`.

        :param str module_name: The name or model of the module.
            See :ref:`available_modules` for possible values.

        :param location: The location of the module.

            This is usually the name or number of the slot on the deck where you
            will be placing the module, like ``1``, ``"1"``, or ``"D1"``. See :ref:`deck-slots`.

            The Thermocycler is only valid in one deck location.
            You don't have to specify a location when loading it, but if you do,
            it must be ``7``, ``"7"``, or ``"B1"``. See :ref:`thermocycler-module`.

            .. versionchanged:: 2.15
                You can now specify a deck slot as a coordinate, like ``"D1"``.

        :param configuration: Configure a thermocycler to be in the ``semi`` position.
            This parameter does not work. Do not use it.

            .. versionchanged:: 2.14
                This parameter dangerously modified the protocol's geometry system,
                and it didn't function properly, so it was removed.

        :type location: str or int or None
        :returns: The loaded and initialized module---a
                  :py:class:`HeaterShakerContext`,
                  :py:class:`MagneticBlockContext`,
                  :py:class:`MagneticModuleContext`,
                  :py:class:`TemperatureModuleContext`, or
                  :py:class:`ThermocyclerContext`,
                  depending on what you requested with ``module_name``.

                  .. versionchanged:: 2.13
                    Added ``HeaterShakerContext`` return value.

                  .. versionchanged:: 2.15
                    Added ``MagneticBlockContext`` return value.
        """
        if configuration:
            if self._api_version < APIVersion(2, 4):
                raise APIVersionError(
                    f"You have specified API {self._api_version}, but you are"
                    "using Thermocycler parameters only available in 2.4"
                )
            if self._api_version >= ENGINE_CORE_API_VERSION:
                raise APIVersionError(
                    "The configuration parameter of load_module has been removed."
                )

        requested_model = validation.ensure_module_model(module_name)
        if isinstance(
            requested_model, MagneticBlockModel
        ) and self._api_version < APIVersion(2, 15):
            raise APIVersionError(
                f"Module of type {module_name} is only available in versions 2.15 and above."
            )

        deck_slot = (
            None
            if location is None
            else validation.ensure_and_convert_deck_slot(
                location, self._api_version, self._core.robot_type
            )
        )
        if isinstance(deck_slot, StagingSlotName):
            raise ValueError("Cannot load a module onto a staging slot.")

        module_core = self._core.load_module(
            model=requested_model,
            deck_slot=deck_slot,
            configuration=configuration,
        )

        module_context = _create_module_context(
            module_core=module_core,
            protocol_core=self._core,
            core_map=self._core_map,
            broker=self._broker,
            api_version=self._api_version,
        )

        self._core_map.add(module_core, module_context)

        return module_context

    # TODO(mm, 2023-06-07): Figure out what to do with this, now that the Flex has non-integer
    # slot names and labware can be stacked. https://opentrons.atlassian.net/browse/RLAB-354
    @property  # type: ignore
    @requires_version(2, 0)
    def loaded_modules(self) -> Dict[int, ModuleTypes]:
        """Get the modules loaded into the protocol context.

        This is a map of deck positions to modules loaded by previous calls
        to :py:meth:`load_module`. It is not necessarily the same as the
        modules attached to the robot - for instance, if the robot has a
        Magnetic Module and a Temperature Module attached, but the protocol
        has only loaded the Temperature Module with :py:meth:`load_module`,
        only the Temperature Module will be present.

        :returns Dict[int, ModuleContext]: Dict mapping slot name to module
                                           contexts. The elements may not be
                                           ordered by slot number.
        """
        return {
            core.get_deck_slot().as_int(): self._core_map.get(core)
            for core in self._core.get_module_cores()
        }

    @requires_version(2, 0)
    def load_instrument(
        self,
        instrument_name: str,
        mount: Union[Mount, str, None] = None,
        tip_racks: Optional[List[Labware]] = None,
        replace: bool = False,
    ) -> InstrumentContext:
        """Load a specific instrument required by the protocol.

        This value will actually be checked when the protocol runs, to
        ensure that the correct instrument is attached in the specified
        location.

        :param str instrument_name: Which instrument you want to load. See :ref:`new-pipette-models`
                                    for the valid values.
        :param mount: The mount where this instrument should be attached.
                      This can either be an instance of the enum type
                      :py:class:`.types.Mount` or one of the strings ``"left"``
                      or ``"right"``. If you're loading a Flex 96-Channel Pipette
                      (``instrument_name="flex_96channel_1000"``), you can leave this unspecified,
                      since it always occupies both mounts; if you do specify a value, it will be
                      ignored.
        :type mount: types.Mount or str or ``None``
        :param tip_racks: A list of tip racks from which to pick tips if
                          :py:meth:`.InstrumentContext.pick_up_tip` is called
                          without arguments.
        :type tip_racks: List[:py:class:`.Labware`]
        :param bool replace: Indicate that the currently-loaded instrument in
                             `mount` (if such an instrument exists) should be
                             replaced by `instrument_name`.
        """
        instrument_name = validation.ensure_lowercase_name(instrument_name)
        checked_instrument_name = validation.ensure_pipette_name(instrument_name)
        checked_mount = validation.ensure_mount_for_pipette(
            mount, checked_instrument_name
        )

        is_96_channel = checked_instrument_name == PipetteNameType.P1000_96

        tip_racks = tip_racks or []

        # TODO (tz, 9-12-23): move validation into PE
        on_right_mount = self._instruments[Mount.RIGHT]
        if is_96_channel and on_right_mount is not None:
            raise RuntimeError(
                f"Instrument already present on right:"
                f" {on_right_mount.name}. In order to load a 96 channel pipette both mounts need to be available."
            )

        existing_instrument = self._instruments[checked_mount]
        if existing_instrument is not None and not replace:
            # TODO(mc, 2022-08-25): create specific exception type
            raise RuntimeError(
                f"Instrument already present on {checked_mount.name.lower()}:"
                f" {existing_instrument.name}"
            )

        logger.info(
            f"Loading {checked_instrument_name} on {checked_mount.name.lower()} mount"
        )

        instrument_core = self._core.load_instrument(
            instrument_name=checked_instrument_name,
            mount=checked_mount,
        )

        for tip_rack in tip_racks:
            instrument_support.validate_tiprack(
                instrument_name=instrument_core.get_pipette_name(),
                tip_rack=tip_rack,
                log=logger,
            )

        trash: Optional[Union[Labware, TrashBin]]
        try:
            trash = self.fixed_trash
        except (NoTrashDefinedError, APIVersionError):
            trash = None

        instrument = InstrumentContext(
            core=instrument_core,
            protocol_core=self._core,
            broker=self._broker,
            api_version=self._api_version,
            tip_racks=tip_racks,
            trash=trash,
            requested_as=instrument_name,
        )

        self._instruments[checked_mount] = instrument

        return instrument

    @property  # type: ignore
    @requires_version(2, 0)
    def loaded_instruments(self) -> Dict[str, InstrumentContext]:
        """Get the instruments that have been loaded into the protocol.

        This is a map of mount name to instruments previously loaded with
        :py:meth:`load_instrument`. It is not necessarily the same as the
        instruments attached to the robot - for instance, if the robot has
        an instrument in both mounts but your protocol has only loaded one
        of them with :py:meth:`load_instrument`, the unused one will not
        be present.

        :returns: A dict mapping mount name
                  (``'left'`` or ``'right'``)
                  to the instrument in that mount.
                  If a mount has no loaded instrument,
                  that key will be missing from the dict.
        """
        return {
            mount.name.lower(): instr
            for mount, instr in self._instruments.items()
            if instr
        }

    @publish(command=cmds.pause)
    @requires_version(2, 0)
    def pause(self, msg: Optional[str] = None) -> None:
        """Pause execution of the protocol until it's resumed.

        A human can resume the protocol through the Opentrons App.

        This function returns immediately, but the next function call that
        is blocked by a paused robot (anything that involves moving) will
        not return until the protocol is resumed.

        :param str msg: An optional message to show to connected clients. The
            Opentrons App will show this in the run log.
        """
        self._core.pause(msg=msg)

    @publish(command=cmds.resume)
    @requires_version(2, 0)
    def resume(self) -> None:
        """Resume the protocol after :py:meth:`pause`.

        .. deprecated:: 2.12
           The Python Protocol API supports no safe way for a protocol to resume itself.
           See https://github.com/Opentrons/opentrons/issues/8209.
           If you're looking for a way for your protocol to resume automatically
           after a period of time, use :py:meth:`delay`.
        """
        if self._api_version >= ENGINE_CORE_API_VERSION:
            raise APIVersionError(
                "A Python Protocol cannot safely resume itself after a pause."
                " To wait automatically for a period of time, use ProtocolContext.delay()."
            )

        # TODO(mc, 2023-02-13): this assert should be enough for mypy
        # investigate if upgrading mypy allows the `cast` to be removed
        assert isinstance(self._core, LegacyProtocolCore)
        cast(LegacyProtocolCore, self._core).resume()

    @publish(command=cmds.comment)
    @requires_version(2, 0)
    def comment(self, msg: str) -> None:
        """
        Add a user-readable comment string that will be echoed to the Opentrons
        app.

        The value of the message is computed during protocol simulation,
        so cannot be used to communicate real-time information from the robot's
        actual run.
        """
        self._core.comment(msg=msg)

    @publish(command=cmds.delay)
    @requires_version(2, 0)
    def delay(
        self,
        seconds: float = 0,
        minutes: float = 0,
        msg: Optional[str] = None,
    ) -> None:
        """Delay protocol execution for a specific amount of time.

        :param float seconds: A time to delay in seconds
        :param float minutes: A time to delay in minutes

        If both `seconds` and `minutes` are specified, they will be added.
        """
        delay_time = seconds + minutes * 60
        self._core.delay(seconds=delay_time, msg=msg)

    @requires_version(2, 0)
    def home(self) -> None:
        """Homes the robot."""
        self._core.home()

    @property
    def location_cache(self) -> Optional[Location]:
        """The cache used by the robot to determine where it last was."""
        return self._core.get_last_location()

    @location_cache.setter
    def location_cache(self, loc: Optional[Location]) -> None:
        self._core.set_last_location(loc)

    @property  # type: ignore
    @requires_version(2, 0)
    def deck(self) -> Deck:
        """An interface to provide information about what's currently loaded on the deck.
        This object is useful for determining if a slot in the deck is free.

        This object behaves like a dictionary whose keys are the deck slot names.
        For instance, ``protocol.deck[1]``, ``protocol.deck["1"]``, and ``protocol.deck["D1"]``
        will all return the object loaded in the front-left slot. (See :ref:`deck-slots`.)

        The value will be a :py:obj:`~opentrons.protocol_api.Labware` if the slot contains a
        labware, a :py:obj:`~opentrons.protocol_api.ModuleContext` if the slot contains a hardware
        module, or ``None`` if the slot doesn't contain anything.

        Rather than filtering the objects in the deck map yourself,
        you can also use :py:attr:`loaded_labwares` to get a dict of labwares
        and :py:attr:`loaded_modules` to get a dict of modules.

        For :ref:`advanced-control` *only*, you can delete an element of the ``deck`` dict.
        This only works for deck slots that contain labware objects. For example, if slot
        1 contains a labware, ``del protocol.deck['1']`` will free the slot so you can
        load another labware there.

        .. warning::
            Deleting labware from a deck slot does not pause the protocol. Subsequent
            commands continue immediately. If you need to physically move the labware to
            reflect the new deck state, add a :py:meth:`.pause` or use
            :py:meth:`.move_labware` instead.

        .. versionchanged:: 2.15
           ``del`` sets the corresponding labware's location to ``OFF_DECK``.
        """
        return self._deck

    @property  # type: ignore
    @requires_version(2, 0)
    def fixed_trash(self) -> Union[Labware, TrashBin]:
        """The trash fixed to slot 12 of an OT-2's deck.

        In API version 2.15 and earlier, the fixed trash is a :py:class:`.Labware` object with one well. Access it like labware in your protocol. For example, ``protocol.fixed_trash['A1']``.

        In API version 2.15 only, Flex protocols have a fixed trash in slot A3.

        In API version 2.16 and later, the fixed trash only exists in OT-2 protocols. It is a :py:class:`.TrashBin` object, which doesn't have any wells. Trying to access ``fixed_trash`` in a Flex protocol will raise an error. See :ref:`configure-trash-bin` for details on using the movable trash in Flex protocols.

        .. versionchanged:: 2.16
            Returns a :py:class:`.TrashBin` object.
        """
        if self._api_version >= APIVersion(2, 16):
            if self._core.robot_type == "OT-3 Standard":
                raise APIVersionError(
                    "Fixed Trash is not supported on Flex protocols in API Version 2.16 and above."
                )
            disposal_locations = self._core.get_disposal_locations()
            if len(disposal_locations) == 0:
                raise NoTrashDefinedError(
                    "No trash container has been defined in this protocol."
                )
            if isinstance(disposal_locations[0], TrashBin):
                return disposal_locations[0]

        fixed_trash = self._core_map.get(self._core.fixed_trash)
        if fixed_trash is None:
            raise NoTrashDefinedError(
                "No trash container has been defined in this protocol."
            )

        return fixed_trash

    def _load_fixed_trash(self) -> None:
        fixed_trash_core = self._core.fixed_trash
        if fixed_trash_core is not None:
            fixed_trash = Labware(
                core=fixed_trash_core,
                api_version=self._api_version,
                protocol_core=self._core,
                core_map=self._core_map,
            )
            self._core_map.add(fixed_trash_core, fixed_trash)

    @requires_version(2, 5)
    def set_rail_lights(self, on: bool) -> None:
        """
        Controls the robot rail lights

        :param bool on: If true, turn on rail lights; otherwise, turn off.
        """
        self._core.set_rail_lights(on=on)

    @requires_version(2, 14)
    def define_liquid(
        self, name: str, description: Optional[str], display_color: Optional[str]
    ) -> Liquid:
        """
        Define a liquid within a protocol.

        :param str name: A human-readable name for the liquid.
        :param str description: An optional description of the liquid.
        :param str display_color: An optional hex color code, with hash included, to represent the specified liquid. Standard three-value, four-value, six-value, and eight-value syntax are all acceptable.

        :return: A :py:class:`~opentrons.protocol_api.Liquid` object representing the specified liquid.
        """
        return self._core.define_liquid(
            name=name,
            description=description,
            display_color=display_color,
        )

    @property  # type: ignore
    @requires_version(2, 5)
    def rail_lights_on(self) -> bool:
        """Returns True if the rail lights are on"""
        return self._core.get_rail_lights_on()

    @property  # type: ignore
    @requires_version(2, 5)
    def door_closed(self) -> bool:
        """Returns True if the robot door is closed"""
        return self._core.door_closed()


def _create_module_context(
    module_core: Union[ModuleCore, NonConnectedModuleCore],
    protocol_core: ProtocolCore,
    core_map: LoadedCoreMap,
    api_version: APIVersion,
    broker: LegacyBroker,
) -> ModuleTypes:
    module_cls: Optional[Type[ModuleTypes]] = None
    if isinstance(module_core, AbstractTemperatureModuleCore):
        module_cls = TemperatureModuleContext
    elif isinstance(module_core, AbstractMagneticModuleCore):
        module_cls = MagneticModuleContext
    elif isinstance(module_core, AbstractThermocyclerCore):
        module_cls = ThermocyclerContext
    elif isinstance(module_core, AbstractHeaterShakerCore):
        module_cls = HeaterShakerContext
    elif isinstance(module_core, AbstractMagneticBlockCore):
        module_cls = MagneticBlockContext
    else:
        assert False, "Unsupported module type"

    return module_cls(
        core=module_core,
        protocol_core=protocol_core,
        core_map=core_map,
        api_version=api_version,
        broker=broker,
    )
