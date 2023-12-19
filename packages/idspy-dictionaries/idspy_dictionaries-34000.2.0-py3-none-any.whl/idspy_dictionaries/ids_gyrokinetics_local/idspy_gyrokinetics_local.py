# __version__= "034000.2.0"
# __version_imas_dd__= "03.40.00"
# __imas_dd_git_commit__= "845f1b30816f86a3cd4d53714dc56cdd307fdca1"
# 
from ..dataclasses_idsschema import idspy_dataclass,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@idspy_dataclass(repr=False, slots=True)
class CodePartialConstant(IdsBaseClass):
    """
    Description of code-specific parameters and constant output flag.

    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    """
    class Meta:
        name = "code_partial_constant"

    parameters: str = field(
        default=""
    )
    output_flag: int = field(
        default=999999999
    )


@idspy_dataclass(repr=False, slots=True)
class Collisions(IdsBaseClass):
    """
    Collisions related quantities.

    :ivar collisionality_norm: Normalised collisionality between two
        species
    """
    class Meta:
        name = "gyrokinetics_collisions"

    collisionality_norm: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class EigenmodeFields(IdsBaseClass):
    """
    Electromagnetic fields of a gyrokinetic calculation for a given eigenmode.

    :ivar phi_potential_perturbed_weight: Amplitude of the perturbed
        electrostatic potential normalised to the sum of amplitudes of
        all perturbed fields
    :ivar phi_potential_perturbed_parity: Parity of the perturbed
        electrostatic potential with respect to theta = 0 (poloidal
        angle)
    :ivar a_field_parallel_perturbed_weight: Amplitude of the perturbed
        parallel vector potential normalised to the sum of amplitudes of
        all perturbed fields
    :ivar a_field_parallel_perturbed_parity: Parity of the perturbed
        parallel vector potential with respect to theta = 0 (poloidal
        angle)
    :ivar b_field_parallel_perturbed_weight: Amplitude of the perturbed
        parallel magnetic field normalised to the sum of amplitudes of
        all perturbed fields
    :ivar b_field_parallel_perturbed_parity: Parity of the perturbed
        parallel magnetic field with respect to theta = 0 (poloidal
        angle)
    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_eigenmode_fields"

    phi_potential_perturbed_weight: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    phi_potential_perturbed_parity: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_weight: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_parity: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_weight: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_parity: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    phi_potential_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsFieldsNl1D(IdsBaseClass):
    """
    Fields intensity, 1D, flux surface averaged, summed over kx, time averaged,
    non-linear.

    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_fields_nl_1d"

    phi_potential_perturbed_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsFieldsNl2DFsAverage(IdsBaseClass):
    """
    Fields intensity, 2D, flux surface averaged, non-linear.

    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_fields_nl_2d_fs_average"

    phi_potential_perturbed_norm: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsFieldsNl2DKy0(IdsBaseClass):
    """
    Fields 2D, ky=0, flux surface averaged, non-linear, complex.

    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_fields_nl_2d_ky0"

    phi_potential_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsFieldsNl3D(IdsBaseClass):
    """
    Fields intensity, 3D, non-linear.

    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_fields_nl_3d"

    phi_potential_perturbed_norm: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsFieldsNl4D(IdsBaseClass):
    """
    Fields, 4D, non-linear, complex.

    :ivar phi_potential_perturbed_norm: Normalised perturbed
        electrostatic potential
    :ivar a_field_parallel_perturbed_norm: Normalised perturbed parallel
        vector potential
    :ivar b_field_parallel_perturbed_norm: Normalised perturbed parallel
        magnetic field
    """
    class Meta:
        name = "gyrokinetics_fields_nl_4d"

    phi_potential_perturbed_norm: ndarray[(int, int, int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    a_field_parallel_perturbed_norm: ndarray[(int, int, int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    b_field_parallel_perturbed_norm: ndarray[(int, int, int, int), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxSurface(IdsBaseClass):
    """
    Flux surface characteristics.

    :ivar r_minor_norm: Normalised minor radius of the flux surface of
        interest = 1/2 * (max(R) - min(R))/L_ref
    :ivar elongation: Elongation
    :ivar delongation_dr_minor_norm: Derivative of the elongation with
        respect to r_minor_norm
    :ivar dgeometric_axis_r_dr_minor: Derivative of the major radius of
        the surface geometric axis with respect to r_minor
    :ivar dgeometric_axis_z_dr_minor: Derivative of the height of the
        surface geometric axis with respect to r_minor
    :ivar q: Safety factor
    :ivar magnetic_shear_r_minor: Magnetic shear, defined as
        r_minor_norm/q . dq/dr_minor_norm (different definition from the
        equilibrium IDS)
    :ivar pressure_gradient_norm: Normalised pressure gradient
        (derivative with respect to r_minor_norm)
    :ivar ip_sign: Sign of the plasma current
    :ivar b_field_tor_sign: Sign of the toroidal magnetic field
    :ivar shape_coefficients_c: 'c' coefficients in the formula defining
        the shape of the flux surface
    :ivar dc_dr_minor_norm: Derivative of the 'c' shape coefficients
        with respect to r_minor_norm
    :ivar shape_coefficients_s: 's' coefficients in the formula defining
        the shape of the flux surface
    :ivar ds_dr_minor_norm: Derivative of the 's' shape coefficients
        with respect to r_minor_norm
    """
    class Meta:
        name = "gyrokinetics_flux_surface"

    r_minor_norm: float = field(
        default=9e+40
    )
    elongation: float = field(
        default=9e+40
    )
    delongation_dr_minor_norm: float = field(
        default=9e+40
    )
    dgeometric_axis_r_dr_minor: float = field(
        default=9e+40
    )
    dgeometric_axis_z_dr_minor: float = field(
        default=9e+40
    )
    q: float = field(
        default=9e+40
    )
    magnetic_shear_r_minor: float = field(
        default=9e+40
    )
    pressure_gradient_norm: float = field(
        default=9e+40
    )
    ip_sign: float = field(
        default=9e+40
    )
    b_field_tor_sign: float = field(
        default=9e+40
    )
    shape_coefficients_c: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    dc_dr_minor_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    shape_coefficients_s: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    ds_dr_minor_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Fluxes(IdsBaseClass):
    """
    Turbulent fluxes for a given eigenmode.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes"

    particles_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: float = field(
        default=9e+40
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl1D(IdsBaseClass):
    """
    Turbulent fluxes 1D, non-linear, flux-surface and time averaged, summed over kx
    and ky.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_1d"

    particles_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl2DSumKx(IdsBaseClass):
    """
    Turbulent fluxes 2D, non-linear, time-averaged and flux-surface averaged,
    summed over kx.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_2d_sum_kx"

    particles_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl2DSumKxKy(IdsBaseClass):
    """
    Turbulent fluxes 2D, non-linear, flux-surface averaged, summed over kx and ky.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_2d_sum_kx_ky"

    particles_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl3D(IdsBaseClass):
    """
    Turbulent fluxes 3D, non-linear, time-averaged and flux-surface averaged.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_3d"

    particles_phi_potential: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,int, int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl4D(IdsBaseClass):
    """
    Turbulent fluxes 4D, non-linear, time-averaged.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_4d"

    particles_phi_potential: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class FluxesNl5D(IdsBaseClass):
    """
    Turbulent fluxes 5D, non-linear.

    :ivar particles_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised particle flux
    :ivar particles_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised particle
        flux
    :ivar particles_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised particle flux
    :ivar energy_phi_potential: Contribution of the perturbed
        electrostatic potential to the normalised energy flux
    :ivar energy_a_field_parallel: Contribution of the perturbed
        parallel electromagnetic potential to the normalised energy flux
    :ivar energy_b_field_parallel: Contribution of the perturbed
        parallel magnetic field to the normalised energy flux
    :ivar momentum_tor_parallel_phi_potential: Contribution of the
        perturbed electrostatic potential to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_a_field_parallel: Contribution of the
        perturbed parallel electromagnetic potential to the parallel
        component of the normalised toroidal momentum flux
    :ivar momentum_tor_parallel_b_field_parallel: Contribution of the
        perturbed parallel magnetic field to the parallel component of
        the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_phi_potential: Contribution of the
        perturbed electrostatic potential to the perpendicular component
        of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_a_field_parallel: Contribution of
        the perturbed parallel electromagnetic potential to the
        perpendicular component of the normalised toroidal momentum flux
    :ivar momentum_tor_perpendicular_b_field_parallel: Contribution of
        the perturbed parallel magnetic field to the perpendicular
        component of the normalised toroidal momentum flux
    """
    class Meta:
        name = "gyrokinetics_fluxes_nl_5d"

    particles_phi_potential: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_a_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    particles_b_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_phi_potential: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_a_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    energy_b_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_phi_potential: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_a_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_parallel_b_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_phi_potential: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_a_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    momentum_tor_perpendicular_b_field_parallel: ndarray[(int,int,int,int,int), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class InputNormalizing(IdsBaseClass):
    """
    GK normalizing quantities.

    :ivar t_e: Electron temperature at outboard equatorial midplane of
        the flux surface (angle_pol = 0)
    :ivar n_e: Electron density at outboard equatorial midplane of the
        flux surface (angle_pol = 0)
    :ivar r: Major radius of the flux surface of interest, defined as
        (min(R)+max(R))/2
    :ivar b_field_tor: Toroidal magnetic field at major radius r
    """
    class Meta:
        name = "gyrokinetics_input_normalizing"

    t_e: float = field(
        default=9e+40
    )
    n_e: float = field(
        default=9e+40
    )
    r: float = field(
        default=9e+40
    )
    b_field_tor: float = field(
        default=9e+40
    )


@idspy_dataclass(repr=False, slots=True)
class InputSpeciesGlobal(IdsBaseClass):
    """
    Species global parameters.

    :ivar beta_reference: Reference plasma beta (see detailed
        documentation at the root of the IDS)
    :ivar velocity_tor_norm: Normalised toroidal velocity of species
        (all species are assumed to have a purely toroidal velocity with
        a common toroidal angular frequency)
    :ivar debye_length_norm: Debye length computed from the reference
        quantities (see detailed documentation at the root of the IDS)
    :ivar shearing_rate_norm: Normalised ExB shearing rate (for non-
        linear runs only)
    :ivar angle_pol: Poloidal angle grid, from -pi to pi, on which the
        species dependent effective potential energy (which determines
        the poloidal variation of the density) is expressed. The angle
        is defined with respect to (R0,Z0) with R0=(Rmax-Rmin)/2 and
        Z0=(Zmax-Zmin)/2. It is increasing clockwise. So (r,theta,phi)
        is right-handed. theta=0 for Z=Z0 and R&gt;R0 (LFS)
    """
    class Meta:
        name = "gyrokinetics_input_species_global"

    beta_reference: float = field(
        default=9e+40
    )
    velocity_tor_norm: float = field(
        default=9e+40
    )
    debye_length_norm: float = field(
        default=9e+40
    )
    shearing_rate_norm: float = field(
        default=9e+40
    )
    angle_pol: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Model(IdsBaseClass):
    """
    Description of the GK model assumptions.

    :ivar include_a_field_parallel: Flag = 1 if fluctuations of the
        parallel vector potential are retained, 0 otherwise
    :ivar include_b_field_parallel: Flag = 1 if fluctuations of the
        parallel magnetic field are retained, 0 otherwise
    :ivar include_full_curvature_drift: Flag = 1 if all contributions to
        the curvature drift are included (including beta_prime), 0
        otherwise. Neglecting the beta_prime contribution (Flag=0) is
        only recommended together with the neglect of parallel magnetic
        field fluctuations
    :ivar include_coriolis_drift: Flag = 1 if Coriolis drift is
        included, 0 otherwise
    :ivar include_centrifugal_effects: Flag = 1 if centrifugal effects
        are retained, 0 otherwise
    :ivar collisions_pitch_only: Flag = 1 if only pitch-angle scattering
        is retained, 0 otherwise
    :ivar collisions_momentum_conservation: Flag = 1 if the collision
        operator conserves momentum, 0 otherwise
    :ivar collisions_energy_conservation: Flag = 1 if the collision
        operator conserves energy, 0 otherwise
    :ivar collisions_finite_larmor_radius: Flag = 1 if finite larmor
        radius effects are retained in the collision operator, 0
        otherwise
    :ivar adiabatic_electrons: Flag = 1 if electrons are adiabatic, 0
        otherwise
    """
    class Meta:
        name = "gyrokinetics_model"

    include_a_field_parallel: int = field(
        default=999999999
    )
    include_b_field_parallel: int = field(
        default=999999999
    )
    include_full_curvature_drift: int = field(
        default=999999999
    )
    include_coriolis_drift: int = field(
        default=999999999
    )
    include_centrifugal_effects: int = field(
        default=999999999
    )
    collisions_pitch_only: int = field(
        default=999999999
    )
    collisions_momentum_conservation: int = field(
        default=999999999
    )
    collisions_energy_conservation: int = field(
        default=999999999
    )
    collisions_finite_larmor_radius: int = field(
        default=999999999
    )
    adiabatic_electrons: int = field(
        default=999999999
    )


@idspy_dataclass(repr=False, slots=True)
class MomentsLinear(IdsBaseClass):
    """
    Turbulent moments for a given eigenmode and a given species.

    :ivar density: Normalised density
    :ivar j_parallel: Normalised parallel current density
    :ivar pressure_parallel: Normalised parallel temperature
    :ivar pressure_perpendicular: Normalised perpendicular temperature
    :ivar heat_flux_parallel: Normalised parallel heat flux (integral of
        0.5 * m * v_par * v^2)
    :ivar v_parallel_energy_perpendicular: Normalised moment (integral
        over 0.5 * m * v_par * v_perp^2)
    :ivar v_perpendicular_square_energy: Normalised moment (integral
        over 0.5 * m * v_perp^2 * v^2)
    """
    class Meta:
        name = "gyrokinetics_moments_linear"

    density: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    j_parallel: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    pressure_parallel: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    pressure_perpendicular: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    heat_flux_parallel: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    v_parallel_energy_perpendicular: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    v_perpendicular_square_energy: ndarray[(int, int, int ), complex] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class Species(IdsBaseClass):
    """
    List of species.

    :ivar charge_norm: Normalised charge
    :ivar mass_norm: Normalised mass
    :ivar density_norm: Normalised density
    :ivar density_log_gradient_norm: Normalised logarithmic gradient
        (with respect to r_minor_norm) of the density
    :ivar temperature_norm: Normalised temperature
    :ivar temperature_log_gradient_norm: Normalised logarithmic gradient
        (with respect to r_minor_norm) of the temperature
    :ivar velocity_tor_gradient_norm: Normalised gradient (with respect
        to r_minor_norm) of the toroidal velocity
    :ivar potential_energy_norm: Normalised gradient (with respect to
        r_minor_norm) of the effective potential energy
    :ivar potential_energy_gradient_norm: Effective potential energy
        determining the poloidal variation of the species background
        density
    """
    class Meta:
        name = "gyrokinetics_species"

    charge_norm: float = field(
        default=9e+40
    )
    mass_norm: float = field(
        default=9e+40
    )
    density_norm: float = field(
        default=9e+40
    )
    density_log_gradient_norm: float = field(
        default=9e+40
    )
    temperature_norm: float = field(
        default=9e+40
    )
    temperature_log_gradient_norm: float = field(
        default=9e+40
    )
    velocity_tor_gradient_norm: float = field(
        default=9e+40
    )
    potential_energy_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    potential_energy_gradient_norm: ndarray[(int,), float] = field(
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
class Eigenmode(IdsBaseClass):
    """
    Output of the GK calculation for a given eigenmode.

    :ivar poloidal_turns: Number of poloidal turns considered in the
        flux-tube simulation
    :ivar growth_rate_norm: Growth rate
    :ivar frequency_norm: Frequency
    :ivar growth_rate_tolerance: Relative tolerance on the growth rate
        (convergence of the simulation)
    :ivar angle_pol: Poloidal angle grid. The angle is defined with
        respect to (R0,Z0) with R0=(Rmax-Rmin)/2 and Z0=(Zmax-Zmin)/2.
        It is increasing clockwise. So (r,theta,phi) is right-handed.
        theta=0 for Z=Z0 and R&gt;R0 (LFS)
    :ivar time_norm: Normalised time of the gyrokinetic simulation
    :ivar fields: Electrostatic potential, magnetic field and magnetic
        vector potential
    :ivar code: Code-specific parameters used for this eigenmode
    :ivar initial_value_run: Flag = 1 if this is an initial value run, 0
        for an eigenvalue run
    :ivar moments_norm_gyrocenter: Moments (normalised) of the perturbed
        distribution function of gyrocenters
    :ivar moments_norm_particle: Moments (normalised) of the perturbed
        distribution function of particles
    :ivar moments_norm_gyrocenter_bessel_0: Moments (normalised) of the
        perturbed distribution function of gyrocenters times 0th order
        Bessel function of the first kind
    :ivar moments_norm_gyrocenter_bessel_1: Moments (normalised) of the
        perturbed distribution function of gyrocenters times 1st order
        Bessel function of the first kind
    :ivar linear_weights: Normalised fluxes in the laboratory frame
    :ivar linear_weights_rotating_frame: Normalised fluxes in the
        rotating frame
    """
    class Meta:
        name = "gyrokinetics_eigenmode"

    poloidal_turns: int = field(
        default=999999999
    )
    growth_rate_norm: float = field(
        default=9e+40
    )
    frequency_norm: float = field(
        default=9e+40
    )
    growth_rate_tolerance: float = field(
        default=9e+40
    )
    angle_pol: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    time_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    fields: Optional[EigenmodeFields] = field(
        default=None
    )
    code: Optional[CodePartialConstant] = field(
        default=None
    )
    initial_value_run: int = field(
        default=999999999
    )
    moments_norm_gyrocenter: Optional[MomentsLinear] = field(
        default=None
    )
    moments_norm_particle: Optional[MomentsLinear] = field(
        default=None
    )
    moments_norm_gyrocenter_bessel_0: Optional[MomentsLinear] = field(
        default=None
    )
    moments_norm_gyrocenter_bessel_1: Optional[MomentsLinear] = field(
        default=None
    )
    linear_weights: Optional[Fluxes] = field(
        default=None
    )
    linear_weights_rotating_frame: Optional[Fluxes] = field(
        default=None
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsNonLinear(IdsBaseClass):
    """
    Non-linear simulation.

    :ivar binormal_wavevector_norm: Array of normalised binormal
        wavevectors
    :ivar radial_wavevector_norm: Array of normalised radial wavevectors
    :ivar angle_pol: Poloidal angle grid. The angle is defined with
        respect to (R0,Z0) with R0=(Rmax-Rmin)/2 and Z0=(Zmax-Zmin)/2.
        It is increasing clockwise. So (r,theta,phi) is right-handed.
        theta=0 for Z=Z0 and R&gt;R0 (LFS)
    :ivar time_norm: Normalised time of the gyrokinetic simulation
    :ivar time_interval_norm: Normalised time interval used to average
        fluxes in non-linear runs
    :ivar quasi_linear: Flag = 1 if the non-linear fluxes are in fact
        calculated by a quasi-linear model, 0 if non-linear
    :ivar code: Code-specific parameters used for the non-linear
        simulation
    :ivar fluxes_5d: 5D fluxes
    :ivar fluxes_4d: 4D fluxes (time averaged)
    :ivar fluxes_3d: 3D fluxes (time and flux surface averaged)
    :ivar fluxes_2d_k_x_sum: 2D fluxes (time and flux-surface averaged),
        summed over kx
    :ivar fluxes_2d_k_x_k_y_sum: 2D fluxes (flux-surface averaged),
        summed over kx and ky
    :ivar fluxes_1d: 1D fluxes (flux-surface and time averaged), summed
        over kx and ky
    :ivar fields_4d: 4D fields
    :ivar fields_intensity_3d: 3D fields (time averaged)
    :ivar fields_intensity_2d_surface_average: 2D fields (time averaged
        and flux surface averaged)
    :ivar fields_zonal_2d: 2D zonal fields (taken at ky=0, flux surface
        averaged)
    :ivar fields_intensity_1d: 1D fields (summed over kx, time averaged
        and flux surface averaged)
    :ivar fluxes_5d_rotating_frame: 5D fluxes in the rotating frame
    :ivar fluxes_4d_rotating_frame: 4D fluxes (time averaged) in the
        rotating frame
    :ivar fluxes_3d_rotating_frame: 3D fluxes (time and flux surface
        averaged) in the rotating frame
    :ivar fluxes_2d_k_x_sum_rotating_frame: 2D fluxes (time and flux-
        surface averaged), summed over kx in the rotating frame
    :ivar fluxes_2d_k_x_k_y_sum_rotating_frame: 2D fluxes (flux-surface
        averaged), summed over kx and ky in the rotating frame
    :ivar fluxes_1d_rotating_frame: 1D fluxes (flux-surface and time
        averaged), summed over kx and ky in the rotating frame
    """
    class Meta:
        name = "gyrokinetics_non_linear"

    binormal_wavevector_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    radial_wavevector_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    angle_pol: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    time_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    time_interval_norm: ndarray[(int,), float] = field(
        default_factory=list,
        metadata={
            "max_occurs": 999,
        }
    )
    quasi_linear: int = field(
        default=999999999
    )
    code: Optional[CodePartialConstant] = field(
        default=None
    )
    fluxes_5d: Optional[FluxesNl5D] = field(
        default=None
    )
    fluxes_4d: Optional[FluxesNl4D] = field(
        default=None
    )
    fluxes_3d: Optional[FluxesNl3D] = field(
        default=None
    )
    fluxes_2d_k_x_sum: Optional[FluxesNl2DSumKx] = field(
        default=None
    )
    fluxes_2d_k_x_k_y_sum: Optional[FluxesNl2DSumKxKy] = field(
        default=None
    )
    fluxes_1d: Optional[FluxesNl1D] = field(
        default=None
    )
    fields_4d: Optional[GyrokineticsFieldsNl4D] = field(
        default=None
    )
    fields_intensity_3d: Optional[GyrokineticsFieldsNl3D] = field(
        default=None
    )
    fields_intensity_2d_surface_average: Optional[GyrokineticsFieldsNl2DFsAverage] = field(
        default=None
    )
    fields_zonal_2d: Optional[GyrokineticsFieldsNl2DKy0] = field(
        default=None
    )
    fields_intensity_1d: Optional[GyrokineticsFieldsNl1D] = field(
        default=None
    )
    fluxes_5d_rotating_frame: Optional[FluxesNl5D] = field(
        default=None
    )
    fluxes_4d_rotating_frame: Optional[FluxesNl4D] = field(
        default=None
    )
    fluxes_3d_rotating_frame: Optional[FluxesNl3D] = field(
        default=None
    )
    fluxes_2d_k_x_sum_rotating_frame: Optional[FluxesNl2DSumKx] = field(
        default=None
    )
    fluxes_2d_k_x_k_y_sum_rotating_frame: Optional[FluxesNl2DSumKxKy] = field(
        default=None
    )
    fluxes_1d_rotating_frame: Optional[FluxesNl1D] = field(
        default=None
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
class Wavevector(IdsBaseClass):
    """
    Components of the linear mode wavevector.

    :ivar radial_wavevector_norm: Normalised radial component of the
        wavevector
    :ivar binormal_wavevector_norm: Normalised binormal component of the
        wavevector
    :ivar eigenmode: Set of eigenmode for this wavector
    """
    class Meta:
        name = "gyrokinetics_wavevector"

    radial_wavevector_norm: float = field(
        default=9e+40
    )
    binormal_wavevector_norm: float = field(
        default=9e+40
    )
    eigenmode: list[Eigenmode] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
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
class GyrokineticsLinear(IdsBaseClass):
    """
    Linear simulation.

    :ivar wavevector: Set of wavevectors
    """
    class Meta:
        name = "gyrokinetics_linear"

    wavevector: list[Wavevector] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@idspy_dataclass(repr=False, slots=True)
class GyrokineticsLocal(IdsBaseClass):
    """Description of a local gyrokinetic simulation (delta-f, flux-tube).

    All quantities within this IDS are normalised (apart from time and
    from the normalizing quantities structure), thus independent of
    rhostar, consistently with the local approximation and a spectral
    representation is assumed in the perpendicular plane (i.e.
    homogeneous turbulence).

    :ivar ids_properties:
    :ivar normalizing_quantities: Physical quantities used for
        normalization (useful to link to the original
        simulation/experience)
    :ivar flux_surface: Flux surface characteristics
    :ivar linear: Linear simulation
    :ivar non_linear: Non-linear simulation
    :ivar model: Assumptions of the GK calculations
    :ivar species_all: Physical quantities common to all species
    :ivar species: Set of species (including electrons) used in the
        calculation and related quantities
    :ivar collisions: Collisions related quantities
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "gyrokinetics_local"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    normalizing_quantities: Optional[InputNormalizing] = field(
        default=None
    )
    flux_surface: Optional[FluxSurface] = field(
        default=None
    )
    linear: Optional[GyrokineticsLinear] = field(
        default=None
    )
    non_linear: Optional[GyrokineticsNonLinear] = field(
        default=None
    )
    model: Optional[Model] = field(
        default=None
    )
    species_all: Optional[InputSpeciesGlobal] = field(
        default=None
    )
    species: list[Species] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    collisions: Optional[Collisions] = field(
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
