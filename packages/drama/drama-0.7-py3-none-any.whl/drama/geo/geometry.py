from collections import namedtuple
from collections.abc import Iterable
from typing import Union
from datetime import datetime

import numpy as np
import numpy.typing as npt
import scipy.constants as sp_constants
from scipy import interpolate
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation as R
from astropy.time import Time

import drama.utils.gohlke_transf as trans
import drama.orbits.formation as d_formation
import drama.orbits.two_body as d_two_body
from drama import constants as const
from drama.orbits import orbit_to_vel
from drama.utils.coord_trans import rot_z, rot_z_prime


class QuickRadarGeometry(object):
    """This class allows quick geom calculations for a radar on a
    circular orbit around a spherical planet.

    Parameters
    ----------
    orbit_height :
        orbit height above surface
    r_planet :
        radious of planet, default's to Earth's
    gm_planet :
        mass of planet, default's to Earths
    degrees :
        if set, everything is in degrees, defaults to False.

    Returns
    -------

    """

    def __init__(
        self,
        orbit_height,
        r_planet=const.r_earth,
        gm_planet=const.gm_earth,
        degrees=False,
    ):
        """Initialise QuickRadarGeometry."""
        self.r_planet = r_planet
        self.gm_planet = gm_planet
        self.h_orb = orbit_height
        self.degrees = degrees
        self.max_look_angle = self.__angout(
            max_look_angle(self.h_orb, r_planet=self.r_planet)
        )
        (
            self.__sr2look,
            self.__sr2inc,
            self.__sr2gr,
            self.__sr2b,
            self.sr_max,
            self.__gr2look,
            self.__gr2inc,
            self.__gr2sr,
            self.__gr2b,
            self.gr_max,
        ) = self.__sr2geo(interp_method="linear", npts=500)

    def __angin(self, a):
        if self.degrees:
            return np.radians(a)
        else:
            return a

    def __angout(self, a):
        if self.degrees:
            return np.degrees(a)
        else:
            return a

    def inc_to_sr(self, theta_i):
        """

        Parameters
        ----------
        theta_i :


        Returns
        -------

        """
        return inc_to_sr(self.__angin(theta_i), self.h_orb, r_planet=self.r_planet)

    def inc_to_gr(self, theta_i):
        """

        Parameters
        ----------
        theta_i :


        Returns
        -------

        """
        return inc_to_gr(self.__angin(theta_i), self.h_orb, r_planet=self.r_planet)

    def inc_to_look(self, theta_i):
        """

        Parameters
        ----------
        theta_i :


        Returns
        -------

        """
        return self.__angout(
            inc_to_look(self.__angin(theta_i), self.h_orb, r_planet=self.r_planet)
        )

    def look_to_inc(self, theta_l):
        """

        Parameters
        ----------
        theta_l :


        Returns
        -------

        """
        return self.__angout(
            look_to_inc(self.__angin(theta_l), self.h_orb, r_planet=self.r_planet)
        )

    def look_to_sr(self, theta_l):
        """

        Parameters
        ----------
        theta_l :


        Returns
        -------

        """
        return look_to_sr(self.__angin(theta_l), self.h_orb, r_planet=self.r_planet)

    def look_to_gr(self, theta_l):
        """

        Parameters
        ----------
        theta_l :


        Returns
        -------

        """
        return self.inc_to_gr(self.look_to_inc(theta_l))

    def sr_to_inc(self, sr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = np.logical_and(sr < self.sr_max, sr > self.h_orb)
        return np.where(val_mask, self.__sr2inc(sr), np.NaN)

    def sr_to_look(self, sr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = np.logical_and(sr < self.sr_max, sr > self.h_orb)
        return np.where(val_mask, self.__sr2look(sr), np.NaN)

    def sr_to_gr(self, sr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = np.logical_and(sr < self.sr_max, sr > self.h_orb)
        return np.where(val_mask, self.__sr2gr(sr), np.NaN)

    def sr_to_b(self, sr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = np.logical_and(sr < self.sr_max, sr > self.h_orb)
        return np.where(val_mask, self.__sr2b(sr), np.NaN)

    def gr_to_inc(self, gr):
        """

        Parameters
        ----------
        gr :


        Returns
        -------

        """
        val_mask = gr < self.gr_max
        return np.where(val_mask, self.__gr2inc(gr), np.NaN)

    def gr_to_look(self, gr):
        """

        Parameters
        ----------
        gr :


        Returns
        -------

        """
        val_mask = gr < self.gr_max
        return np.where(val_mask, self.__gr2look(gr), np.NaN)

    def gr_to_sr(self, gr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = gr < self.gr_max
        return np.where(val_mask, self.__gr2sr(gr), np.NaN)

    def gr_to_b(self, gr):
        """

        Parameters
        ----------
        sr :


        Returns
        -------

        """
        val_mask = gr < self.gr_max
        return np.where(val_mask, self.__gr2b(gr), np.NaN)

    def __sr2geo(self, npts=500, interp_method="linear"):
        theta_l = np.linspace(0, self.max_look_angle, npts)
        theta_i = self.look_to_inc(theta_l)
        delta_theta = self.__angin(theta_i - theta_l)  # This is now in radians
        r_track = np.cos(delta_theta) * self.r_planet
        v_orb = orbit_to_vel(
            self.h_orb, r_planet=self.r_planet, m_planet=self.gm_planet
        )
        b = v_orb**2 * r_track / (self.r_planet + self.h_orb)
        # Calculate Ground Range and Slant Range
        gr = self.r_planet * delta_theta
        sr = np.sqrt(
            (self.h_orb + self.r_planet - self.r_planet * np.cos(delta_theta)) ** 2
            + (self.r_planet * np.sin(delta_theta)) ** 2
        )
        sr2look = interpolate.interp1d(
            sr, theta_l, interp_method, bounds_error=False, fill_value=np.NaN
        )
        sr2inc = interpolate.interp1d(
            sr, theta_i, interp_method, bounds_error=False, fill_value=np.NaN
        )
        sr2gr = interpolate.interp1d(
            sr, gr, interp_method, bounds_error=False, fill_value=np.NaN
        )
        sr2b = interpolate.interp1d(
            sr, b, interp_method, bounds_error=False, fill_value=np.NaN
        )

        gr2look = interpolate.interp1d(
            gr, theta_l, interp_method, bounds_error=False, fill_value=np.NaN
        )
        gr2inc = interpolate.interp1d(
            gr, theta_i, interp_method, bounds_error=False, fill_value=np.NaN
        )
        gr2sr = interpolate.interp1d(
            gr, sr, interp_method, bounds_error=False, fill_value=np.NaN
        )
        gr2b = interpolate.interp1d(
            gr, b, interp_method, bounds_error=False, fill_value=np.NaN
        )
        return (
            sr2look,
            sr2inc,
            sr2gr,
            sr2b,
            sr.max(),
            gr2look,
            gr2inc,
            gr2sr,
            gr2b,
            gr.max(),
        )


def inc_to_sr(theta_i, orbit_alt, r_planet=const.r_earth):
    """Calculates slant range angle given incidence angle

    Parameters
    ----------
    theta_i :
        Incidence angle
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        Slant range

    """

    theta_l = inc_to_look(theta_i, orbit_alt, r_planet=r_planet)
    delta_theta = theta_i - theta_l

    return np.sqrt(
        (orbit_alt + r_planet - r_planet * np.cos(delta_theta)) ** 2
        + (r_planet * np.sin(delta_theta)) ** 2
    )


def inc_to_gr(theta_i, orbit_alt, r_planet=const.r_earth):
    """Calculates ground range given incidence angle

    Parameters
    ----------
    theta_i :
        Incidence angle
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        Ground range

    """
    return r_planet * (theta_i - inc_to_look(theta_i, orbit_alt, r_planet=r_planet))


def inc_to_look(theta_i, orbit_alt, r_planet=const.r_earth):
    """Calculates look angle given incidence angle

    Parameters
    ----------
    theta_i :
        Incidence angle [rad]
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        Look angle [rad]

    """

    return np.arcsin(np.sin(theta_i) / (r_planet + orbit_alt) * r_planet)


def look_to_inc(theta_l, orbit_alt, r_planet=const.r_earth):
    """Calculates incidence angle given look angle

    Parameters
    ----------
    theta_l :
        Look angle
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        Incidence angle

    """
    return np.arcsin(np.sin(theta_l) * (r_planet + orbit_alt) / r_planet)


def look_to_sr(theta_l, orbit_alt, r_planet=const.r_earth):
    """Calculates slant range angle given look angle

    Parameters
    ----------
    theta_l :
        Look angle
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        slant range

    """
    theta_i = look_to_inc(theta_l, orbit_alt, r_planet=r_planet)
    delta_theta = theta_i - theta_l
    return np.sqrt(
        (orbit_alt + r_planet - r_planet * np.cos(delta_theta)) ** 2
        + (r_planet * np.sin(delta_theta)) ** 2
    )


def sr_to_geo(slant_range, orbit_alt, r_planet=const.r_earth, m_planet=const.m_earth):
    """Calculates zero Doppler interpolated SAR geometric parameters given a
        set of slant range points

    Parameters
    ----------
    slant_range :
        Set of ground range points
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius
    m_planet :
        mass of planet, defaults to Earth's mass

    Returns
    -------
    type
        ground range, incidence angle, look angle

    """
    # Calculate look/incident angles
    theta_l = np.linspace(0, max_look_angle(orbit_alt, r_planet=r_planet), 500)
    theta_i = look_to_inc(theta_l, orbit_alt, r_planet=r_planet)
    delta_theta = theta_i - theta_l
    r_track = np.cos(delta_theta) * r_planet
    v_orb = orbit_to_vel(orbit_alt, r_planet=r_planet, m_planet=m_planet)
    b = v_orb**2 * r_track / (r_planet + orbit_alt)

    # Calculate Ground Range and Slant Range
    gr = r_planet * delta_theta
    sr = np.sqrt(
        (orbit_alt + r_planet - r_planet * np.cos(delta_theta)) ** 2
        + (r_planet * np.sin(delta_theta)) ** 2
    )

    # Interpolate look/incidence angles and Slant Range
    val_mask = np.logical_and(slant_range < sr.max(), slant_range > sr.min())
    theta_l_interp = np.where(
        val_mask,
        interpolate.interp1d(
            sr, theta_l, "linear", bounds_error=False, fill_value=np.NaN
        )(slant_range),
        np.NaN,
    )
    theta_i_interp = np.where(
        val_mask,
        interpolate.interp1d(
            sr, theta_i, "linear", bounds_error=False, fill_value=np.NaN
        )(slant_range),
        np.NaN,
    )
    gr_interp = np.where(
        val_mask,
        interpolate.interp1d(sr, gr, "linear", bounds_error=False, fill_value=np.NaN)(
            slant_range
        ),
        np.NaN,
    )
    b_interp = np.where(
        val_mask,
        interpolate.interp1d(sr, b, "linear", bounds_error=False, fill_value=np.NaN)(
            slant_range
        ),
        np.NaN,
    )
    return gr_interp, theta_i_interp, theta_l_interp, b_interp


def gr_to_geo(ground_range, orbit_alt, r_planet=const.r_earth):
    """Calculates interpolated SAR geometric parameters given a set of
        ground range points

    Parameters
    ----------
    ground_range :
        Set of ground range points
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        slant range, incidence angle, look angle

    """
    # Calculate look/incident angles
    theta_l = np.linspace(0, max_look_angle(orbit_alt), 500)
    theta_i = look_to_inc(theta_l, orbit_alt, r_planet=r_planet)
    delta_theta = theta_i - theta_l

    # Calculate Ground Range and Slant Range
    gr = r_planet * delta_theta
    sr = np.sqrt(
        (orbit_alt + const.r_earth - r_planet * np.cos(delta_theta)) ** 2
        + (r_planet * np.sin(delta_theta)) ** 2
    )

    # Interpolate look/incidence angles and Slant Range
    theta_l_interp = interpolate.interp1d(
        gr, theta_l, "linear", bounds_error=False, fill_value=np.NaN
    )(ground_range)
    theta_i_interp = interpolate.interp1d(
        gr, theta_i, "linear", bounds_error=False, fill_value=np.NaN
    )(ground_range)
    sr_interp = interpolate.interp1d(
        gr, sr, "linear", bounds_error=False, fill_value=np.NaN
    )(ground_range)

    return sr_interp, theta_i_interp, theta_l_interp


def max_look_angle(orbit_alt, r_planet=const.r_earth):
    """Calculates maximum look angle given satellite orbit altitude

    Parameters
    ----------
    orbit_alt :
        Satellite orbit altitude
    r_planet :
        radious of planet, defaults to Earth's radius

    Returns
    -------
    type
        Maximum look angle

    """
    return np.arcsin(r_planet / (r_planet + orbit_alt))


def geodetic_to_ecef(geodetic):
    """convert ecef coords to geodetic or opposite (accurate)

    Parameters
    ----------
    coords :
        ecef -> [x, y, z]) (geodetic -> [lat, lon, alt]
        lat and lon in degrees)
    inverse :
        inverse the transformation (Default value = False)

    Returns
    -------

    """
    retrans = False  # flag to return coords with same format
    if isinstance(geodetic, list):
        geodetic = np.array(geodetic)
    if geodetic.ndim == 1:
        geodetic = geodetic[np.newaxis, :]
    if geodetic.shape[1] != 3:
        geodetic = geodetic.T
        retrans = True

    a = const.r_equatorial["wgs84"]
    b = const.r_polar["wgs84"]
    e = np.sqrt((a**2 - b**2) / (a**2))
    # Radius of curvature [m]
    N = a / np.sqrt(1 - (e**2) * (np.sin(np.radians(geodetic[:, 0]))) ** 2)

    X = (
        (N + geodetic[:, 2])
        * np.cos(np.radians(geodetic[:, 0]))
        * np.cos(np.radians(geodetic[:, 1]))
    )
    Y = (
        (N + geodetic[:, 2])
        * np.cos(np.radians(geodetic[:, 0]))
        * np.sin(np.radians(geodetic[:, 1]))
    )
    Z = ((b**2) / (a**2) * N + geodetic[:, 2]) * np.sin(np.radians(geodetic[:, 0]))

    new_coord0 = np.vstack((X[np.newaxis, :], Y[np.newaxis, :], Z[np.newaxis, :]))
    # convert  eci to ecef

    # rotational matrix from ECI to ECEF
    new_geodetic = rot_z(new_coord0, const.omega_earth)
    if retrans:
        new_geodetic = new_geodetic.T
    return new_geodetic.T


def ecef_to_geodetic(ecef: npt.ArrayLike) -> np.ndarray:
    """Convert Earth-centered Earth-fixed coordinates to latitude, longitude and altitude.

    Parameters
    ----------
    ecef : npt.ArrayLike
        ecef -> [x, y, z])

    Returns
    -------
    np.ndarray
        The output coordinates in the geodetic frame.
        geodetic -> [lat, lon, alt] lat and lon in degrees. The output
        will have the same shape as the input array. For an N by 3
        input array of N ECEF coordinates the output will be an N by 3
        array lat, lon, alt.

    Notes
    -----
    Based on Algorithm 12 of_[1] and the closed formula set of section 2.2 of_[2].

    References
    ----------
    .. [1] Vallado DA, McClain WD. Fundamentals of Astrodynamics and Applications. 4th ed. Hawthorne, CA: Microcosm Press; 2013.
    .. [2] mu-blox AG (1999). Datum Transformations of GPS Positions. Application Note
    """
    x = np.atleast_1d(ecef[..., 0])
    y = np.atleast_1d(ecef[..., 1])
    z = np.atleast_1d(ecef[..., 2])

    a = const.r_equatorial["wgs84"]
    b = const.r_polar["wgs84"]

    e = np.sqrt((a**2 - b**2) / a**2)
    e_prime = np.sqrt((a**2 - b**2) / b**2)

    p = np.sqrt(x**2 + y**2)
    theta = np.arctan2(z * a, p * b)

    lon = np.arctan2(y, x)
    lat = np.arctan2(
        z + ((e_prime**2) * b * (np.sin(theta)) ** 3),
        p - ((e**2) * a * (np.cos(theta) ** 3)),
    )

    N = a / np.sqrt(1 - (e**2) * (np.sin(lat) ** 2))
    alt = np.empty_like(lon)
    alt = p / np.cos(lat) - N

    # According to Vallado_[1] the region around the poles by 1 degree is critical
    critical_value = np.cos(np.deg2rad(89)) - np.cos(np.deg2rad(+90))
    mask = np.abs(np.cos(lat)) < critical_value
    alt[mask] = (z / np.sin(lat) - N * (1 - e**2))[mask]
    geodetic = np.squeeze(np.column_stack((np.rad2deg(lat), np.rad2deg(lon), alt)))
    return geodetic


def eci_to_ecef(
    eci: npt.ArrayLike, epoch: Union[datetime, Iterable[datetime]]
) -> np.ndarray:
    """Convert Earth-centered Inertial coordinates to Earth-centered Earth-fixed.

    Parameters
    ----------
    eci : npt.ArrayLike
        Coordinates in ECI. Accepts both a 1D (of shape (3,)) array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    epoch : Union(datetime, Iterable[datetime])
        The epoch corresponding to each set of coordinates in UTC. Both date and time must be specified. The number of epochs must match the number of coordinates.

    Returns
    -------
    np.ndarray
        The input coordinates represented in the ECEF frame.
    """
    eci = np.atleast_1d(eci)
    epoch = np.atleast_1d(epoch)
    r_z = r_eci_to_ecef(epoch)
    # express the rotation as a rotation matrix
    r_z = r_z.as_matrix()
    # r_z will have shape (N, 3, 3) and eci (3,) or (N, 3) or (N, f, 3) for f number of
    # formations so add a singleton dimension to eci to allow broadcasting. If eci has 3
    # dimensions because of different formations, we need to add a singleton dimension
    # to broadcast the rotation matrix over them.
    if eci.ndim == 3:
        r_z = r_z[:, np.newaxis, ...]
    return np.squeeze(r_z @ eci[..., np.newaxis])


def r_eci_to_ecef(epoch: Union[datetime, Iterable[datetime]]) -> R:
    # Convert the epoch to Greenwich apparent sidereal time.
    gm_st = Time(epoch).sidereal_time("apparent", "greenwich").radian
    # The angle is negated because R.from_euler() produces a rotation
    # matrix using the alibi convention but since we want to rotate
    # the axes of the ECI frame we are interested in an alias
    # rotation.
    # See https://en.wikipedia.org/wiki/Rotation_matrix#Ambiguities
    return R.from_euler("z", -gm_st, degrees=False)


def ecef_to_eci(
    ecef: npt.ArrayLike, epoch: Union[datetime, Iterable[datetime]]
) -> np.ndarray:
    """Convert Earth-centered Earth-fixed coordinates to Earth-centered Inertial.

    Parameters
    ----------
    ecef : npt.ArrayLike
        Coordinates in ECEF. Accepts both a 1D (of shape (3,)) array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    epoch : Union(datetime, Iterable[datetime])
        The epoch corresponding to each set of coordinates in UTC. Both date and time must be specified. The number of epochs must match the number of coordinates.

    Returns
    -------
    np.ndarray
        The input coordinates represented in the ECI frame.
    """
    ecef = np.atleast_1d(ecef)
    epoch = np.atleast_1d(epoch)
    r_z = r_ecef_to_eci(epoch)
    # express the rotation as a rotation matrix
    r_z = r_z.as_matrix()
    # r_z will have shape (N, 3, 3) and eci (3,) or (N, 3) so add a
    # singleton dimension to eci to allow broadcasting.
    return np.squeeze(r_z @ ecef[..., np.newaxis])


def r_ecef_to_eci(epoch: Union[datetime, Iterable[datetime]]) -> R:
    return r_eci_to_ecef(epoch).inv()


def find_tangent_normal_basis(r, w):
    """Find the tanget-normal vector basis given the position vector r [m], and the wave number vector w.

    The tangent normal basis is defined by the tangent plane to the point r on the WGS-84 ellipsoid and the normal vector to it. The function returns the basis vectors t⃗, v⃗ and n⃗ that define the tangent normal frame. t⃗ is in the direction of w projected on the tangent plane at r, v⃗ is on the tangent plane perpendicular to t⃗ and n⃗ is the unit normal vector of the plane.

    Parameters
    ----------
    r :npt.ArrayLike
        The position vector. Accepts both a 1D (of shape (3,)) array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    w : npt.ArrayLike
        The wavevector. Accepts both a 1D (of shape (3,)) array representing a wavevector and a 2D (N by 3) array of N wavevectors.

    Returns
    -------
    Tuple
        Return the three basis vectors that make up the tangent-normal basis. The first basis is t, the second is v, and the third is n.
    """
    r = np.atleast_1d(r)
    w = np.atleast_1d(w)
    x, y, z = r[..., 0], r[..., 1], r[..., 2]
    a_wgs84_sq = const.r_equatorial["wgs84"] ** 2
    b_wgs84_sq = const.r_polar["wgs84"] ** 2
    if x.ndim == 1:
        n = 2 * np.column_stack((x / a_wgs84_sq, y / a_wgs84_sq, z / b_wgs84_sq))
    else:
        n = 2 * np.dstack((x / a_wgs84_sq, y / a_wgs84_sq, z / b_wgs84_sq))
    n = n / np.linalg.norm(n, axis=-1, keepdims=True)
    # project vector w on the tangent plane with normal n
    t = w - np.sum(w * n, axis=-1, keepdims=True) * n
    t = t / np.linalg.norm(t, axis=-1, keepdims=True)
    # complete the right handed set
    v = np.cross(n, t)
    return (np.squeeze(t), np.squeeze(v), np.squeeze(n))


def ec_to_tangent_normal(r_ec, rs, w):
    """Convert a vector in an Earth-centred frame to a tangent normal frame defined by the position vector on the surface and the wavevector.

    Refer to the documentation of `find_tangent_normal_basis` for the definition of the tangent-normal frame.

    Parameters
    ----------
    r_ec : npt.ArrayLike
        The position vector in an Earth-centred frame. Accepts both a 1D (of shape (3,)) array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.

    rs : npt.ArrayLike
        The position vector of the point on the surface. Accepts both a 1D (of shape (3,)) array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    w : npt.ArrayLike
        The wavevector. Accepts both a 1D (of shape (3,)) array representing a wavevector and a 2D (N by 3) array of N wavevectors.

    Returns
    -------
    npt.ArrayLike
        Return r_ec converted to the tangent-normal frame
    """
    r_tn = np.zeros_like(r_ec)
    t, v, n = find_tangent_normal_basis(rs, w)
    r_tn[..., 0] = np.sum(r_ec * n, axis=-1)
    r_tn[..., 1] = np.sum(r_ec * t, axis=-1)
    r_tn[..., 2] = np.sum(r_ec * v, axis=-1)
    return r_tn


def unit_v(r):
    return r / np.linalg.norm(r, axis=-1, keepdims=True)


def temporal_and_spectral_shift(r_t1, r_t2, r_r1, r_r2, r_p, v_t1, v_r1, k0):
    """Compute the temporal and spectral shift of two acquisitions.

    The two acquisitions of a resolution cell located at `r_p` are done by two
    transmitters with position vectors `r_t1` and `r_t2` and two receivers `r_r1` and
    `r_r2`. This operation spectrally aligns the ground-projected wavenumber region of
    support of two SAR sensors and finds the temporal shift and wavenumber shift
    required to align the regions of support. All vectors should be given in the local
    tangent-normal frame at `r_p`. It is assumed that the first component of the vectors
    is normal to the tangent plane, the second is on the tangent plane along the range
    direction and the third is on the tangent plane perpendicular to the other two basis
    directions.

    Parameters
    ----------
    r_t1 : npt.ArrayLike
        The position vector of the first transmitter. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    r_t2 : npt.ArrayLike
        The position vector of the second transmitter. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    r_r1 : npt.ArrayLike
        The position vector of the first reciever. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    r_r2 : npt.ArrayLike
        The position vector of the second reciever. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    r_p : npt.ArrayLike
        The position vector of the resolution cell. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    v_t1 : npt.ArrayLike
        The velocity vector of the first transmitter. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    v_r1 : npt.ArrayLike
        The velocity vector of the first reciever. Accepts both a 1D (of shape (3,))
        array of one set of XYZ coordinates and a 2D (N by 3) array of N coordinates.
    k0: float
        The angular wavenumber of the carrier signal.

    Returns
    -------
    npt.ArrayLike
        Return an N by 2 array where the first element is the temporal shift [s] and the second the spectral shift [rad/m].
    """
    r_t1_p = -r_t1 + r_p
    r_r1_p = -r_r1 + r_p
    norm_l_t1 = np.linalg.norm(r_t1_p, axis=-1, keepdims=True)
    norm_l_r1 = np.linalg.norm(r_r1_p, axis=-1, keepdims=True)
    l_t1 = r_t1_p / norm_l_t1
    l_r1 = r_r1_p / norm_l_r1
    l_t2 = unit_v(-r_t2 + r_p)
    l_r2 = unit_v(-r_r2 + r_p)
    delta_l_t = l_t2 - l_t1
    delta_l_r = l_r2 - l_r1
    l_dot_t = (-v_t1 + np.sum(l_t1 * v_t1, axis=-1, keepdims=True) * l_t1) / norm_l_t1
    l_dot_r = (-v_r1 + np.sum(l_r1 * v_r1, axis=-1, keepdims=True) * l_r1) / norm_l_r1
    l_dot_total = l_dot_t + l_dot_r
    delta_l_total = delta_l_t + delta_l_r
    l_total = l_t1 + l_r1 + delta_l_total
    # For each resolution cell, at a given time, line of sight and
    # formation we have 2 by 2 matrix
    out_shape = np.broadcast_shapes(r_p.shape[0:-1], r_r2.shape[0:-1]) + (2, 2)
    A = np.zeros(out_shape)
    A[..., 0] = k0 * l_dot_total[..., 1:3]
    A[..., 1] = l_total[..., 1:3]
    b = -k0 * delta_l_total[..., 1:3]
    delta_t_delta_k = np.linalg.solve(A, b)
    return delta_t_delta_k


def sensitivity(
    r_t1, r_r1, r_r2, v_t1, v_r1, r_p, delta_t_delta_k, time, f_c, b_perp=False
):
    delta_t, delta_k = delta_t_delta_k[..., 0], delta_t_delta_k[..., 1]
    sp1 = compute_support(r_t1, r_r1, r_p, f_c)
    r_t1_p = -r_t1 + r_p
    r_r1_p = -r_r1 + r_p
    r_bi = unit_v(r_t1_p) + unit_v(r_r1_p)
    doppler_direction = -v_t1 / np.linalg.norm(
        r_t1_p, axis=-1, keepdims=True
    ) - v_r1 / np.linalg.norm(r_r1_p, axis=-1, keepdims=True)
    zeta = np.cross(r_bi, doppler_direction)
    zeta = unit_v(zeta)
    _, _, e_z = find_tangent_normal_basis(r_p, unit_v(r_r1_p))
    # Now we recalculate the position of the TX and the second receiver at the temporal
    # lag
    time_vec_shifted = time + delta_t
    spl = CubicSpline(time, r_t1, extrapolate=True)
    r_t1_shift = spl(time_vec_shifted)
    spl = CubicSpline(time, r_r2, extrapolate=True)
    r_r2_shift = spl(time_vec_shifted)
    delta_k = delta_t_delta_k[..., 1]
    f_shift = delta_k * sp_constants.c / (2 * np.pi)
    fr = f_c + f_shift
    sp2 = compute_support(r_t1_shift, r_r2_shift, r_p, fr[..., np.newaxis])
    delta_sp = sp1 - sp2
    # why is there not a nice way to take the dot product between rows of arrays in
    # numpy?
    sensitivity = np.sum(delta_sp * zeta, axis=-1) / (np.sum(zeta * e_z, axis=-1))
    if b_perp:
        delta_r = r_r2_shift - r_r1
        b_perp = np.sum(delta_r * zeta, axis=-1)
        res = np.stack((sensitivity, b_perp), axis=-1)
    else:
        res = sensitivity
    return res


def compute_support(r_c, r_d, r_p, fr):
    r_bi = unit_v(-r_c + r_p) + unit_v(-r_d + r_p)
    spectral_support = 2 * np.pi / sp_constants.c * fr * r_bi
    return spectral_support


def pt_get_intersection_ellipsoid(position, direction):
    """Calculate intercept point of antenna look direction with ellipsoid.


    Parameters
    ----------
    position : ndarray
        float 2-D array containing antenna origins (satellite's position) [m].
    direction : ndarray
          float 2-D array containing look directions of the antenna [deg].

    Returns
    -------
    ndarray
        float 2-D array giving the intercept point(s) with the
        ellipsoid [m].

    """
    # make valid for single position
    if position.ndim == 1:
        position = position.reshape((1, 3))
    if direction.ndim == 1:
        direction = direction.reshape((1, 1, 3))
    # Set some default values for earth ellipsoid
    r_x = const.r_equatorial["wgs84"]  # earth equatorial radius [m]
    r_y = const.r_equatorial["wgs84"]  # earth equatorial radius [m]
    r_z = const.r_polar["wgs84"]  # earth radius at pole [m]

    # Some initialization
    dir_shape = direction.shape

    # Map input arrays to vectors with short names
    # 1st vector is X direction, 2nd is Y and 3rd is Z

    pos_x = position[:, 0].reshape((dir_shape[0], 1))
    pos_y = position[:, 1].reshape((dir_shape[0], 1))
    pos_z = position[:, 2].reshape((dir_shape[0], 1))

    # Calculate coefficients of quadradic equation
    af = (
        (direction[:, :, 0] / r_x) ** 2
        + (direction[:, :, 1] / r_y) ** 2
        + (direction[:, :, 2] / r_z) ** 2
    )
    bf = 2.0 * (
        (direction[:, :, 0] / r_x) * (pos_x / r_x)
        + (direction[:, :, 1] / r_y) * (pos_y / r_y)
        + (direction[:, :, 2] / r_z) * (pos_z / r_z)
    )
    cf = (pos_x / r_x) ** 2 + (pos_y / r_y) ** 2 + (pos_z / r_z) ** 2 - 1.0

    # Check if solution of quadratic equation is real. Print informational
    # message if there would be one or many complex results.
    radicand = bf**2 - 4.0 * af * cf
    index_0 = np.where(radicand < 0.0)
    if radicand[index_0].size > 0:
        raise ValueError(
            "The Line-of-Sight vector does not point \
        toward the Earth. At some positions there is no intersection \
        with the ellipsoid. Please check your inputs."
        )

    # Solve quadratic equation to get intersection. Negative values of radicand
    # result in 'NaN'.
    solution_1 = (-bf + np.sqrt(radicand)) / (2.0 * af)
    solution_2 = (-bf - np.sqrt(radicand)) / (2.0 * af)

    # Negative solutions appear if there is an intersection in the
    # backward direction.
    # They are excluded by setting the solution to 'NaN'.
    # Set negative solutions to NaN before picking the minimum root as
    # the solution
    index_negative_1 = np.where(solution_1 < 0.0)
    index_negative_2 = np.where(solution_2 < 0.0)
    if solution_1[index_negative_1].size > 0:
        solution_1[index_negative_1] = np.nan
    if solution_2[index_negative_2].size > 0:
        solution_2[index_negative_2] = np.nan
    if (solution_1[index_negative_1].size + solution_2[index_negative_2].size) > 1.0:
        raise ValueError(
            "The Line-of-Sight vector does not point \
        toward the Earth. There are some intersections in the backward \
        direction. Please check your inputs."
        )

    # The smaller of the two solutions is the first intercept point
    jf = np.minimum(solution_1, solution_2)

    # Calculate coordinates of the intercept point
    target_x = jf * direction[:, :, 0] + pos_x
    target_y = jf * direction[:, :, 1] + pos_y
    target_z = jf * direction[:, :, 2] + pos_z
    intercept_point = np.zeros(dir_shape)
    intercept_point[:, :, 0] = target_x
    intercept_point[:, :, 1] = target_y
    intercept_point[:, :, 2] = target_z

    return intercept_point


def antenna_squinted_los(v_ver, r_ver, look_ang, squint_ang, right_looking=True):
    """Find LoS vector given a satellite coordinate system, a number
        of look angles, and a squint angle.

    Parameters
    ----------
    v_ver : ndarray
        (N, 3) array containing typically the flight direction
        (not if we mechanically rotate the antenna)
    r_ver : ndarray
        (N, 3) array with the radial (vertical) versor
    look_ang : float
        look angles [rad]
    squint_ang : float
        antenna squint [rad]
    right_looking : bool
         True if antenna is looking to the right. (Default value = True)

    Returns
    -------
    ndarray
        (N_t, N_l, 3) vector defining the line-of-sight of the antenna
        for each time instance and look angle. N_t is the number of
        time samples, and N_l the number of look angles.
    """
    n_ver = np.cross(v_ver, r_ver)
    # we assume that squint_ang has the same size as v_ver and r_ver
    Nv = v_ver.shape[0]
    Nla = look_ang.size
    if not right_looking:
        look_ang = -look_ang
    # phi, psi = np.meshgrid(look_ang, squint_ang, sparse=True)
    phi = look_ang
    psi = squint_ang
    v_ver_ = np.array([0, 1, 0]).reshape((3, 1, 1))
    r_ver_ = np.array([0, 0, 1]).reshape((3, 1, 1))
    n_ver_ = np.array([1, 0, 0]).reshape((3, 1, 1))
    # 3 x npts
    cos_psi = np.cos(psi)
    LoS_ = (
        v_ver_ * np.sin(psi)
        + n_ver_ * (cos_psi * np.sin(phi))
        - r_ver_ * (cos_psi * np.cos(phi))
    )
    LoS = (
        v_ver.reshape((Nv, 1, 3)) * LoS_[1, :].reshape((Nv, Nla, 1))
        + r_ver.reshape((Nv, 1, 3)) * LoS_[2, :].reshape((Nv, Nla, 1))
        + n_ver.reshape((Nv, 1, 3)) * LoS_[0, :].reshape((Nv, Nla, 1))
    )
    return LoS


def create_LoS(
    position,
    velocity,
    look_ang,
    squint_a=0,
    force_zero_Doppler=True,
    right_looking=True,
    yaw=0,
):
    """Find the LoS vector corresponding to a certain position and velocity
        vector, taking into consideration the look angle and squint

    Parameters
    ----------
    position : ndarray
        float 2-D array [N x 3] containing antenna origins
        (satellite's position) [m].
    velocity : ndarray
       float 2-D array [N x 3] containing velocity of the antenna
       [m/s].
    look_ang : float
        look angle [rad]
    squint_a : float
        antenna squint, defaults to zero [deg]
    force_zero_Doppler : bool
         force a zero doppler geometry. If True, the position unit
         vector is forced to be perpendicular to the velocity and
         normal unit vectors, thus forming a set of orthonormal
         vectors. (Default value = True)
    right_looking : bool
         (Default value = True)

    Returns
    -------
    ndarray
        float 3-D array containing the line-of-sight vector
    """

    Nla = look_ang.size
    ant_squint_rad = np.radians(squint_a)
    if velocity.ndim == 1:
        ax = 0
        Nv = 1
    else:
        ax = 1
        Nv = velocity.shape[0]

    # Calculate velocity and positions versor
    v_ver = velocity / np.linalg.norm(velocity, axis=ax).reshape((Nv, 1))
    r_ver = position / np.linalg.norm(position, axis=ax).reshape((Nv, 1))

    n_ver = np.cross(v_ver, r_ver)  # cross product of versors
    if force_zero_Doppler:
        r_ver2 = np.cross(n_ver, v_ver)
    else:
        r_ver2 = r_ver

    if np.isclose(ant_squint_rad, 0).all():
        if not right_looking:
            look_ang = -look_ang
        look_ang = look_ang.reshape(1, Nla, 1)
        yaw = np.atleast_1d(yaw)
        if np.isclose(yaw, 0).all():
            LoS = -np.cos(look_ang) * r_ver2.reshape(Nv, 1, 3) + np.sin(
                look_ang
            ) * n_ver.reshape(Nv, 1, 3)
        else:
            yaw = yaw[:, np.newaxis, np.newaxis]  # prepare yaw for broadcasting
            sin_look_ang = np.sin(look_ang)  # no need to compute it twice
            LoS = (
                -np.cos(look_ang) * r_ver2.reshape(Nv, 1, 3)
                + np.cos(yaw) * sin_look_ang * n_ver.reshape(Nv, 1, 3)
                + np.sin(yaw) * sin_look_ang * v_ver.reshape(Nv, 1, 3)
            )
    else:
        LoS = antenna_squinted_los(
            v_ver, r_ver2, look_ang, ant_squint_rad, right_looking=right_looking
        )
    return LoS


def antenna_axes(ant_x, ant_y):
    """Calculate principal axes of antenna.

    The x-axis is defined as the axis-orthogonal to the antenna, to be
    consistent with the x-axis = (ground) range convention. The antenna plane is
    y-z plane.

    Parameters
    ----------
    ant_x : ndarray
        (3,) np.array defining x axis
    ant_y : ndarray
        (3,) np.array defining y axis

    Returns
    -------
    ndarray
        array giving the axis of the antenna
    """
    # x for antenna pointing
    # y-z plane is antenna plane, z would be elevation cut, y azimuth
    if len(ant_x.shape) == 1:
        ant_y_n = ant_y / np.linalg.norm(ant_y)
        ant_x_n = ant_x / np.linalg.norm(ant_x)
        ant_z_n = np.cross(ant_x_n, ant_y_n)
    else:
        Npts = ant_y.shape[0]
        ant_y_n = ant_y / np.linalg.norm(ant_y, axis=1).reshape((Npts, 1))
        ant_x_n = ant_x / np.linalg.norm(ant_x, axis=1).reshape((Npts, 1))
        ant_z_n = np.cross(ant_x_n, ant_y_n)
    return (ant_x_n, ant_y_n, ant_z_n)


def companion_pointing(swpts, r_ecef, v_ecef, tilt=0):
    """Calculates mechanical pointing of a companion satellite to maximize
        the swath overlap, according to a number of assumptions :-)

    Parameters
    ----------
    swpts :
        Nl x 3 or Na x Nl x 3 array with points in center of
        reference footprint
    r_ecef :
        Na x 3 or 3-element array with spacecraft position
    v_ecef :
        Na x 3 or 3-element array with spacecraft velocity
    tilt :
        antenna tilt with respect to Nadir (Default value = 0)

    Returns
    -------
    type
        a named tuple with 'ant_xyz', 'sat_xyz', 'sat', 'euler_xyz',
        the xyz rotation matrices to antenna coordinates, the
        xyz rotation matrix for the spacecraft, the rotation matrix
        of for the satellite in satellite coordinates, and the
        corresponding Euler rotations, respectively

    """
    if swpts.ndim == 2:
        swpts = swpts.reshape((1,) + swpts.shape)
    if r_ecef.ndim == 1:
        r_ecef = r_ecef.reshape((1, 3))
        v_ecef = v_ecef.reshape((1, 3))
    s2r_near = swpts[:, 0, :] - r_ecef
    s2r_far = swpts[:, -1, :] - r_ecef
    Npts = r_ecef.shape[0]
    LoS_s_near = s2r_near / np.linalg.norm(s2r_near, axis=1).reshape((Npts, 1))
    LoS_s_far = s2r_far / np.linalg.norm(s2r_far, axis=1).reshape((Npts, 1))
    w = np.linspace(0, 1, swpts.shape[1]).reshape((1, swpts.shape[1], 1))
    LoS_s = (
        LoS_s_near.reshape((Npts, 1, 3)) * (1 - w) + LoS_s_far.reshape((Npts, 1, 3)) * w
    )
    # swpts_s = pt_get_intersection_ellipsoid(r_ecef, LoS_s)
    # This is to define a reference frame with respect to a zero-Doppler
    # aligned but elevation-tilted antenna. This is useful as one would typically
    # mount the antenna tilted and then rotate the companion satellite
    LoS_s_ZD = create_LoS(
        r_ecef, v_ecef, np.array([np.radians(tilt)]), force_zero_Doppler=True
    )
    SE_x_ref = LoS_s_ZD[:, 0, :]

    SE_y = np.cross(LoS_s_far, LoS_s_near)

    # Desired antenna axes
    SE_x_n, SE_y_n, SE_z_n = antenna_axes((LoS_s_far + LoS_s_near) / 2, SE_y)
    # ZD antenna axes
    SE_ref_x_n, SE_ref_y_n, SE_ref_z_n = antenna_axes(SE_x_ref / 2, v_ecef)
    # Satellite axes
    LoS_hor = create_LoS(
        r_ecef, v_ecef, np.array([np.pi / 2]), force_zero_Doppler=True
    ).reshape((Npts, 3))
    SE_sref_x_n, SE_sref_y_n, SE_sref_z_n = antenna_axes(LoS_hor, v_ecef)
    # This converts from coordinates in antenna coordinates to ecef
    # We create a n x 3 x 3 matrix
    # Each column (axis=1) contains a unit vector
    # so rot_SE \cdot tranpose([1,0,0]) would give the ECEF vector corresponding
    # to the x-axis
    rot_SE = ant2ecef = np.stack((SE_x_n, SE_y_n, SE_z_n), axis=2)
    # ZD antenna coordinates to ecef
    rot_ref_SE = rant2ecef = np.stack((SE_ref_x_n, SE_ref_y_n, SE_ref_z_n), axis=2)
    # sat coordinates to ecef
    sat_ref_SE = sat2ecef = np.stack((SE_sref_x_n, SE_sref_y_n, SE_sref_z_n), axis=2)
    # ant2ecef \cdot ecef2zd = ?
    # rot_xyz_sat =  np.einsum("ijk,ikl->ijl", ant2ecef, np.linalg.inv(rant2ecef))
    # PLD 2022/01/03 inverting this, since it seems wrong
    # ecef2zd \ cdot ant2ecef =  ant2zd
    # ant2rant = np.einsum("ijk,ikl->ijl", np.linalg.inv(rant2ecef), ant2ecef)
    # Required rotation of satellite in satellite coordinates
    # rot_sat = sat2rant^-1 \cdot rot_rant2ant \cdot sat2rant
    # ant2zd \cdot sat2ecef
    # In zd coordinates, required rotation
    rot_rant2ant = np.einsum("ijk,ikl->ijl", np.linalg.inv(rant2ecef), ant2ecef)
    # Now we need sat2zd
    sat2rant = np.einsum("ijk,ikl->ijl", np.linalg.inv(rant2ecef), sat2ecef)
    tmp = np.einsum("ijk,ikl->ijl", rot_rant2ant, sat2rant)
    rot_sat = np.einsum("ijk,ikl->ijl", np.linalg.inv(sat2rant), tmp)
    # PDL 2022/01/04 removed following three lines
    # tmp = np.einsum("ijk,ikl->ijl", rot_xyz_sat, sat2ecef)
    # ecef2sat \cdot ant2ecef \cdot ecef2zd \cdot sat2ecef
    # rot_sat = np.einsum("ijk,ikl->ijl", np.linalg.inv(sat2ecef), tmp)
    #    for u_ind in np.arange(0, r_m.shape[0], 100):
    #        LOS_m =
    rxyz = np.zeros((Npts, 3))
    for u_ind in range(r_ecef.shape[0]):
        rxyz[u_ind] = np.array(trans.euler_from_matrix(rot_sat[u_ind], axes="rxyz"))
        # PLD 2022/01/03
        # rxyz[u_ind] = np.array(trans.euler_from_matrix(ant2rant[u_ind], axes="rxyz"))
    companion_rot = namedtuple(
        "sar_rotations", ["ant_xyz", "sat_xyz", "sat", "euler_xyz"]
    )
    return companion_rot(rot_SE, sat_ref_SE, rot_sat, rxyz)


def geo_to_zero_doppler(lat, lon, alt, Single_orbData):
    """Finds the (closest) zero Doppler orbit location for a specific point in
    geographic coordinates (i.e. the distance vector and the orbit speed are
    orthogonal) and returns the orbit location coordinates and the look angle

    Parameters
    ----------
    lat :
        point latitude
    lon :
        point longitude
    alt :
        point altitude
    Single_orbData :
        object returned from SingleOrbit Class

    Returns
    -------
    type
        ecef coordinates of orbit location [x, y, z],
        platform speed vector at orbit location [vx, vy, vaz],
        time of orbit location
        look angle,
        look direction ('right' or 'left')

    """
    # point ecef coordinates
    coords_geo = np.array([[lat, lon, alt]])
    coords_ecef = geodetic_to_ecef(coords_geo)

    # Compute distances between point and orbit
    d = np.linalg.norm(Single_orbData.r_ecef - coords_ecef, axis=1)

    # Considers only orbit path closer to the point
    valid_orb = np.where(d < min(d) + 1e4)

    r_ecef = Single_orbData.r_ecef[valid_orb[0], :]
    v_ecef = Single_orbData.v_ecef[valid_orb[0], :]
    t_vec = Single_orbData.timevec[valid_orb[0]]

    # visual check
    if 0:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot(
            Single_orbData.r_ecef[:, 0],
            Single_orbData.r_ecef[:, 1],
            Single_orbData.r_ecef[:, 2],
        )
        ax.plot(
            r_ecef[:, 0],
            r_ecef[:, 1],
            r_ecef[:, 2],
            linestyle="None",
            marker="o",
        )

    # Compute look angle
    la = np.degrees(
        np.arccos(
            np.sum(r_ecef * (r_ecef - coords_ecef), axis=1)
            / (
                np.linalg.norm(r_ecef, axis=1)
                * np.linalg.norm(r_ecef - coords_ecef, axis=1)
            )
        )
    )

    # Compute azimuth angle
    az = np.degrees(
        np.arccos(
            np.sum(v_ecef * (r_ecef - coords_ecef), axis=1)
            / (
                np.linalg.norm(v_ecef, axis=1)
                * np.linalg.norm(r_ecef - coords_ecef, axis=1)
            )
        )
    )

    # Check that the azimuth angles are monotonous and that 90° is included in
    # the range
    if np.sum(np.diff(az) > 0) > 0 and np.sum(np.diff(az) > 0) < (len(az) - 1):
        print(az)
        raise ValueError("geo_to_zero_doppler: azimuth vector is not monotonous")
    if (min(az) > 90) or (max(az) < 90):
        raise ValueError("geo_to_zero_doppler: az vector range does not include 90")

    # Find the orbit location associated to the zero-doppler position
    az_interp = interpolate.interp1d(az, range(len(valid_orb[0])), kind="linear")
    la_interp = interpolate.interp1d(range(len(valid_orb[0])), la, kind="linear")
    t_interp = interpolate.interp1d(range(len(valid_orb[0])), t_vec, kind="linear")
    r_x_interp = interpolate.interp1d(
        range(len(valid_orb[0])), r_ecef[:, 0], kind="linear"
    )
    r_y_interp = interpolate.interp1d(
        range(len(valid_orb[0])), r_ecef[:, 1], kind="linear"
    )
    r_z_interp = interpolate.interp1d(
        range(len(valid_orb[0])), r_ecef[:, 2], kind="linear"
    )
    v_x_interp = interpolate.interp1d(
        range(len(valid_orb[0])), v_ecef[:, 0], kind="linear"
    )
    v_y_interp = interpolate.interp1d(
        range(len(valid_orb[0])), v_ecef[:, 1], kind="linear"
    )
    v_z_interp = interpolate.interp1d(
        range(len(valid_orb[0])), v_ecef[:, 2], kind="linear"
    )

    smp_index = az_interp(90)
    look_angle = np.asscalar(la_interp(smp_index))
    t_zero = np.asscalar(t_interp(smp_index))
    r_ecef_zero = np.array(
        [r_x_interp(smp_index), r_y_interp(smp_index), r_z_interp(smp_index)]
    )
    v_ecef_zero = np.array(
        [v_x_interp(smp_index), v_y_interp(smp_index), v_z_interp(smp_index)]
    )

    look_dir_cos = np.inner(np.cross(r_ecef_zero, coords_ecef), v_ecef_zero)
    look_dir = "right" if look_dir_cos > 0 else "left"

    return r_ecef_zero, v_ecef_zero, t_zero, look_angle, look_dir
