# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class IdentifierStatic(IdsBaseClass):
    """Standard type for identifiers (static).

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
        name = "identifier_static"

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
class Rz1DStaticClosedFlag(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant) and closed flag.

    :ivar r: Major radius
    :ivar z: Height
    :ivar closed: Flag identifying whether the contour is closed (1) or
        open (0)
    """
    class Meta:
        name = "rz1d_static_closed_flag"

    r: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    z: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    closed: int = field(
        default=999999999
    )


@idspy_dataclass(repr=False, slots=True)
class SignalFlt1D(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d"

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
class Vessel2DAnnular(IdsBaseClass):
    """
    2D vessel annular description.

    :ivar outline_inner: Inner vessel outline. Do NOT repeat the first
        point for closed contours
    :ivar outline_outer: Outer vessel outline. Do NOT repeat the first
        point for closed contours
    :ivar centreline: Centreline, i.e. middle of the vessel layer as a
        series of point. Do NOT repeat the first point for closed
        contours
    :ivar thickness: Thickness of the vessel layer  in the perpendicular
        direction to the centreline. Thickness(i) is the thickness of
        the layer between centreline/r(i),z(i) and
        centreline/r(i+1),z(i+1)
    :ivar resistivity: Resistivity of the vessel unit
    """
    class Meta:
        name = "vessel_2d_annular"

    outline_inner: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    outline_outer: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    centreline: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    thickness: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    resistivity: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Vessel2DElement(IdsBaseClass):
    """
    2D vessel block element description.

    :ivar name: Name of the block element
    :ivar outline: Outline of the block element. Do NOT repeat the first
        point for closed contours
    :ivar resistivity: Resistivity of the block element
    :ivar j_tor: Toroidal current induced in this block element
    :ivar resistance: Resistance of the block element
    """
    class Meta:
        name = "vessel_2d_element"

    name: str = field(
        default=""
    )
    outline: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    resistivity: float = field(
        default=9e+40
    )
    j_tor: Optional[SignalFlt1D] = field(
        default=None
    )
    resistance: float = field(
        default=9e+40
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
class Vessel2DUnit(IdsBaseClass):
    """
    2D vessel unit description.

    :ivar name: Name of the unit
    :ivar identifier: Identifier of the unit
    :ivar annular: Annular representation of a layer by two contours,
        inner and outer. Alternatively, the layer can be described by a
        centreline and thickness.
    :ivar element: Set of block elements
    """
    class Meta:
        name = "vessel_2d_unit"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    annular: Optional[Vessel2DAnnular] = field(
        default=None
    )
    element: list[Vessel2DElement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 38,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Vessel2D(IdsBaseClass):
    """
    2D vessel description.

    :ivar type_value: Type of the description. index = 0 for the
        official single/multiple annular representation and 1 for the
        official block element representation for each unit. Additional
        representations needed on a code-by-code basis follow same
        incremental pair tagging starting on index=2
    :ivar unit: Set of units
    """
    class Meta:
        name = "vessel_2d"

    type_value: Optional[IdentifierStatic] = field(
        default=None
    )
    unit: list[Vessel2DUnit] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Cryostat2D(IdsBaseClass):
    """
    2D cryostat description.

    :ivar cryostat: Mechanical structure of the cryostat. It is
        described as a set of nested layers with given physics
        properties; Two representations are admitted for each vessel
        unit : annular (two contours) or block elements.
    :ivar thermal_shield: Mechanical structure of the cryostat thermal
        shield. It is described as a set of nested layers with given
        physics properties; Two representations are admitted for each
        vessel unit : annular (two contours) or block elements.
    """
    class Meta:
        name = "cryostat_2d"

    cryostat: Optional[Vessel2D] = field(
        default=None
    )
    thermal_shield: Optional[Vessel2D] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class Cryostat(IdsBaseClass):
    """
    Description of the cryostat surrounding the machine (if any)

    :ivar ids_properties:
    :ivar description_2d: Set of 2D cryostat descriptions, for each type
        of possible physics or engineering configurations necessary
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "cryostat"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    description_2d: list[Cryostat2D] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
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
