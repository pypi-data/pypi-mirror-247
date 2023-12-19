import unittest
from datetime import datetime

import numpy as np
from astropy.time import Time
import scipy.constants as sp_constants

import drama.geo.geometry as d_geo
from drama.constants import r_polar, r_equatorial


class TestECI(unittest.TestCase):
    def test_eci_to_ecef(self):
        # Test values from Matlab documentation on eci2ecef
        t0_utc = datetime(2019, 1, 4, 12)
        # t0_utc = Time(t0_utc, format="datetime", scale="utc")
        # epoch = t0_utc.jd
        eci = [-2981784, 5207055, 3161595]
        ecef = d_geo.eci_to_ecef(eci, t0_utc)
        np.testing.assert_allclose(ecef, [-5.7627e6, -1.6827e6, 3.1560e6], rtol=0.02)

    def test_eci_to_ecef2(self):
        """
        Notes
        -----
        Test scenario taken from Vallado_[1] Example 3-15: Performing IAU-76/FK5 reduction.
        The example shows that for
        UTC epoch = April 6, 2004, 07:51:28.386009

        References
        ----------
        ..[1] Vallado, D. A.; McClain, W. D. Fundamentals of Astrodynamics and Applications, 4th ed.; Space Technology Library; Microcosm Press: Hawthorne, CA, 2013.
        """
        t0_utc = datetime(2004, 4, 6, 7, 51, 28)
        eci = [5102.50895790e3, 6123.01140070e3, 6378.13692820e3]
        ecef = d_geo.eci_to_ecef(eci, t0_utc)
        np.testing.assert_allclose(
            ecef, [-1033.4793830e3, 7901.2952754e3, 6380.3565958e3], rtol=0.02
        )

    def test_eci_to_ecef_array(self):
        to_utc = np.array((datetime(2019, 1, 4, 12), datetime(2004, 4, 6, 7, 51, 28)))
        eci = np.array(
            [
                (-2981784, 5207055, 3161595),
                (5102.50895790e3, 6123.01140070e3, 6378.13692820e3),
            ]
        )
        expected = np.array(
            [
                (-5.7627e6, -1.6827e6, 3.1560e6),
                (-1033.4793830e3, 7901.2952754e3, 6380.3565958e3),
            ]
        )
        ecef = d_geo.eci_to_ecef(eci, to_utc)
        np.testing.assert_allclose(ecef, expected, rtol=0.02)


class TestECEF(unittest.TestCase):
    def test_ecef_to_geodetic(self):
        ecef = np.array([4201, 172.46, 4780.1]) * 1e3
        expected_llh = np.array([48.8562, 2.3508, 0.0674e3])
        llh = d_geo.ecef_to_geodetic(ecef)
        np.testing.assert_allclose(llh, expected_llh, rtol=1e3)

    def test_ecef_to_geodetic2(self):
        ecef = np.array([6524.834, 6862.875, 6448.296]) * 1e3
        expected_llh = np.array([34.352496, 46.4464, 5085.22e3])
        llh = d_geo.ecef_to_geodetic(ecef)
        np.testing.assert_allclose(llh, expected_llh, rtol=1e3)

    def test_ecef_to_geodetic_array(self):
        ecef_1 = np.array([4201, 172.46, 4780.1]) * 1e3
        ecef_2 = np.array([6524.834, 6862.875, 6448.296]) * 1e3
        ecef = np.array([ecef_1, ecef_2])
        llh_1 = np.array([48.8562, 2.3508, 0.0674e3])
        llh_2 = np.array([34.352496, 46.4464, 5085.22e3])
        expected_llh = np.array([llh_1, llh_2])
        llh = d_geo.ecef_to_geodetic(ecef)
        np.testing.assert_allclose(llh, expected_llh, rtol=1e3)

    def test_ecef_to_geodetic_north_pole(self):
        r0 = r_equatorial["wgs84"]
        z = r0 + 10
        llh = d_geo.ecef_to_geodetic(np.array([0, 0, z]))
        expected_llh = np.array([90, 0, z - r_polar["wgs84"]])
        np.testing.assert_allclose(llh, expected_llh, rtol=1e-5)

    def test_ecef_to_geodetic_south_pole(self):
        r0 = r_equatorial["wgs84"]
        z = -r0 + 10
        llh = d_geo.ecef_to_geodetic(np.array([0, 0, z]))
        expected_llh = np.array([-90, 0, -z - r_polar["wgs84"]])
        np.testing.assert_allclose(llh, expected_llh, rtol=1e-5)

    def test_ecef_to_eci(self):
        # Test values from Matlab documentation on ecef2eci
        t0_utc = datetime(2019, 1, 4, 12)
        ecef = np.array([-5762640, -1682738, 3156028])
        expected_eci = (
            np.array([-3.0096805185984354, 5.194367153197111, 3.156028]) * 1e6
        )
        eci = d_geo.ecef_to_eci(ecef, t0_utc)
        np.testing.assert_allclose(eci, expected_eci, rtol=1e-3)


