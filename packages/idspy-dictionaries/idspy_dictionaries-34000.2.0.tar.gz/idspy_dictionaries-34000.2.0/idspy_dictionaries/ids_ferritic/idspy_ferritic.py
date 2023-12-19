# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


@idspy_dataclass(repr=False, slots=True)
class AnnulusStatic(IdsBaseClass):
    """
    Annulus description (2D object)

    :ivar r: Centre major radius
    :ivar z: Centre height
    :ivar radius_inner: Inner radius
    :ivar radius_outer: Outer radius
    """
    class Meta:
        name = "annulus_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    radius_inner: float = field(
        default=9e+40
    )
    radius_outer: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class ArcsOfCircleStatic(IdsBaseClass):
    """
    Arcs of circle description of a 2D contour.

    :ivar r: Major radii of the start point of each arc of circle
    :ivar z: Height of the start point of each arc of circle
    :ivar curvature_radii: Curvature radius of each arc of circle
    """
    class Meta:
        name = "arcs_of_circle_static"

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
    curvature_radii: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FerriticObjectTimeSlice(IdsBaseClass):
    """
    Dynamic quantities.

    :ivar b_field_r: R component of the magnetic field at each centroid
    :ivar b_field_z: Z component of the magnetic field at each centroid
    :ivar b_field_tor: Toroidal component of the magnetic field at each
        centroid
    :ivar magnetic_moment_r: R component of the magnetic moment of each
        element
    :ivar magnetic_moment_z: Z component of the magnetic moment of each
        element
    :ivar magnetic_moment_tor: Toroidal component of the magnetic moment
        of each element
    :ivar time: Time
    """
    class Meta:
        name = "ferritic_object_time_slice"

    b_field_r: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_z: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_tor: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    magnetic_moment_r: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    magnetic_moment_z: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    magnetic_moment_tor: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    time: Optional[float] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class FerriticPermeabilityTable(IdsBaseClass):
    """
    Permeability table.

    :ivar name: Name of this table
    :ivar description: Description of this table
    :ivar b_field: Array of magnetic field values, for each of which the
        relative permeability is given
    :ivar relative_permeability: Relative permeability as a function of
        the magnetic field
    """
    class Meta:
        name = "ferritic_permeability_table"

    name: str = field(
        default=""
    )
    description: str = field(
        default=""
    )
    b_field: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    relative_permeability: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


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
class ObliqueStatic(IdsBaseClass):
    """
    Description of a 2D parallelogram.

    :ivar r: Major radius of the reference point (from which the alpha
        and beta angles are defined, marked by a + on the diagram)
    :ivar z: Height of the reference point (from which the alpha and
        beta angles are defined, marked by a + on the diagram)
    :ivar length_alpha: Length of the parallelogram side inclined with
        angle alpha with respect to the major radius axis
    :ivar length_beta: Length of the parallelogram side inclined with
        angle beta with respect to the height axis
    :ivar alpha: Inclination of first angle measured counter-clockwise
        from horizontal outwardly directed radial vector (grad R).
    :ivar beta: Inclination of second angle measured counter-clockwise
        from vertically upwards directed vector (grad Z). If both alpha
        and beta are zero (rectangle) then the simpler rectangular
        elements description should be used.
    """
    class Meta:
        name = "oblique_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    length_alpha: float = field(
        default=9e+40
    )
    length_beta: float = field(
        default=9e+40
    )
    alpha: float = field(
        default=9e+40
    )
    beta: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class RectangleStatic(IdsBaseClass):
    """
    Rectangular description of a 2D object.

    :ivar r: Geometric centre R
    :ivar z: Geometric centre Z
    :ivar width: Horizontal full width
    :ivar height: Vertical full height
    """
    class Meta:
        name = "rectangle_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    width: float = field(
        default=9e+40
    )
    height: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Rz0DStatic(IdsBaseClass):
    """
    Structure for a single R, Z position (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Rz1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_static"

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
class Xyz1DPositionsStatic(IdsBaseClass):
    """
    Structure for list of X, Y, Z positions (1D, static)

    :ivar x: List of X coordinates
    :ivar y: List of Y coordinates
    :ivar z: List of Z coordinates
    """
    class Meta:
        name = "xyz1d_positions_static"

    x: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    y: ndarray[(int,), float] = field(
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
class ThickLineStatic(IdsBaseClass):
    """
    2D contour approximated by two points and a thickness (in the direction
    perpendicular to the segment) in the poloidal cross-section.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    :ivar thickness: Thickness
    """
    class Meta:
        name = "thick_line_static"

    first_point: Optional[Rz0DStatic] = field(
        default=None
    )
    second_point: Optional[Rz0DStatic] = field(
        default=None
    )
    thickness: float = field(
        default=9e+40
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
class Outline2DGeometryStatic(IdsBaseClass):
    """
    Description of 2D geometry.

    :ivar geometry_type: Type used to describe the element shape
        (1:'outline', 2:'rectangle', 3:'oblique', 4:'arcs of circle, 5:
        'annulus', 6 : 'thick line')
    :ivar outline: Irregular outline of the element. Do NOT repeat the
        first point.
    :ivar rectangle: Rectangular description of the element
    :ivar oblique: Parallelogram description of the element
    :ivar arcs_of_circle: Description of the element contour by a set of
        arcs of circle. For each of these, the position of the start
        point is given together with the curvature radius. The end point
        is given by the start point of the next arc of circle.
    :ivar annulus: The element is an annulus of centre R, Z, with inner
        radius radius_inner and outer radius radius_outer
    :ivar thick_line: The element is approximated by a rectangle defined
        by a central segment and a thickness in the direction
        perpendicular to the segment
    """
    class Meta:
        name = "outline_2d_geometry_static"

    geometry_type: int = field(
        default=999999999
    )
    outline: Optional[Rz1DStatic] = field(
        default=None
    )
    rectangle: Optional[RectangleStatic] = field(
        default=None
    )
    oblique: Optional[ObliqueStatic] = field(
        default=None
    )
    arcs_of_circle: Optional[ArcsOfCircleStatic] = field(
        default=None
    )
    annulus: Optional[AnnulusStatic] = field(
        default=None
    )
    thick_line: Optional[ThickLineStatic] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class FerriticObject(IdsBaseClass):
    """
    Ferritic object.

    :ivar centroid: List of positions of the centroids, in Cartesian
        coordinates
    :ivar volume: Volume of each element of this object
    :ivar saturated_relative_permeability: Saturated relative magnetic
        permeability of each element
    :ivar permeability_table_index: Index of permeability table to be
        used for each element. If not allocated or if an element is
        equal to EMPTY_INT, use the sibling saturated relative
        permeability instead ../relative_permeability, for that element
    :ivar axisymmetric: Optional equivalent axisymmetric representation
        of the geometry of each element (e.g. for each iron core
        segment), typically used to represent iron core in axisymmetric
        equilibrium solvers
    :ivar ggd_object_index: Index of GGD volumic object corresponding to
        each element. Refers to the array
        /grid_ggd/space(1)/objects_per_dimension(4)/object
    :ivar time_slice: Dynamic quantities, per time slice
    """
    class Meta:
        name = "ferritic_object"

    centroid: Optional[Xyz1DPositionsStatic] = field(
        default=None
    )
    volume: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    saturated_relative_permeability: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    permeability_table_index: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    axisymmetric: list[Outline2DGeometryStatic] = field(
        default_factory=list,
        metadata={
            "max_occurs": 33,
        }
    )
    ggd_object_index: ndarray[(int,), int] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    time_slice: list[FerriticObjectTimeSlice] = field(
        default_factory=list
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
class Ferritic(IdsBaseClass):
    """
    Description of ferritic material (inserts, TBMs, NBI shielding, welds, rebar,
    etc...)

    :ivar ids_properties:
    :ivar object_value: Set of n objects characterized by a list of
        centroids, volumes, and permeabilities. Optionally a full 3D
        description of the n volumes may be given in ../grid_ggd. Here
        the index for each element given in the grid_ggd should be
        referenced by the object set.
    :ivar permeability_table: Set of tables for relative permeability as
        a function of the magnetic field
    :ivar grid_ggd: GGD for describing the 3D geometry of the various
        objects and their elements
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "ferritic"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    object_value: list[FerriticObject] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    permeability_table: list[FerriticPermeabilityTable] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    grid_ggd: Optional[GenericGridConstant] = field(
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
