import os.path
import numpy as np
from numpy.testing import assert_allclose

from astropy.modeling.models import (Polynomial1D, Polynomial2D, Shift,
                                     Const1D, Mapping)
from gwcs import wcs
from gwcs.wcstools import grid_from_bounding_box

from ...datamodels import SlitModel
from ...transforms import models as transforms
from ...extract_2d.grisms import compute_wavelength_array

import pytest

from . import data
data_path = os.path.split(os.path.abspath(data.__file__))[0]


def create_slit(model, x0, y0, order):
    """ Create a SlitModel representing a grism slit."""
    ymin = 0
    xmin = 0
    # ymax = 58
    # xmax = 1323
    model = Mapping((0, 1, 0, 0, 0)) | (Shift(xmin) & Shift(ymin) &
                                        Const1D(x0) & Const1D(y0) & Const1D(order) )| model
    wcsobj = wcs.WCS([('det', model), ('world', None)])
    wcsobj.bounding_box = ((20, 25), (800, 805))
    slit = SlitModel()
    slit.meta.wcs = wcsobj
    slit.source_xpos = x0
    slit.source_ypos = y0
    return slit


def test_NIRCAMForwardRowGrismDispersion():
    xmodels = [Polynomial1D(1, c0=0.59115385, c1=0.00038615),
               Polynomial1D(1, c0=-0.16596154, c1=0.00019308)]
    ymodels = [Polynomial1D(1, c0=0., c1=0.), Polynomial1D(1, c0=0., c1=0.)]
    lmodels = [Polynomial1D(1, c0=2.4, c1=2.6), Polynomial1D(1, c0=2.4, c1=2.6)]
    model = transforms.NIRCAMForwardRowGrismDispersion([1, 2], lmodels, xmodels, ymodels)


    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(model, x0, y0, order)

    expected = np.array([[3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ],
                         [3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ],
                         [3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ],
                         [3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ],
                         [3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ],
                         [3.03973415, 3.04073814, 3.04174213, 3.04274612, 3.04375011, 3.0447541 ]])

    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    wavelength = compute_wavelength_array(slit) #x, y, np.zeros(x.shape)  +x0, np.zeros(y.shape)+y0, np.zeros(x.shape)+order)
    assert_allclose(wavelength, expected)

    with pytest.raises(ValueError):
        slit = create_slit(model, x0, y0, 3)
        compute_wavelength_array(slit)


def test_NIRCAMForwardColumnGrismDispersion():
    ymodels = [Polynomial1D(1, c0=0.5911538461431823, c1=0.000386153846153726),
               Polynomial1D(1, c0=-0.1659615384582264, c1=0.0001930769230768787)]

    xmodels = [Polynomial1D(1, c0=0., c1=0.), Polynomial1D(1, c0=0., c1=0.)]
    lmodels = [Polynomial1D(1, c0=2.4, c1=2.6), Polynomial1D(1, c0=2.4, c1=2.6)]
    model = transforms.NIRCAMForwardColumnGrismDispersion([1, 2], lmodels, xmodels, ymodels)


    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(model, x0, y0, order)
    expected = np.array([[4.724638, 4.724638, 4.724638, 4.724638, 4.724638, 4.724638],
                         [4.725642, 4.725642, 4.725642, 4.725642, 4.725642, 4.725642],
                         [4.726646, 4.726646, 4.726646, 4.726646, 4.726646, 4.726646],
                         [4.72765 , 4.72765 , 4.72765 , 4.72765 , 4.72765 , 4.72765 ],
                         [4.728654, 4.728654, 4.728654, 4.728654, 4.728654, 4.728654],
                         [4.729658, 4.729658, 4.729658, 4.729658, 4.729658, 4.729658]])

    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    wavelength = compute_wavelength_array(slit) #x, y, np.zeros(x.shape)  +x0, np.zeros(y.shape)+y0, np.zeros(x.shape)+order)
    assert_allclose(wavelength, expected)

    with pytest.raises(ValueError):
        slit = create_slit(model, x0, y0, 3)
        compute_wavelength_array(slit)