class TestTangentNormalConversion(unittest.TestCase):
    def test_find_tangent_normal_basis(self):
        r = np.array([-993382.7506101627, -763509.8241467009, -6.232900768555447e6])
        w = np.array([-0.2447238746586203, -0.18376316149629157, 0.9520196036053877])
        expected_t = np.array([-0.78180129, -0.59198796, 0.19579835])
        expected_v = np.array([-0.60389191, 0.79706503, -0.00138188])
        expected_n = np.array([-0.15524596, -0.1193214, -0.9806432])
        t, v, n = d_geo.find_tangent_normal_basis(r, w)
        np.testing.assert_allclose(t, expected_t, atol=1e-8)
        np.testing.assert_allclose(v, expected_v, atol=1e-8)
        np.testing.assert_allclose(n, expected_n, atol=1e-8)

    def test_broadcasting(self):
        r = np.array(
            [
                [-993382.7506101627, -763509.8241467009, -6.232900768555447e6],
                [-1.0060022130299454e6, -773261.2421226028, -6.229695366323533e6],
            ]
        )
        w = np.array(
            [
                [-0.2447238746586203, -0.18376316149629157, 0.9520196036053877],
                [-0.4825923595120959, 0.13440317039210423, 0.8654712024839988],
            ]
        )
        expected_t = np.array(
            [
                [-0.78180129, -0.59198796, 0.19579835],
                [-0.98657639, 0.06359028, 0.15041043],
            ]
        )
        expected_v = np.array(
            [
                [-0.60389191, 0.79706503, -0.00138188],
                [0.04415105, 0.99063241, -0.12922114],
            ]
        )
        expected_n = np.array(
            [
                [-0.15524596, -0.1193214, -0.9806432],
                [-0.15721866, -0.12084575, -0.98014213],
            ]
        )
        t, v, n = d_geo.find_tangent_normal_basis(r, w)
        np.testing.assert_allclose(t, expected_t, atol=1e-8)
        np.testing.assert_allclose(v, expected_v, atol=1e-8)
        np.testing.assert_allclose(n, expected_n, atol=1e-8)


class TestTemporalAndSpectralShift(unittest.TestCase):
    def test_with_vectors(self):
        r_s1 = np.array([7.061499706109255e6, -383721.9098312183, 2026.019742999808])
        r_h1 = np.array([7.052907109477044e6, -384199.7730604316, -347871.2026890115])
        r_h2 = np.array([7.053051718818049e6, -384207.66154170793, -347878.3378482498])
        v_s1 = np.array([-2.6026908011483556, -4.674117845586608, 7580.507319191023])
        v_h1 = np.array([373.3230562034925, 0.16532665268261507, 7571.26158559659])
        r_p = np.array([6.357623970960754e6, 8217.480989297153, 2026.0197429997497])
        k0 = 2 * np.pi * 5.405e9 / sp_constants.c
        expected_delta_t_delta_k = np.array(
            [-0.0014226157295881882, 0.006754767828725657]
        )
        delta_t_delta_k = d_geo.temporal_and_spectral_shift(
            r_s1, r_s1, r_h1, r_h2, r_p, v_s1, v_h1, k0
        )
        np.testing.assert_allclose(delta_t_delta_k, expected_delta_t_delta_k)


if __name__ == "__main__":
    unittest.main()
