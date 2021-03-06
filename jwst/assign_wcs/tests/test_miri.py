"""
Test MIRI MRS WCS transformation against IDT team data.

"""
from __future__ import absolute_import, division, unicode_literals, print_function
import os
import shutil
import tempfile
import numpy as np
from numpy.testing import utils
import pytest
from gwcs import wcs

from jwst.datamodels import ImageModel
from jwst.assign_wcs.tools.miri import miri_ifu_ref_tools
from jwst.assign_wcs import miri
from jwst.assign_wcs import AssignWcsStep


mrs_ref_data = {
    '1A': {'x': np.array([28.310396, 475.02154, 493.9777, 41.282537, 58.998266]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([11, 1, 1, 21, 21]),
           'alpha': np.array([0, -1.66946, 1.65180, -1.70573, 1.70244]),
           'beta': np.array([0, -1.77210, -1.77210, 1.77210, 1.77210]),
           'lam': np.array([5.34437, 4.86642, 4.95325,  5.65296, 5.74349]),
           'v2': np.array([-8.39424,  -8.41746, -8.36306, -8.42653, -8.37026]),
           'v3': np.array([-2.48763, -2.52081, -2.51311, -2.46269, -2.45395]),
           },
    '1B': {'x': np.array([28.648221, 475.07259, 493.98157,41.559386, 59.738296]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([11, 1, 1, 21, 21]),
           'alpha': np.array([0., -1.70796, 1.60161, -1.70854, 1.78261]),
           'beta': np.array([0., -1.77204, -1.77204, 1.77204, 1.77204]),
           'lam': np.array([6.17572, 5.62345, 5.72380, 6.53231, 6.63698]),
           'v2': np.array([-8.39426, -8.41808, -8.36368, -8.42682, -8.36899]),
           'v3': np.array([-2.48492, -2.51808, -2.51040, -2.46001, -2.45126])
           },
    '1C': {'x': np.array([30.461871, 477.23742, 495.96228, 43.905314, 60.995683]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([11, 1, 1, 21, 21]),
           'alpha': np.array([0., -1.60587, 1.67276, -1.60766, 1.68720]),
           'beta': np.array([0., -1.77202, -1.77202, 1.77202, 1.77202]),
           'lam': np.array([7.04951, 6.42424, 6.53753, 7.45360, 7.57167]),
           'v2': np.array([-8.39357, -8.41570, -8.36165, -8.42457, -8.36996]),
           'v3': np.array([-2.48987, -2.52271, -2.51525, -2.46467, -2.45649])
           },
    '2A': {'x': np.array([992.158, 545.38386, 525.76143, 969.29711, 944.19303]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([9, 1, 1, 17, 17]),
           'alpha': np.array([0., -2.11250, 2.10676, -2.17239, 2.10447]),
           'beta': np.array([0., -2.23775, -2.23775, 2.23775, 2.23775]),
           'lam': np.array([8.20797, 7.52144, 7.64907, 8.68677, 8.83051]),
           'v2': np.array([-8.39393, -8.42259, -8.35355, -8.43583, -8.36499]),
           'v3': np.array([-2.48181, -2.52375, -2.51357, -2.44987, -2.44022])
           },
    '2B': {'x': np.array([988.39977, 541.23447, 521.60207, 964.91753, 990.10325]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([9, 1, 1, 17, 17]),
           'alpha': np.array([0., -2.10593, 2.10015, -2.08817, 2.10422]),
           'beta': np.array([0., -2.23781, -2.23781, 2.23781, 2.23781]),
           'lam': np.array([9.44205, 8.65341, 8.79991, 9.99257, 10.15795]),
           'v2': np.array([-8.39645, -8.42502, -8.35603, -8.43716, -8.36742]),
           'v3': np.array([-2.47773, -2.51972, -2.50938, -2.44554, -2.43626])
           },
    '2C': {'x': np.array([990.89693, 543.82344, 524.34514, 967.98318, 942.77564]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([9, 1, 1, 17, 17]),
           'alpha': np.array([0., -2.07490, 2.11234, -2.14704, 2.14196]),
           'beta': np.array([0., -2.23778, -2.23778, 2.23778, 2.23778]),
           'lam': np.array([10.90225, 9.99162, 10.16079, 11.53780, 11.72887]),
           'v2': np.array([-8.39303, -8.42129, -8.35221, -8.43454, -8.36352]),
           'v3': np.array([-2.47869, -2.52052, -2.51036, -2.44668, -2.43712])
           },
    '3A': {'x': np.array([574.80828, 1001.0602, 984.6387, 547.27479, 518.89992]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([8, 1, 1, 16, 16]),
           'alpha': np.array([0., -2.86745, 3.20982, -3.01230, 2.96643]),
           'beta': np.array([-0.19491, -2.92360, -2.92360, 2.92360, 2.92360]),
           'lam': np.array([12.5335, 13.49968, 13.33846, 11.77148, 11.52350]),
           'v2': np.array([-8.40590, -844849, -834906, -8.46070, -8.36174]),
           'v3': np.array([-2.48992, -2.54104, -2.52854, -2.44547, -2.43112])
           },
    '3B': {'x': np.array([574.26012, 1001.7349,985.30166, 548.016, 519.98]),
           'y': np.array([512., 1., 100, 900, 1014]),
           's': np.array([8, 10, 1, 16,  16]),
           'alpha':np.array([0, -3.17728, 2.92434, -3.29402, 2.60797]),
           'beta': np.array([-0.19491, -2.92360, -2.92360, 2.92360, 2.92360]),
           'lam': np.array([14.53997, 15.66039, 15.47355, 13.65622, 13.36833]),
           'v2': np.array([-8.40044, -8.44785, -8.34786, -8.46088, -8.36211]),
           'v3': np.array([-2.48588, -2.53771, -2.52512, -2.44219, -2.42776])
           },
    '3C': {'x': np.array([573.25446, 1000.21721, 983.92918, 546.00285, 518.2782]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([8, 1, 1, 16, 16]),
           'alpha': np.array([0., -2.94573, 3.09057, -3.07810, 2.73161]),
           'beta': np.array([-0.19491, -2.92360, -2.93360, 2.92360, 2.92360]),
           'lam': np.array([16.79017, 18.08441, 17.86845, 15.76948, 15.43724]),
           'v2': np.array([-8.40205, -8.44574, -8.34664, -8.45859, -8.36196]),
           'v3': np.array([-2.48627, -2.53761, -2.52502, -2.44221, -2.42787]),
           },
    '4A': {'x': np.array([80.987181, 434.34987, 461.90855, 26.322503, 53.674656]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([6, 1, 1, 12, 12]),
           'alpha': np.array([0., -3.74625, 3.72621, -3.94261, 3.62762]),
           'beta': np.array([-0.32802, -3.60821, -3.60821, 3.60821, 3.60821]),
           'lam': np.array([19.34914, 20.93078, 20.6464, 18.07975, 17.67221]),
           'v2': np.array([-8.38446, -8.43506, -8.31378, -8.46256, -8.33609]),
           'v3': np.array([-2.48058, -2.5444, -2.52426, -2.42449, -2.40839])
           },
    '4B': {'x': np.array([77.62553, 431.57061, 458.86869, 23.559111, 50.632416]),
           'y': np.array([512., 10, 100, 900, 1014]),
           's': np.array([6, 1, 1, 12, 12]),
           'alpha': np.array([0., -3.54817, 3.73313, -3.73558, 3.74096]),
           'beta': np.array([-0.32802, -3.60821, -3.60821, 3.60821, 3.60821]),
           'lam': np.array([22.38267, 24.21212, 23.88327, 20.91426, 20.44279]),
           'v2': np.array([-8.38581, -8.43443, -8.3141, -8.46152, -833604]),
           'v3': np.array([-2.48185, -2.54526, -2.52568, -2.42513, -2.40959])
           },
    '4C': {'x': np.array([79.662059, 433.73384, 460.75026, 25.820431, 52.412219]),
           'y': np.array([512., 10, 100, 900, 104]),
           's': np.array([6, 1, 1, 12, 12]),
           'alpha': np.array([0., -3.61682, 3.69713, -3.66259, 3.69888]),
           'beta': np.array([-0.32802, -3.60819, -3.60819, 3.60819, 3.60819]),
           'lam': np.array([26.18343, 28.32354, 27.93894, 24.46574, 23.91417]),
           'v2': np.array([-8.38603, -8.43509, -8.31524, -8.45888, -8.33707]),
           'v3': np.array([-2.48315, -2.54647, -2.52661, -2.42721, -2.41060])
           }
}


channel_band = [('MIRIFUSHORT', '12', 'SHORT'),
                ('MIRIFUSHORT', '12', 'MEDIUM'),
                ('MIRIFUSHORT', '12', 'LONG'),
                ('MIRIFULONG',  '34', 'SHORT'),
                ('MIRIFULONG',  '34', 'MEDIUM'),
                ('MIRIFULONG',  '34', 'LONG'),
                ]


band_mapping = {'SHORT': 'A', 'MEDIUM': 'B', 'LONG': 'C'}


refs = {'distortion': '',
        'regions': '',
        'specwcs': '',
        'v2v3': '',
        'wavelengthrange': ''
        }

build6_temporary_references_root = "/user/dencheva/build_6_references/miri-mrs"

def test_miri_mrs_1A():
    #ref = {}
    ref = {'distortion': '',
           'regions': '',
           'specwcs': '',
           'v2v3': '',
           'wavelengthrange': ''
           }
    im = ImageModel()
    im.meta.instrument.name = 'MIRI'
    im.meta.instrument.detector = 'MIRIFUSHORT'
    im.meta.instrument.channel = '12'
    im.meta.instrument.band = 'SHORT'
    im.meta.exposure.type = 'MIR_MRS'
    step = AssignWcsStep()
    for reftype in refs:
        ref[reftype] = step.get_reference_file(im, reftype)

    pipeline = miri.create_pipeline(im, ref)
    wcsobj = wcs.WCS(pipeline)

    for ch in im.meta.instrument.channel:
        ref_data = mrs_ref_data[ch + band_mapping[im.meta.instrument.band]]
        #ref_data = mrs_ref_data[im.meta.instrument.channel + band_mapping[im.meta.instrument.band]]
        #x = np.trunc(ref_data['x']).astype(np.int)
        #y = np.trunc(ref_data['y']).astype(np.int)
        for i, s in enumerate(ref_data['s']):
            sl = int(ch) * 100 + s
            detector_to_alpha_beta = wcsobj.get_transform('detector', 'alpha_beta')
            alpha, beta, lam = detector_to_alpha_beta.set_input(sl)(ref_data['x'][i], ref_data['y'][i])
            ##xan, yan, lam = wcsobj.forward_transform.set_input(sl)(ref_data['x'][i], ref_data['y'][i])
            utils.assert_allclose(alpha, ref_data['alpha'][i], atol=10**-5)
            utils.assert_allclose(beta, ref_data['beta'][i], atol=10**-5)
            utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
            detector_to_xan_yan = wcsobj.get_transform('detector', 'Xan_Yan')
            xan, yan, lam = wcsobj(ref_data['x'], ref_data['y'])
            utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
            utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
            utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)

    #for i, s in enumerate(ref_data['s']):
        #sl = int(ch) * 100 + s
        #xan, yan, lam = wcsobj.forward_transform(ref_data['x'][i], ref_data['y'][i])
        #utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
        #utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
        #utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
        #xin, yin = wcsobj.backward_transform(ref_data['v2'][i], ref_data['v3'][i], ref_data['lam'][i])
        #utils.assert_allclose(xin, ref_data['x'][i], atol=10**-5)
        #utils.assert_allclose(y, ref_data['y'][i], atol=10**-5)


def test_miri_mrs_1B():
    ref = {}

    im = ImageModel()
    im.meta.instrument.name = 'MIRI'
    im.meta.instrument.detector = 'MIRIFUSHORT'
    im.meta.instrument.channel = '12'
    im.meta.instrument.band = 'MEDIUM'
    im.meta.exposure.type = 'MIR_MRS'
    step = AssignWcsStep()
    for reftype in refs:
        ref[reftype] = step.get_reference_file(im, reftype)

    pipeline = miri.create_pipeline(im, ref)
    wcsobj = wcs.WCS(pipeline)

    for ch in im.meta.instrument.channel:
        ref_data = mrs_ref_data[ch + band_mapping[im.meta.instrument.band]]
    for i, s in enumerate(ref_data['s']):
        sl = int(ch) * 100 + s
        xan, yan, lam = wcsobj.forward_transform.set_input(sl)(ref_data['x'][i], ref_data['y'][i])
        utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
        utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
        utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
    for i, s in enumerate(ref_data['s']):
        sl = int(ch) * 100 + s
        xan, yan, lam = wcsobj.forward_transform(ref_data['x'][i], ref_data['y'][i])
        utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
        utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
        utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
        xin, yin = wcsobj.backward_transform(ref_data['v2'][i], ref_data['v3'][i], ref_data['lam'][i])
        utils.assert_allclose(xin, ref_data['x'][i], atol=10**-5)
        utils.assert_allclose(y, ref_data['y'][i], atol=10**-5)


def test_miri_mrs_1C():
    ref = {}

    im = ImageModel()
    im.meta.instrument.name = 'MIRI'
    im.meta.instrument.detector = 'MIRIFUSHORT'
    im.meta.instrument.channel = '12'
    im.meta.instrument.band = 'LONG'
    im.meta.exposure.type = 'MIR_MRS'
    step = AssignWcsStep()
    for reftype in refs:
        ref[reftype] = step.get_reference_file(im, reftype)

    pipeline = miri.create_pipeline(im, ref)
    wcsobj = wcs.WCS(pipeline)

    for ch in im.meta.instrument.channel:
        ref_data = mrs_ref_data[ch + band_mapping[im.meta.instrument.band]]
    for i, s in enumerate(ref_data['s']):
        sl = int(ch) * 100 + s
        xan, yan, lam = wcsobj.forward_transform.set_input(sl)(ref_data['x'][i], ref_data['y'][i])
        utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
        utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
        utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
    for i, s in enumerate(ref_data['s']):
        sl = int(ch) * 100 + s
        xan, yan, lam = wcsobj.forward_transform(ref_data['x'][i], ref_data['y'][i])
        utils.assert_allclose(xan, ref_data['v2'][i], atol=10**-5)
        utils.assert_allclose(yan, ref_data['v3'][i], atol=10**-5)
        utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
        xin, yin = wcsobj.backward_transform(ref_data['v2'][i], ref_data['v3'][i], ref_data['lam'][i])
        utils.assert_allclose(xin, ref_data['x'][i], atol=10**-5)
        utils.assert_allclose(y, ref_data['y'][i], atol=10**-5)

#@pytest.mark.parametrize(('detector', 'channel', 'band'), channel_band)
#def test_miri_mrs(detector, channel, band):
    #ref = {'distortion': '',
           #'regions': '',
           #'specwcs': '',
           #'v2v3': '',
           #'wavelengthrange': ''}

    #band_mapping = {'SHORT': 'A', 'MEDIUM': 'B', 'LONG': 'C'}
    #im = ImageModel()
    #im.meta.instrument.name = 'MIRI'
    #im.meta.instrument.detector = detector
    #im.meta.instrument.channel = channel
    #im.meta.instrument.band = band
    #im.meta.exposure.type = 'MIR_MRS'
    #step = AssignWcsStep()
    #for reftype in ref:
        #ref[reftype] = step.get_reference_file(im, reftype)

    #pipeline = miri.create_pipeline(im, ref)
    #wcsobj = wcs.WCS(pipeline)

    #for ch in channel:
        #ref_data = mrs_ref_data[ch + band_mapping[band]]
    #for i, s in enumerate(ref_data['s']):
        #sl = int(ch) * 100 + s
        #v2, v3, lam = wcsobj.forward_transform.set_input(sl)(ref_data['x'][i], ref_data['y'][i])
        #utils.assert_allclose(v2, ref_data['v2'][i], atol=10**-5)
        #utils.assert_allclose(v3, ref_data['v3'][i], atol=10**-5)
        #utils.assert_allclose(lam, ref_data['lam'][i], atol=10**-5)
