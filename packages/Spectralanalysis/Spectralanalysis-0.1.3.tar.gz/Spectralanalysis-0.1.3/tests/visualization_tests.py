import unittest
import pandas as pd
import numpy as np
from visualization import Visualization

class TestVisualization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up for testing Visualization class.
        """
        cls.viz = Visualization()
        # Creating sample spectrum data
        cls.sample_spectrum = pd.Series(np.random.rand(100))
        cls.multiple_spectra = {
            'spectrum1': pd.Series(np.random.rand(100)),
            'spectrum2': pd.Series(np.random.rand(100))
        }

    def test_plot_spectrum(self):
        """
        Test the plot_spectrum method.
        """
        try:
            self.viz.plot_spectrum(self.sample_spectrum)
        except Exception as e:
            self.fail(f"plot_spectrum method failed with an exception: {e}")

    def test_visualize_comparison(self):
        """
        Test the visualize_comparison method.
        """
        try:
            self.viz.visualize_comparison(self.multiple_spectra)
        except Exception as e:
            self.fail(f"visualize_comparison method failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