def test_NIRCAMBackwardDispersion():
    forward_ymodels = [Polynomial1D(1, c0=0.5911538461431823, c1=0.000386153846153726),
                       Polynomial1D(1, c0=-0.1659615384582264, c1=0.0001930769230768787)]

    forward_xmodels = [Polynomial1D(1, c0=0., c1=0.), Polynomial1D(1, c0=0., c1=0.)]
    forward_lmodels = [Polynomial1D(1, c0=2.4, c1=2.6), Polynomial1D(1, c0=2.4, c1=2.6)]

    forward_model = transforms.NIRCAMForwardColumnGrismDispersion([1, 2], forward_lmodels,
                                                                  forward_xmodels, forward_ymodels)


    ymodels = [Polynomial1D(1, c0=-1530.8764939967652, c1=2589.641434263754),
               Polynomial1D(1, c0=859.5617529710912, c1=5179.282868527087)]

    xmodels = [Polynomial1D(1, c0=0., c1=0.),
               Polynomial1D(1, c0=0., c1=0.)]
    lmodels = [Polynomial1D(1, c0=-0.923076923076923, c1=0.3846153846153846),
               Polynomial1D(1, c0=-0.923076923076923, c1=0.3846153846153846)]
    model = transforms.NIRCAMBackwardGrismDispersion([1, 2], lmodels, xmodels, ymodels)
    wavelength = np.array([[4.724638, 4.724638, 4.724638, 4.724638, 4.724638, 4.724638],
                           [4.725642, 4.725642, 4.725642, 4.725642, 4.725642, 4.725642],
                           [4.726646, 4.726646, 4.726646, 4.726646, 4.726646, 4.726646],
                           [4.72765 , 4.72765 , 4.72765 , 4.72765 , 4.72765 , 4.72765 ],
                           [4.728654, 4.728654, 4.728654, 4.728654, 4.728654, 4.728654],
                           [4.729658, 4.729658, 4.729658, 4.729658, 4.729658, 4.729658]])

    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(forward_model, x0, y0, order)

    expected_xdx = np.array([[20., 21., 22., 23., 24., 25.],
                             [20., 21., 22., 23., 24., 25.],
                             [20., 21., 22., 23., 24., 25.],
                             [20., 21., 22., 23., 24., 25.],
                             [20., 21., 22., 23., 24., 25.],
                             [20., 21., 22., 23., 24., 25.]])

    expected_ydy = np.array([[1584.50000003, 1584.50000003, 1584.50000003, 1584.50000003, 1584.50000003, 1584.50000003],
                             [1586.50000003, 1586.50000003, 1586.50000003, 1586.50000003, 1586.50000003, 1586.50000003],
                             [1588.50000003, 1588.50000003, 1588.50000003, 1588.50000003, 1588.50000003, 1588.50000003],
                             [1590.50000003, 1590.50000003, 1590.50000003, 1590.50000003, 1590.50000003, 1590.50000003],
                             [1592.50000003, 1592.50000003, 1592.50000003, 1592.50000003, 1592.50000003, 1592.50000003],
                             [1594.50000003, 1594.50000003, 1594.50000003, 1594.50000003, 1594.50000003, 1594.50000003]])
    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    xdx, ydy, _, _, _ = model(x, y, wavelength, np.zeros(x.shape) + order)
    assert_allclose(xdx, expected_xdx)
    assert_allclose(ydy, expected_ydy)


