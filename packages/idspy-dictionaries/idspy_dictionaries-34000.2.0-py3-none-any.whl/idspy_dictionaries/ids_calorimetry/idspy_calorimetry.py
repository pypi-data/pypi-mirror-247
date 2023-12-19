# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@idspy_dataclass(repr=False, slots=True)
class DataFlt0DConstantValidity(IdsBaseClass):
    """
    Constant data (FLT_0D) with validity flag.

    :ivar validity: Indicator of the validity of the data for the whole
        acquisition period. 0: valid from automated processing, 1: valid
        and certified by the diagnostic RO; - 1 means problem identified
        in the data processing (request verification by the diagnostic
        RO), -2: invalid data, should not be used (values lower than -2
        have a code-specific meaning detailing the origin of their
        invalidity)
    """
    class Meta:
        name = "data_flt_0d_constant_validity"

    validity: int = field(
        default=999999999
    )

    @idspy_dataclass(repr=False, slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_0D"
        )


@idspy_dataclass(repr=False, slots=True)
class Identifier(IdsBaseClass):
    """Standard type for identifiers (constant).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar name: Short string identifier
    :ivar index: Integer identifier (enumeration index within a list).
        Private identifier values must be indicated by a negative index.
    :ivar description: Verbose description
    """
    class Meta:
        name = "identifier"

    name: str = field(
        default=""
    )
    index: int = field(
        default=999999999
    )
    description: str = field(
        default=""
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProvenanceNode(IdsBaseClass):
    """
    Provenance information for a given node of the IDS.

    :ivar path: Path of the node within the IDS, following the syntax
        given in the link below. If empty, means the provenance
        information applies to the whole IDS.
    :ivar sources: List of sources used to import or calculate this
        node, identified as explained below. In case the node is the
        result of of a calculation / data processing, the source is an
        input to the process described in the "code" structure at the
        root of the IDS. The source can be an IDS (identified by a URI
        or a persitent identifier, see syntax in the link below) or non-
        IDS data imported directly from an non-IMAS database (identified
        by the command used to import the source, or the persistent
        identifier of the data source). Often data are obtained by a
        chain of processes, however only the last process input are
        recorded here. The full chain of provenance has then to be
        reconstructed recursively from the provenance information
        contained in the data sources.
    """
    class Meta:
        name = "ids_provenance_node"

    path: str = field(
        default=""
    )
    sources: Optional[list[str]] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class Library(IdsBaseClass):
    """
    Library used by the code that has produced this IDS.

    :ivar name: Name of software
    :ivar description: Short description of the software (type, purpose)
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    """
    class Meta:
        name = "library"

    name: str = field(
        default=""
    )
    description: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )


@idspy_dataclass(repr=False, slots=True)
class SignalFlt1DValidity(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base and validity flags.

    :ivar validity_timed: Indicator of the validity of the data for each
        time slice. 0: valid from automated processing, 1: valid and
        certified by the diagnostic RO; - 1 means problem identified in
        the data processing (request verification by the diagnostic RO),
        -2: invalid data, should not be used (values lower than -2 have
        a code-specific meaning detailing the origin of their
        invalidity)
    :ivar validity: Indicator of the validity of the data for the whole
        acquisition period. 0: valid from automated processing, 1: valid
        and certified by the diagnostic RO; - 1 means problem identified
        in the data processing (request verification by the diagnostic
        RO), -2: invalid data, should not be used (values lower than -2
        have a code-specific meaning detailing the origin of their
        invalidity)
    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d_validity"

    validity_timed: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    validity: int = field(
        default=999999999
    )
    time: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )

    @idspy_dataclass(repr=False, slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_1D"
        )


