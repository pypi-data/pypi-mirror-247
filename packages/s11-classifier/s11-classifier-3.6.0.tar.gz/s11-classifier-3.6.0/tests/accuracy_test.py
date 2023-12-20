from unittest import TestCase

import numpy as np

from classifier.accuracy import get_confidence_map_from_random_forest_model

NOISE_FACTOR = 10

class MockTree:
    def predict(self, data):
        return (data + np.random.rand(*data.shape) * NOISE_FACTOR)[0]

class MockModel:
    estimators_ = [MockTree(), MockTree(), MockTree()]


class ConfidenceMapTestCase(TestCase):
    def setUp(self):
        # arrange
        self.test_function = get_confidence_map_from_random_forest_model
        self.array = np.array([
            [[10, 20, 30], [30, 40, 50]],
            [[50, 60, 70], [70, 80, 90]],
        ])

    def test_confidence_map_ok(self):
        # act
        result = self.test_function(
            MockModel(), self.array, confidence_level=0.95
        )
        # assert
        self.assertTrue(all(result.ravel() < 5))
        self.assertEqual(result.shape, self.array.shape[-2:])