def test_NIRISSBackwardDispersion():
    forward_ymodels = [[Polynomial2D(2, c0_0=-1.876215, c1_0=-5.179793e-04, c2_0=2.116366e-08,
                                     c0_1=-2.259297e-04, c0_2=-2.502127e-12, c1_1=4.771951e-08),

                        Polynomial2D(2, c0_0=-3.089115, c1_0=3.063270e-03, c2_0=-9.786785e-07,
                                     c0_1=1.237905e-03, c0_2=-1.510774e-11, c1_1=-5.405480e-09)]]

    forward_xmodels = [[Polynomial2D(2, c0_0=63.55173, c1_0=3.846599e-06, c2_0=-7.173816e-10,
                                     c0_1=8.158127e-07, c0_2=-1.274281e-09, c1_1=4.098804e-11),

                        Polynomial2D(2, c0_0=-331.8532, c1_0=-1.24494e-05, c2_0=4.210112e-10,
                                     c0_1=-1.615311e-06, c0_2=6.665276e-09, c1_1=1.43762e-10)]]

    forward_lmodels = [Polynomial1D(1, c0=0.75, c1=1.55),
                       Polynomial1D(1, c0=0.75, c1=1.55)]

    forward_model = transforms.NIRISSForwardColumnGrismDispersion([1, 2], forward_lmodels,
                                                                  forward_xmodels, forward_ymodels)

    # NirissBackward model uses xmodels, ymodels and invlmodels
    lmodels = [Polynomial1D(1, c0=-0.48387097, c1=0.64516129),
               Polynomial1D(1, c0=-0.48387097, c1=0.64516129)
               ]

    model = transforms.NIRISSBackwardGrismDispersion([1, 2], lmodels=lmodels,
                                                     xmodels=forward_xmodels, ymodels=forward_ymodels)

    wavelength = np.array(
        [[2.3, 2.3, 2.3, 2.3, 2.3, 2.3, 2.3],
         [0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]])

    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(forward_model, x0, y0, order)
    slit.meta.wcs.bounding_box = ((910, 916), (12,18))

    expected_xdx = np.array(
        [[641.69045022, 642.69044108, 643.69043194, 644.6904228, 645.69041366, 646.69040451, 647.69039537],
       [923.12589407, 924.12589483, 925.1258956, 926.12589636, 927.12589712, 928.12589788, 929.12589864],
       [973.55464886, 974.55465141, 975.55465395, 976.55465648, 977.55465902, 978.55466155, 979.55466409],
       [973.55464968, 974.55465222, 975.55465476, 976.5546573, 977.55465984, 978.55466237, 979.5546649 ],
       [973.55465049, 974.55465304, 975.55465557, 976.55465811, 977.55466065, 978.55466318, 979.55466572],
       [973.55465131, 974.55465385, 975.55465639, 976.55465892, 977.55466146, 978.554664, 979.55466653],
       [973.55465211, 974.55465466, 975.55465719, 976.55465973, 977.55466227, 978.5546648 , 979.55466734]])



    expected_ydy = np.array(
        [[ 8.57057227, 8.57137444, 8.57217468, 8.57297302, 8.57376944, 8.57456394, 8.57535653],
         [10.5010401, 10.50075594, 10.50047152, 10.50018685, 10.49990193, 10.49961675, 10.49933131],
         [11.6673944, 11.66691562, 11.66643689, 11.66595821, 11.66547956, 11.66500096, 11.6645224],
         [12.66721189, 12.66673317, 12.66625449, 12.66577585, 12.66529725, 12.66481869, 12.66434018],
         [13.66702939, 13.66655071, 13.66607208, 13.66559348, 13.66511493, 13.66463643, 13.66415796],
         [14.66684688, 14.66636825, 14.66588967, 14.66541112, 14.66493262, 14.66445416, 14.66397574],
         [15.66666438, 15.6661858 , 15.66570726, 15.66522876, 15.66475031, 15.66427189, 15.66379352]])

    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    xdx, ydy, _, _, _ = model(x, y, wavelength, np.zeros(x.shape)+1)
    assert_allclose(xdx, expected_xdx)
    assert_allclose(ydy, expected_ydy)