@idspy_dataclass(repr=False, slots=True)
class CalorimetryCoolingLoop(IdsBaseClass):
    """
    Cooling loop.

    :ivar name: Name of the loop
    :ivar identifier: ID of the loop
    :ivar temperature_in: Temperature of the coolant when entering the
        loop
    :ivar temperature_out: Temperature of the coolant when exiting the
        loop
    :ivar mass_flow: Mass flow of the coolant going through the loop
    """
    class Meta:
        name = "calorimetry_cooling_loop"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    temperature_in: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    temperature_out: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    mass_flow: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class CalorimetryGroupComponent(IdsBaseClass):
    """
    Component.

    :ivar name: Name of the component
    :ivar identifier: ID of the component
    :ivar power: Power extracted from the component
    :ivar energy_cumulated: Energy extracted from the component since
        the start of the pulse
    :ivar energy_total: Energy extracted from the component on the whole
        plasma discharge, including the return to thermal equilibrium of
        the component in the post-pulse phase
    :ivar temperature_in: Temperature of the coolant when entering the
        component
    :ivar temperature_out: Temperature of the coolant when exiting the
        component
    :ivar mass_flow: Mass flow of the coolant going through the
        component
    :ivar transit_time: Transit time for the coolant to go from the
        input to the output of the component
    """
    class Meta:
        name = "calorimetry_group_component"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    power: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    energy_cumulated: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    energy_total: Optional[DataFlt0DConstantValidity] = field(
        default=None
    )
    temperature_in: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    temperature_out: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    mass_flow: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    transit_time: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class Code(IdsBaseClass):
    """
    Generic decription of the code-specific parameters for the code that has
    produced this IDS.

    :ivar name: Name of software generating IDS
    :ivar description: Short description of the software (type, purpose)
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    :ivar library: List of external libraries used by the code that has
        produced this IDS
    """
    class Meta:
        name = "code"

    name: str = field(
        default=""
    )
    description: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )
    output_flag: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    library: list[Library] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProvenance(IdsBaseClass):
    """
    Provenance information about the IDS.

    :ivar node: Set of IDS nodes for which the provenance is given. The
        provenance information applies to the whole structure below the
        IDS node. For documenting provenance information for the whole
        IDS, set the size of this array of structure to 1 and leave the
        child "path" node empty
    """
    class Meta:
        name = "ids_provenance"

    node: list[IdsProvenanceNode] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class CalorimetryGroup(IdsBaseClass):
    """
    Group of components on which calorimetry measurements are carried out.

    :ivar name: Name of the group
    :ivar identifier: ID of the group
    :ivar component: Set of components on which calorimetry measurements
        are carried out
    """
    class Meta:
        name = "calorimetry_group"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    component: list[CalorimetryGroupComponent] = field(
        default_factory=list,
        metadata={
            "max_occurs": 40,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProperties(IdsBaseClass):
    """Interface Data Structure properties.

    This element identifies the node above as an IDS

    :ivar comment: Any comment describing the content of this IDS
    :ivar name: User-defined name for this IDS occurrence
    :ivar homogeneous_time: This node must be filled (with 0, 1, or 2)
        for the IDS to be valid. If 1, the time of this IDS is
        homogeneous, i.e. the time values for this IDS are stored in the
        time node just below the root of this IDS. If 0, the time values
        are stored in the various time fields at lower levels in the
        tree. In the case only constant or static nodes are filled
        within the IDS, homogeneous_time must be set to 2
    :ivar occurrence_type: Type of data contained in this occurrence
    :ivar provider: Name of the person in charge of producing this data
    :ivar creation_date: Date at which this data has been produced
    :ivar provenance: Provenance information about this IDS
    """
    class Meta:
        name = "ids_properties"

    comment: str = field(
        default=""
    )
    name: str = field(
        default=""
    )
    homogeneous_time: int = field(
        default=999999999
    )
    occurrence_type: Optional[Identifier] = field(
        default=None
    )
    provider: str = field(
        default=""
    )
    creation_date: str = field(
        default=""
    )
    provenance: Optional[IdsProvenance] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class Calorimetry(IdsBaseClass):
    """
    Calometry measurements on various tokamak subsystems.

    :ivar ids_properties:
    :ivar group: Set of groups of components on which calorimetry
        measurements are carried out (grouped by tokamak subsystems or
        localisation on the machine)
    :ivar cooling_loop: Set of cooling loops
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "calorimetry"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    group: list[CalorimetryGroup] = field(
        default_factory=list,
        metadata={
            "max_occurs": 25,
        }
    )
    cooling_loop: list[CalorimetryCoolingLoop] = field(
        default_factory=list,
        metadata={
            "max_occurs": 8,
        }
    )
    latency: float = field(
        default=9e+40
    )
    code: Optional[Code] = field(
        default=None
    )
    time: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
