# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantGridSubsetElementObject(IdsBaseClass):
    """
    Generic grid, object part of an element part of a grid_subset (constant)

    :ivar space: Index of the space from which that object is taken
    :ivar dimension: Dimension of the object
    :ivar index: Object index
    """
    class Meta:
        name = "generic_grid_constant_grid_subset_element_object"

    space: int = field(
        default=999999999
    )
    dimension: int = field(
        default=999999999
    )
    index: int = field(
        default=999999999
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantGridSubsetMetric(IdsBaseClass):
    """
    Generic grid, metric description for a given grid_subset and base (constant)

    :ivar jacobian: Metric Jacobian
    :ivar tensor_covariant: Covariant metric tensor, given on each
        element of the subgrid (first dimension)
    :ivar tensor_contravariant: Contravariant metric tensor, given on
        each element of the subgrid (first dimension)
    """
    class Meta:
        name = "generic_grid_constant_grid_subset_metric"

    jacobian: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    tensor_covariant: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    tensor_contravariant: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantSpaceDimensionObjectBoundary(IdsBaseClass):
    """
    Generic grid, description of an object boundary and its neighbours (constant)

    :ivar index: Index of this (n-1)-dimensional boundary object
    :ivar neighbours: List of indices of the n-dimensional objects
        adjacent to the given n-dimensional object. An object may have
        multiple neighbours on a boundary
    """
    class Meta:
        name = "generic_grid_constant_space_dimension_object_boundary"

    index: int = field(
        default=999999999
    )
    neighbours: ndarray[(int,), int] = field(
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
class EmCouplingMatrix(IdsBaseClass):
    """
    User-defined coupling matrix.

    :ivar name: Name of this coupling matrix
    :ivar quantity: Physical quantity obtained following the matrix
        multiplication of the data node with the vector constructed from
        references contained in the columns_uri node
    :ivar rows_uri: List of URIs corresponding to the rows (1st
        dimension) of the coupling matrix. If not all indices of a given
        node are used, they must be listed explicitly e.g. rows_uri(i) =
        pf_active:1/coil(i) will refer to a list of indices of the
        occurrence 1 of the pf_active IDS of this data entry. If the
        rows correspond to all indices of a given vector, it is
        sufficient to give a insgle uri, the one  of the vector with the
        impliicit notation (:), e.g. rows_uri(1) =
        /grid_ggd(3)/grid_subset(2)/elements(:).
    :ivar columns_uri: List of URIs corresponding to the columns (2nd
        dimension) of the coupling matrix. See examples above (rows_uri)
    """
    class Meta:
        name = "em_coupling_matrix"

    name: str = field(
        default=""
    )
    quantity: Optional[IdentifierStatic] = field(
        default=None
    )
    rows_uri: Optional[list[str]] = field(
        default=None
    )
    columns_uri: Optional[list[str]] = field(
        default=None
    )

    @idspy_dataclass(repr=False, slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_2D"
        )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantGridSubsetElement(IdsBaseClass):
    """
    Generic grid, element part of a grid_subset (constant)

    :ivar object_value: Set of objects defining the element
    """
    class Meta:
        name = "generic_grid_constant_grid_subset_element"

    object_value: list[GenericGridConstantGridSubsetElementObject] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantSpaceDimensionObject(IdsBaseClass):
    """
    Generic grid, list of objects of a given dimension within a space (constant)

    :ivar boundary: Set of (n-1)-dimensional objects defining the
        boundary of this n-dimensional object
    :ivar geometry: Geometry data associated with the object. Its
        detailed content is defined by ../../geometry_content. Its
        dimension depends on the type of object, geometry and coordinate
        considered.
    :ivar nodes: List of nodes forming this object (indices to
        objects_per_dimension(1)%object(:) in Fortran notation)
    :ivar measure: Measure of the space object, i.e. physical size
        (length for 1d, area for 2d, volume for 3d objects,...)
    :ivar geometry_2d: 2D geometry data associated with the object. Its
        dimension depends on the type of object, geometry and coordinate
        considered. Typically, the first dimension represents the object
        coordinates, while the second dimension would represent the
        values of the various degrees of freedom of the finite element
        attached to the object.
    """
    class Meta:
        name = "generic_grid_constant_space_dimension_object"

    boundary: list[GenericGridConstantSpaceDimensionObjectBoundary] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    geometry: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    nodes: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    measure: float = field(
        default=9e+40
    )
    geometry_2d: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
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
class GenericGridConstantGridSubset(IdsBaseClass):
    """
    Generic grid grid_subset (constant)

    :ivar identifier: Grid subset identifier
    :ivar dimension: Space dimension of the grid subset elements. This
        must be equal to the sum of the dimensions of the individual
        objects forming the element.
    :ivar element: Set of elements defining the grid subset. An element
        is defined by a combination of objects from potentially all
        spaces
    :ivar base: Set of bases for the grid subset. For each base, the
        structure describes the projection of the base vectors on the
        canonical frame of the grid.
    :ivar metric: Metric of the canonical frame onto Cartesian
        coordinates
    """
    class Meta:
        name = "generic_grid_constant_grid_subset"

    identifier: Optional[Identifier] = field(
        default=None
    )
    dimension: int = field(
        default=999999999
    )
    element: list[GenericGridConstantGridSubsetElement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )
    base: list[GenericGridConstantGridSubsetMetric] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    metric: Optional[GenericGridConstantGridSubsetMetric] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstantSpaceDimension(IdsBaseClass):
    """
    Generic grid, list of dimensions within a space (constant)

    :ivar object_value: Set of objects for a given dimension
    :ivar geometry_content: Content of the ../object/geometry node for
        this dimension
    """
    class Meta:
        name = "generic_grid_constant_space_dimension"

    object_value: list[GenericGridConstantSpaceDimensionObject] = field(
        default_factory=list,
        metadata={
            "max_occurs": 300,
        }
    )
    geometry_content: Optional[Identifier] = field(
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
class GenericGridConstantSpace(IdsBaseClass):
    """
    Generic grid space (constant)

    :ivar identifier: Space identifier
    :ivar geometry_type: Type of space geometry (0: standard, 1:Fourier,
        &gt;1: Fourier with periodicity)
    :ivar coordinates_type: Type of coordinates describing the physical
        space, for every coordinate of the space. The size of this node
        therefore defines the dimension of the space. The meaning of
        these predefined integer constants can be found in the Data
        Dictionary under utilities/coordinate_identifier.xml
    :ivar objects_per_dimension: Definition of the space objects for
        every dimension (from one to the dimension of the highest-
        dimensional objects). The index correspond to 1=nodes, 2=edges,
        3=faces, 4=cells/volumes, .... For every index, a collection of
        objects of that dimension is described.
    """
    class Meta:
        name = "generic_grid_constant_space"

    identifier: Optional[Identifier] = field(
        default=None
    )
    geometry_type: Optional[Identifier] = field(
        default=None
    )
    coordinates_type: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    objects_per_dimension: list[GenericGridConstantSpaceDimension] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridConstant(IdsBaseClass):
    """
    Generic grid (constant)

    :ivar identifier: Grid identifier
    :ivar path: Path of the grid, including the IDS name, in case of
        implicit reference to a grid_ggd node described in another IDS.
        To be filled only if the grid is not described explicitly in
        this grid_ggd structure. Example syntax:
        IDS::wall/0/description_ggd(1)/grid_ggd, means that the grid is
        located in the wall IDS, occurrence 0, with relative path
        description_ggd(1)/grid_ggd, using Fortran index convention
        (here : first index of the array)
    :ivar space: Set of grid spaces
    :ivar grid_subset: Grid subsets
    """
    class Meta:
        name = "generic_grid_constant"

    identifier: Optional[Identifier] = field(
        default=None
    )
    path: str = field(
        default=""
    )
    space: list[GenericGridConstantSpace] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    grid_subset: list[GenericGridConstantGridSubset] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class EmCoupling(IdsBaseClass):
    """
    Description of the axisymmetric mutual electromagnetics; does not include non-
    axisymmetric coil systems; the convention is Quantity_Sensor_Source.

    :ivar ids_properties:
    :ivar coupling_matrix: Set of user-defined coupling matrices,
        complementary to the other system-based coupling matrices of
        this IDS
    :ivar grid_ggd: Set of grids for use in the coupling_matrix array of
        structure, described using the GGD
    :ivar mutual_active_active: Mutual inductance coupling from active
        coils to active coils
    :ivar mutual_passive_active: Mutual inductance coupling from active
        coils to passive loops
    :ivar mutual_loops_active: Mutual inductance coupling from active
        coils to flux loops
    :ivar b_field_pol_probes_active: Poloidal field coupling from active
        coils to poloidal field probes
    :ivar mutual_passive_passive: Mutual inductance coupling from
        passive loops to passive loops
    :ivar mutual_loops_passive: Mutual inductance coupling from passive
        loops to flux loops
    :ivar b_field_pol_probes_passive: Poloidal field coupling from
        passive loops to poloidal field probes
    :ivar mutual_plasma_plasma: Mutual inductance coupling from plasma
        elements to plasma elements
    :ivar mutual_plasma_active: Mutual inductance coupling from active
        coils to plasma elements
    :ivar mutual_plasma_passive: Mutual inductance coupling from passive
        loops to plasma elements
    :ivar b_field_pol_probes_plasma: Poloidal field coupling from plasma
        elements to poloidal field probes
    :ivar mutual_loops_plasma: Mutual inductance from plasma elements to
        poloidal flux loops
    :ivar active_coils: List of URIs of the active coils considered in
        the IDS
    :ivar passive_loops: List of URIs of the passive loops considered in
        the IDS
    :ivar b_field_pol_probes: List of URIs of the poloidal field probes
        considered in the IDS
    :ivar flux_loops: List of URIs of the flux loops considered in the
        IDS
    :ivar plasma_elements: List of URIs of the plasma elements
        considered in the IDS
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "em_coupling"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    coupling_matrix: list[EmCouplingMatrix] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    grid_ggd: list[GenericGridConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    mutual_active_active: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_passive_active: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_loops_active: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_pol_probes_active: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_passive_passive: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_loops_passive: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_pol_probes_passive: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_plasma_plasma: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_plasma_active: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_plasma_passive: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_pol_probes_plasma: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    mutual_loops_plasma: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    active_coils: Optional[list[str]] = field(
        default=None
    )
    passive_loops: Optional[list[str]] = field(
        default=None
    )
    b_field_pol_probes: Optional[list[str]] = field(
        default=None
    )
    flux_loops: Optional[list[str]] = field(
        default=None
    )
    plasma_elements: Optional[list[str]] = field(
        default=None
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