def test_NIRISSForwardRowGrismDispersion():
    ymodels = [[Polynomial2D(2, c0_0=-1.876215, c1_0=-5.179793e-04, c2_0=2.116366e-08,
                             c0_1=-2.259297e-04, c0_2=-2.502127e-12, c1_1=4.771951e-08),

               Polynomial2D(2, c0_0=-3.089115, c1_0=3.063270e-03, c2_0=-9.786785e-07,
                            c0_1=1.237905e-03, c0_2=-1.510774e-11, c1_1=-5.405480e-09)]]

    xmodels = [[Polynomial2D(2, c0_0=63.55173, c1_0=3.846599e-06, c2_0=-7.173816e-10,
                             c0_1=8.158127e-07, c0_2=-1.274281e-09, c1_1=4.098804e-11),

               Polynomial2D(2, c0_0=-331.8532, c1_0=-1.24494e-05, c2_0=4.210112e-10,
                            c0_1=-1.615311e-06, c0_2=6.665276e-09, c1_1=1.43762e-10)]]

    lmodels = [Polynomial1D(1, c0=0.75, c1=1.55),
               Polynomial1D(1, c0=0.75, c1=1.55)]

    model = transforms.NIRISSForwardRowGrismDispersion([1, 2, 3, -1], lmodels, xmodels, ymodels)


    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(model, x0, y0, order)
    slit.meta.wcs.bounding_box = ((910, 916), (12, 18))

    wavelength = compute_wavelength_array(slit)
    expected = np.array(
        [[1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506],
         [1.06411857, 1.05944798, 1.0547774, 1.05010681, 1.04543623, 1.04076564, 1.03609506]])


    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    wavelength = compute_wavelength_array(slit)
    assert_allclose(wavelength, expected)


def test_NIRISSForwardColumnGrismDispersion():
    ymodels = [[Polynomial2D(2, c0_0=-1.876215, c1_0=-5.179793e-04, c2_0=2.116366e-08,
                             c0_1=-2.259297e-04, c0_2=-2.502127e-12, c1_1=4.771951e-08),

               Polynomial2D(2, c0_0=-3.089115, c1_0=3.063270e-03, c2_0=-9.786785e-07,
                            c0_1=1.237905e-03, c0_2=-1.510774e-11, c1_1=-5.405480e-09)]]

    xmodels = [[Polynomial2D(2, c0_0=63.55173, c1_0=3.846599e-06, c2_0=-7.173816e-10,
                             c0_1=8.158127e-07, c0_2=-1.274281e-09, c1_1=4.098804e-11),

               Polynomial2D(2, c0_0=-331.8532, c1_0=-1.24494e-05, c2_0=4.210112e-10,
                            c0_1=-1.615311e-06, c0_2=6.665276e-09, c1_1=1.43762e-10)]]

    lmodels = [Polynomial1D(1, c0=0.75, c1=1.55),
               Polynomial1D(1, c0=0.75, c1=1.55)]

    model = transforms.NIRISSForwardColumnGrismDispersion([1, 2, 3, -1], lmodels=lmodels,
                                                          xmodels=xmodels, ymodels=ymodels)


    x0 = 913.7
    y0 = 15.5
    order = 1

    slit = create_slit(model, x0, y0, order)
    slit.meta.wcs.bounding_box = ((910, 916), (12, 18))
    expected = np.array(
        [[2.3, 2.3, 2.3, 2.3, 2.3, 2.3, 2.3],
         [0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179, 0.98553179],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
         [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]])

    # refactored call
    x, y = grid_from_bounding_box(slit.meta.wcs.bounding_box)
    wavelength = compute_wavelength_array(slit)
    assert_allclose(wavelength, expected)


