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
class Rz1DDynamicAos(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
    3 array of structures (index on time))

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_dynamic_aos"

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


@idspy_dataclass(repr=False, slots=True)
class Rzphi1DDynamicAos3(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (1D, dynamic within a type 3 array of
    structure)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi1d_dynamic_aos3"

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
class BFieldNaFieldMap(IdsBaseClass):
    """
    Description of the non axisymmetric b-field on a 3D grid.

    :ivar grid: 3D grid
    :ivar b_field_r: R component of the vacuum error magnetic field
    :ivar b_field_z: Z component of the vacuum error magnetic field
    :ivar b_field_tor: Toroidal component of the vacuum error magnetic
        field
    :ivar ripple_amplitude: Value of (b_field_max-
        b_field_min)/(b_field_max+b_field_min), where b_field_max resp.
        b_field_min) is the maximum (resp. minimum) of the magnetic
        field amplitude over a 2pi rotation in toroidal angle phi at a
        given R, Z position.
    """
    class Meta:
        name = "b_field_na_field_map"

    grid: Optional[Rzphi1DDynamicAos3] = field(
        default=None
    )
    b_field_r: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_z: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_tor: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    ripple_amplitude: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class BFieldNaSurface(IdsBaseClass):
    """
    Fourier decompositions of the normal components of the B-field for a given
    control surface.

    :ivar outline: Set of points defining the surface in a poloidal
        plane. The surface then extends in the toroidal direction in an
        axisymmetric way
    :ivar normal_vector: Components of the normal vector to the surface,
        given on each point of the surface
    :ivar phi: Toroidal angle array, on which the Fourier decomposition
        is carried out
    :ivar n_tor: Toroidal mode number
    :ivar b_field_r: R component of the vacuum error magnetic field on
        the various surface points
    :ivar b_field_z: Z component of the vacuum error magnetic field on
        the various surface points
    :ivar b_field_tor: Toroidal component of the vacuum error magnetic
        field on the various surface points
    :ivar b_field_normal: Normal component of the vacuum error magnetic
        field on the various surface points
    :ivar b_field_normal_fourier: Fourier coefficients of the normal
        component of the vacuum error magnetic field on the various
        surface points
    """
    class Meta:
        name = "b_field_na_surface"

    outline: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    normal_vector: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    phi: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    n_tor: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_r: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_z: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_tor: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_normal: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_normal_fourier: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
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
class BFieldNaTimeSlice(IdsBaseClass):
    """
    Time slice for the description of the 3D vaccum non-axisymmetric magnetic
    field.

    :ivar field_map: Description of the error field map
    :ivar control_surface: Magnetic field components and Fourier
        decomposition of the normal components of the magnetic field for
        a set of given control surfaces
    :ivar time: Time
    """
    class Meta:
        name = "b_field_na_time_slice"

    field_map: Optional[BFieldNaFieldMap] = field(
        default=None
    )
    control_surface: list[BFieldNaSurface] = field(
        default_factory=list
    )
    time: Optional[float] = field(
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
class BFieldNonAxisymmetric(IdsBaseClass):
    """
    Vacuum 3d error magnetic field (the full 3d magnetic field with the
    axisymmetric components subtracted)

    :ivar ids_properties:
    :ivar configuration: In case of a constant (single time slice)
        b_field description, name of the corresponding
        scenario/configuration
    :ivar control_surface_names: List of control surface names, refers
        to the ../time_slice/control_surface index
    :ivar time_slice: Set of time slices
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "b_field_non_axisymmetric"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    configuration: str = field(
        default=""
    )
    control_surface_names: Optional[list[str]] = field(
        default=None
    )
    time_slice: list[BFieldNaTimeSlice] = field(
        default_factory=list
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
