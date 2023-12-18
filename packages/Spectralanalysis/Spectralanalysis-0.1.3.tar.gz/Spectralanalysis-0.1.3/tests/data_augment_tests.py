import unittest
import pandas as pd
import numpy as np
from data_augment import DataAugment

class TestDataAugment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up for testing DataAugment class.
        """
        cls.da = DataAugment()
        cls.test_data = pd.DataFrame({
            'spectrum1': np.linspace(0, 10, 100),
            'spectrum2': np.sin(np.linspace(0, 10, 100))
        })

    def test_compute_derivatives(self):
        """
        Test the compute_derivatives method.
        """
        derivative_data = self.da.compute_derivatives(self.test_data)
        self.assertIsInstance(derivative_data, pd.DataFrame)
        self.assertEqual(derivative_data.shape, self.test_data.shape)
        self.assertTrue(all(derivative_data.columns == ['spectrum1_derivative', 'spectrum2_derivative']))

    def test_compute_fracderivatives(self):
        """
        Test the compute_fracderivatives method.
        """
        frac_derivative_data = self.da.compute_fracderivatives(self.test_data, order=0.5)
        self.assertIsInstance(frac_derivative_data, pd.DataFrame)
        self.assertEqual(frac_derivative_data.shape, self.test_data.shape)
        self.assertTrue(all(frac_derivative_data.columns == ['spectrum1_frac_derivative', 'spectrum2_frac_derivative']))

    def test_compute_fracderivatives_invalid_order(self):
        """
        Test compute_fracderivatives with an invalid derivative order.
        """
        with self.assertRaises(ValueError):
            _ = self.da.compute_fracderivatives(self.test_data, order=-1)

if __name__ == '__main__':
    unittest.main()