@pytest.mark.xfail
def test_compare_fits_gwcs():
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    from jwst.lib.catalog_utils import SkyObject
    from astropy import wcs
    from astropy.wcs.utils import skycoord_to_pixel
    from astropy.io import fits
    import asdf

    sk = SkyObject(sid=10, xcentroid=1942.42047611*u.pix, ycentroid=96.66721183*u.pix,
                 sky_centroid=SkyCoord(53.16349779, -27.81034994, unit=(u.deg, u.deg)),
                 abmag=93.81427764892578, abmag_error=5085.0444,
                 sky_bbox_ll=SkyCoord(53.16439778, -27.81106339, unit=(u.deg, u.deg)),
                 sky_bbox_lr=SkyCoord(53.1626226, -27.81107933, unit=(u.deg, u.deg)),
                 sky_bbox_ul=SkyCoord(53.16438104, -27.80960604, unit=(u.deg, u.deg)),
                 sky_bbox_ur=SkyCoord(53.16260589, -27.80962197, unit=(u.deg, u.deg)))

    lmin, lmax = (3.001085025, 4.302320901)
    order = 1

    fits_header = """
WCSAXES =                    2 / Number of coordinate axes
CRPIX1  =               1024.5 / Pixel coordinate of reference point
CRPIX2  =               1024.5 / Pixel coordinate of reference point
PC1_1   =     -0.9999988613384 / Coordinate transformation matrix element
PC1_2   =  -0.0015090798219302 / Coordinate transformation matrix element
PC2_1   =  -0.0015090798219302 / Coordinate transformation matrix element
PC2_2   =      0.9999988613384 / Coordinate transformation matrix element
CDELT1  =  1.7438002777778E-05 / [deg] Coordinate increment at reference point
CDELT2  =  1.7521186111111E-05 / [deg] Coordinate increment at reference point
CUNIT1  = 'deg'                / Units of coordinate increment and value
CUNIT2  = 'deg'                / Units of coordinate increment and value
CTYPE1  = 'RA---TAN'           / Right ascension, gnomonic projection
CTYPE2  = 'DEC--TAN'           / Declination, gnomonic projection
CRVAL1  =      53.161292774469 / [deg] Coordinate value at reference point
CRVAL2  =     -27.792691818741 / [deg] Coordinate value at reference point
LONPOLE =                180.0 / [deg] Native longitude of celestial pole
LATPOLE =     -27.792691818741 / [deg] Native latitude of celestial pole
MJDREFI =                  0.0 / [d] MJD of fiducial time, integer part
MJDREFF =                  0.0 / [d] MJD of fiducial time, fractional part
RADESYS = 'ICRS'               / Equatorial coordinate system
SPECSYS = 'BARYCENT'           / Reference frame of spectral coordinates
    """
    fits_wcs = wcs.WCS(fits.Header.fromstring(fits_header, sep='\n'))
    grism_wcs_file = os.path.join(data_path, "grism_wcs.asdf")
    fa = asdf.open(grism_wcs_file)

    grism_wcs = fa.tree['grism_wcs']
    detector_to_grism = grism_wcs.get_transform('detector', 'grism_detector')
    sky_to_grism = grism_wcs.backward_transform

    # translate the boxes using fits wcs
    dxmax, dymax = skycoord_to_pixel(sk.sky_bbox_ur,
                                     fits_wcs, origin=1)
    dxmin, dymin = skycoord_to_pixel(sk.sky_bbox_ll,
                                     fits_wcs, origin=1)

    # now translate through the grism transforms
    fxmin, fymin, _, _, _ = detector_to_grism(dxmin, dymin, lmin, order)
    fxmax, fymax, _, _, _ = detector_to_grism(dxmax, dymax, lmax, order)

    # Now use GWCS
    gxmax, gymax, _, _, _ = sky_to_grism(sk.sky_bbox_ll.ra.value,
                                         sk.sky_bbox_ll.dec.value,
                                         lmin, order)
    gxmin, gymin, _, _, _ = sky_to_grism(sk.sky_bbox_ur.ra.value,
                                         sk.sky_bbox_ur.dec.value,
                                         lmax, order)
    assert_allclose((fxmin, fxmax, fymin, fymax), (gxmin+1, gxmax+1, gymin+1, gymax+1))
