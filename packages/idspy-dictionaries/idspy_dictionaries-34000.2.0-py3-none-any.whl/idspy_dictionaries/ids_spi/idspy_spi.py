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
class Rzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    phi: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Rzphi1DDynamicRootTime(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (1D, dynamic), using the root time of the
    IDS.

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle
    """
    class Meta:
        name = "rzphi1d_dynamic_root_time"

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
class SpiSpeciesDensity(IdsBaseClass):
    """
    Species included in pellet composition, with species density.

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar label: String identifying the species (e.g. H, D, T, ...)
    :ivar density: Density of the species
    """
    class Meta:
        name = "spi_species_density"

    a: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    density: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class SpiSpeciesFraction(IdsBaseClass):
    """
    Species included in pellet composition, with species atomic fraction.

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar label: String identifying the species (e.g. H, D, T, ...)
    :ivar fraction: Atomic fraction of the species
    """
    class Meta:
        name = "spi_species_fraction"

    a: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    fraction: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Xyz0DConstant(IdsBaseClass):
    """
    Structure for list of X, Y, Z components (0D, constant)

    :ivar x: Component along X axis
    :ivar y: Component along Y axis
    :ivar z: Component along Z axis
    """
    class Meta:
        name = "xyz0d_constant"

    x: float = field(
        default=9e+40
    )
    y: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class Xyz0DStatic(IdsBaseClass):
    """
    Structure for list of X, Y, Z components (0D, static)

    :ivar x: Component along X axis
    :ivar y: Component along Y axis
    :ivar z: Component along Z axis
    """
    class Meta:
        name = "xyz0d_static"

    x: float = field(
        default=9e+40
    )
    y: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
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
class SpiFragment(IdsBaseClass):
    """
    SPI pellet fragment.

    :ivar position: Position of the centre of mass of the pellet
    :ivar velocity_r: Major radius component of the fragment velocity
    :ivar velocity_z: Vertical component of the fragment velocity
    :ivar velocity_tor: Toroidal component of the fragment velocity
    :ivar volume: Volume of the fragment
    :ivar species: Atomic species in the fragment composition
    """
    class Meta:
        name = "spi_fragment"

    position: Optional[Rzphi1DDynamicRootTime] = field(
        default=None
    )
    velocity_r: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    velocity_z: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    velocity_tor: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    volume: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    species: list[SpiSpeciesDensity] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class SpiGas(IdsBaseClass):
    """
    SPI gas.

    :ivar flow_rate: Flow rate of the gas at the injector exit
    :ivar species: Atomic species in the gas composition
    :ivar atoms_n: Total number of atoms of the gas
    :ivar temperature: Gas temperature
    """
    class Meta:
        name = "spi_gas"

    flow_rate: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    species: list[SpiSpeciesFraction] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    atoms_n: float = field(
        default=9e+40
    )
    temperature: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class SpiOpd(IdsBaseClass):
    """
    Optical pellet diagnostic.

    :ivar position: Position of the measurement
    :ivar time_arrival: Arrival time at the optical pellet diagnostic,
        for each object
    """
    class Meta:
        name = "spi_opd"

    position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    time_arrival: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class SpiShatterCone(IdsBaseClass):
    """
    SPI shatter cone.

    :ivar direction: Unit vector of the cone direction
    :ivar origin: Coordinates of the origin of the shatter cone
    :ivar unit_vector_major: Major unit vector describing the geometry
        of the elliptic shatter cone
    :ivar unit_vector_minor: Minor unit vector describing the geometry
        of the elliptic shatter cone
    :ivar angle_major: Angle between the cone direction and
        unit_vector_major
    :ivar angle_minor: Angle between the cone direction and
        unit_vector_minor
    """
    class Meta:
        name = "spi_shatter_cone"

    direction: Optional[Xyz0DConstant] = field(
        default=None
    )
    origin: Optional[Rzphi0DStatic] = field(
        default=None
    )
    unit_vector_major: Optional[Xyz0DStatic] = field(
        default=None
    )
    unit_vector_minor: Optional[Xyz0DStatic] = field(
        default=None
    )
    angle_major: float = field(
        default=9e+40
    )
    angle_minor: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class SpiShell(IdsBaseClass):
    """
    SPI shell.

    :ivar species: Atomic species in the shell composition
    :ivar atoms_n: Total number of atoms of desublimated gas
    """
    class Meta:
        name = "spi_shell"

    species: list[SpiSpeciesDensity] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    atoms_n: float = field(
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
class SpiPellet(IdsBaseClass):
    """
    SPI pellet.

    :ivar position: Position of the centre of mass of the pellet
    :ivar velocity_r: Major radius component of the velocity of the
        centre of mass of the pellet
    :ivar velocity_z: Vertical component of the velocity of the centre
        of mass of the pellet
    :ivar velocity_tor: Toroidal component of the velocity of the centre
        of mass of the pellet
    :ivar velocity_shatter: Norm of the velocity of the centre of mass
        of the pellet right before shattering
    :ivar diameter: Pellet diameter
    :ivar length: Pellet length (cylindrical pellet)
    :ivar shell: Shell-layer around of the unshattered pellet
    :ivar core: Core of the unshattered pellet
    """
    class Meta:
        name = "spi_pellet"

    position: Optional[Rzphi1DDynamicRootTime] = field(
        default=None
    )
    velocity_r: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    velocity_z: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    velocity_tor: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    velocity_shatter: float = field(
        default=9e+40
    )
    diameter: float = field(
        default=9e+40
    )
    length: float = field(
        default=9e+40
    )
    shell: Optional[SpiShell] = field(
        default=None
    )
    core: Optional[SpiShell] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class SpiSingle(IdsBaseClass):
    """
    Description of a single spi system.

    :ivar name: Name of the injector
    :ivar identifier: Identifier of the injector
    :ivar optical_pellet_diagnostic: Information related to the embedded
        optical pellet diagnostic
    :ivar time_trigger: Time of trigger request to the power supply
        according to the DMS sequence
    :ivar time_shatter: Arrival time at the shattering unit
    :ivar pellet: Information related to the pellet
    :ivar fragmentation_gas: Description of the gas produced during
        fragmentation
    :ivar propellant_gas: Description of the propellant gas
    :ivar injection_direction: Unit vector of the unshattered pellet
        velocity direction right before shattering
    :ivar shattering_position: Position where the pellet is shattered.
        It is defined as the intersection of the trayectory of the
        pellet center of mass with the shattering element
    :ivar shattering_angle: Impact (or grazing) angle of the pellet with
        the shattering element. It is the complementary of the incidence
        angle with the element surface at the shattering location
    :ivar shatter_cone: Description of the elliptic shatter cone
    :ivar velocity_mass_centre_fragments_r: Major radius component of
        the velocity of the centre of mass of the fragments at the
        shattering cone origin
    :ivar velocity_mass_centre_fragments_z: Vertical component of the
        velocity velocity of the centre of mass of the fragments at the
        shattering cone origin
    :ivar velocity_mass_centre_fragments_tor: Toroidal component of the
        velocity of the centre of mass of the fragments at the
        shattering cone origin
    :ivar fragment: Set of shattered pellet fragments
    """
    class Meta:
        name = "spi_single"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    optical_pellet_diagnostic: Optional[SpiOpd] = field(
        default=None
    )
    time_trigger: float = field(
        default=9e+40
    )
    time_shatter: float = field(
        default=9e+40
    )
    pellet: Optional[SpiPellet] = field(
        default=None
    )
    fragmentation_gas: Optional[SpiGas] = field(
        default=None
    )
    propellant_gas: Optional[SpiGas] = field(
        default=None
    )
    injection_direction: Optional[Xyz0DConstant] = field(
        default=None
    )
    shattering_position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    shattering_angle: float = field(
        default=9e+40
    )
    shatter_cone: Optional[SpiShatterCone] = field(
        default=None
    )
    velocity_mass_centre_fragments_r: float = field(
        default=9e+40
    )
    velocity_mass_centre_fragments_z: float = field(
        default=9e+40
    )
    velocity_mass_centre_fragments_tor: float = field(
        default=9e+40
    )
    fragment: list[SpiFragment] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Spi(IdsBaseClass):
    """
    Shattered pellets injectors.

    :ivar ids_properties:
    :ivar injector: Set of shattered pellet injectors
    :ivar shatter_cone_definition: Definition of the shatter cone
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "spi"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    injector: list[SpiSingle] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    shatter_cone_definition: Optional[Identifier] = field(
        default=None
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
