import os

import numpy as np
import matplotlib

if os.environ.get('DISPLAY', '') == '':
    print('No DISPLAY found. Using non-interactive "Agg"backend.')
    matplotlib.use('Agg')
from matplotlib import pyplot as plt  # noqa

import pytest  # noqa

from roipoly import RoiPoly  # noqa


@pytest.fixture()
def roi1():
    roi1_properties = {
        'x': [1, 1, 3, 3],
        'y': [1, 3, 3, 1]
    }
    fig = plt.figure()
    roi1 = RoiPoly(color='r', fig=fig, show_fig=False)
    roi1.x = roi1_properties['x']
    roi1.y = roi1_properties['y']
    return roi1


@pytest.fixture()
def img1():
    return np.ones((5, 5)) * range(5)


@pytest.fixture()
def roi1_expected_mask():
    return np.array(
        [[False, False, False, False, False],
         [False, False, False, False, False],
         [False, True, True, True, False],
         [False, True, True, True, False],
         [False, False, False, False, False]]
    )


def test_get_mask(roi1, img1, roi1_expected_mask):
    result = roi1.get_mask(img1)
    np.testing.assert_array_equal(result, roi1_expected_mask)


def test_get_mean_and_std(roi1, img1, roi1_expected_mask):
    mean, std = roi1.get_mean_and_std(img1)
    masked_img = img1.copy()
    masked_img[~roi1_expected_mask] = np.nan
    expected_mean = np.nanmean(masked_img)
    expected_std = np.nanstd(masked_img)
    np.testing.assert_almost_equal(mean, expected_mean)
    np.testing.assert_almost_equal(std, expected_std)
