import unittest

import numpy as np
from matplotlib import pyplot as plt

from roipoly import RoiPoly


class TestRoiPoly(unittest.TestCase):

    def setUp(self):
        roi1_properties = {
            'x': [1, 1, 3, 3],
            'y': [1, 3, 3, 1]
        }
        fig = plt.figure()
        roi1 = RoiPoly(color='r', fig=fig, show_fig=False)
        roi1.x = roi1_properties['x']
        roi1.y = roi1_properties['y']
        self.roi1 = roi1
        self.img1 = np.ones((5, 5)) * range(5)
        self.roi1_expected_mask = np.array(
            [[False, False, False, False, False],
             [False, False, False, False, False],
             [False, True, True, True, False],
             [False, True, True, True, False],
             [False, False, False, False, False]])

    def test_get_mask(self):
        result = self.roi1.get_mask(self.img1)
        np.testing.assert_array_equal(result, self.roi1_expected_mask)

    def test_get_mean_and_std(self):
        mean, std = self.roi1.get_mean_and_std(self.img1)
        masked_img = self.img1.copy()
        masked_img[~self.roi1_expected_mask] = np.nan
        expected_mean = np.nanmean(masked_img)
        expected_std = np.nanstd(masked_img)
        np.testing.assert_almost_equal(mean, expected_mean)
        np.testing.assert_almost_equal(std, expected_std)
