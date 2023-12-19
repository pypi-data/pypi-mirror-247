# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@idspy_dataclass(repr=False, slots=True)
class CoilNaRzphi1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z, Phi positions (1D, static), with a reference to the
    types coordinate specific to this IDS.

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "coil_na_rzphi1d_static"

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
    phi: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
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
class NormalBinormalStatic(IdsBaseClass):
    """
    Structure for list of normal, binormal positions (1D, static)

    :ivar normal: Coordinate along the normal axis
    :ivar binormal: Coordinates along the binormal axis
    """
    class Meta:
        name = "normal_binormal_static"

    normal: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    binormal: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
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
class CoilConductorElements(IdsBaseClass):
    """
    Elements descibring the conductor contour.

    :ivar types: Type of every element: 1: line segment, its ends are
        given by the start and end points; index = 2: arc of a circle;
        index = 3: full circle
    :ivar start_points: Position of the start point of every element
    :ivar intermediate_points: Position of an intermediate point along
        the circle or arc of circle, for every element, providing the
        orientation of the element (must define with the corresponding
        start point an aperture angle strictly inferior to PI). In the
        case of a line segment (../types/index=1), fill this node with a
        point such that the vector intermediate_point - start_point
        defines the direction of the element's normal axis (see
        documentation of ../elements)
    :ivar end_points: Position of the end point of every element.
        Meaningful only if type/index = 1 or 2, fill with default/empty
        value otherwise
    :ivar centres: Position of the centre of the arc of a circle of
        every element (meaningful only if type/index = 2 or 3, fill with
        default/empty value otherwise)
    """
    class Meta:
        name = "coil_conductor_elements"

    types: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    start_points: Optional[CoilNaRzphi1DStatic] = field(
        default=None
    )
    intermediate_points: Optional[CoilNaRzphi1DStatic] = field(
        default=None
    )
    end_points: Optional[CoilNaRzphi1DStatic] = field(
        default=None
    )
    centres: Optional[CoilNaRzphi1DStatic] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class CoilCrossSection(IdsBaseClass):
    """
    Coil cross-section.

    :ivar geometry_type: Geometry type used to describe the cross
        section of this element. The conductor centre is given by the
        ../../elements description.
    :ivar width: Full width of the rectangle or square in the normal
        direction, when geometry_type/index = 3 or 4. Diameter of the
        circle when geometry_type/index = 2. Outer diameter of the
        annulus in case geometry_type/index = 5
    :ivar height: Full height of the rectangle in the binormal
        direction, used only if geometry_type/index = 3
    :ivar radius_inner: Inner radius of the annulus, used only if
        geometry_type/index = 5
    :ivar outline: Polygonal outline of the cross section in the
        (normal, binormal) coordinate system. Do NOT repeat the first
        point.
    :ivar area: Area of the conductor cross-section, derived from the
        above geometric data
    """
    class Meta:
        name = "coil_cross_section"

    geometry_type: Optional[IdentifierStatic] = field(
        default=None
    )
    width: float = field(
        default=9e+40
    )
    height: float = field(
        default=9e+40
    )
    radius_inner: float = field(
        default=9e+40
    )
    outline: Optional[NormalBinormalStatic] = field(
        default=None
    )
    area: float = field(
        default=9e+40
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
class CoilConductor(IdsBaseClass):
    """
    Description of a conductor.

    :ivar elements: Set of geometrical elements (line segments and/or
        arcs of a circle) describing the contour of the conductor
        centre. We define a coordinate system associated to each element
        as follows: for the arc and circle elements: binormal = (start
        point - center) x (intermediate point - center). This vector
        points in the direction of the circle / arc axis. normal =
        (center - point on curve). The normal vector will rotate as the
        point moves around the curve. Tangent = normal x binormal. For
        the line element we require an extra point, using the currently
        redundant intermediate point to define the line element's normal
        axis. The local coordinates for the line element then become:
        tangent = end point - start point; normal = intermediate point -
        start point; binormal = tangent x normal. It is assumed that all
        the axes above are normalized such that they have a unit length.
    :ivar cross_section: The cross-section perpendicular to the
        conductor contour is described by a series of contour points,
        given by their relative position with respect to the start point
        of each element. If the size of this array of structure is equal
        to 1, then the cross-section is given only for the first element
        and translated along the conductor elements. Otherwise, it's
        given explictly for each element, allowing to describe changes
        of the cross section shape
    :ivar resistance: conductor resistance
    :ivar voltage: Voltage on the conductor terminals. Sign convention :
        positive when the current flows in the direction in which
        conductor elements are ordered (from start to end for a positive
        polarity coil)
    """
    class Meta:
        name = "coil_conductor"

    elements: Optional[CoilConductorElements] = field(
        default=None
    )
    cross_section: list[CoilCrossSection] = field(
        default_factory=list,
        metadata={
            "max_occurs": 50,
        }
    )
    resistance: float = field(
        default=9e+40
    )
    voltage: Optional[SignalFlt1D] = field(
        default=None
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
class Coil(IdsBaseClass):
    """
    Description of a given coil.

    :ivar name: Name of the coil
    :ivar identifier: Alphanumeric identifier of coil
    :ivar conductor: Set of conductors inside the coil. The structure
        can be used with size 1 for a simplified description as a single
        conductor. A conductor is composed of several elements, serially
        connected, i.e. transporting the same current.
    :ivar turns: Number of total turns in the coil. May be a fraction
        when describing the coil connections.
    :ivar resistance: Coil resistance
    :ivar current: Current in one turn of the coil (to be multiplied by
        the number of turns to calculate the magnetic field generated).
        Sign convention : a positive current flows in the direction in
        which conductor elements are ordered (from start to end for a
        positive polarity coil)
    :ivar voltage: Voltage on the coil terminals. Sign convention :
        positive when the current flows in the direction in which
        conductor elements are ordered (from start to end for a positive
        polarity coil)
    """
    class Meta:
        name = "coil"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    conductor: list[CoilConductor] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    turns: float = field(
        default=9e+40
    )
    resistance: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class CoilsNonAxisymmetric(IdsBaseClass):
    """
    Non axisymmetric active coils system (e.g. ELM control coils, error field
    correction coils, ...)

    :ivar ids_properties:
    :ivar coil: Set of coils
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "coils_non_axisymmetric"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    coil: list[Coil] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
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
