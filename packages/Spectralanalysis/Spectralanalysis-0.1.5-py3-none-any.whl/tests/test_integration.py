# This file designs integration tests so that we can verify the interactions between different modules of our application.

import unittest
import spectralysis as sp
import pandas as pd
import os

class TestSpectralysisIntegration(unittest.TestCase):
    """
    Integration tests for the Spectralysis library.
    """
    
    def setUp(self):
        """
        Set up any necessary data or configurations before each test.
        Ensures sample data is available and properly loaded.
        """
        self.sample_data_path = 'path/to/sample_data.csv'
        self.assertTrue(os.path.exists(self.sample_data_path), "Sample data file does not exist at specified path")
        self.sample_data = pd.read_csv(self.sample_data_path)

    def test_data_loading_and_preprocessing(self):
        """
        Test the integration of data loading and preprocessing modules.
        Verifies that data is loaded correctly and preprocessing is applied as expected.
        """
        data = sp.load_data(self.sample_data_path)
        preprocessed_data = sp.preprocess_data(data)
        
        self.assertIsNotNone(data, "Data should not be None after loading")
        self.assertIsNotNone(preprocessed_data, "Preprocessed data should not be None")
        # Example specific assertion (modify as needed)
        self.assertEqual(preprocessed_data.shape, data.shape, "Preprocessed data should have the same shape as original")

    def test_preprocessing_and_analysis(self):
        """
        Test the integration between preprocessing and spectral analysis modules.
        Ensures that preprocessing results are suitable for analysis.
        """
        preprocessed_data = sp.preprocess_data(self.sample_data)
        spectrum = sp.compute_spectrum(preprocessed_data)

        self.assertIsNotNone(spectrum, "Spectrum should not be None after computation")
        # Example specific assertion (modify as needed)
        self.assertTrue(spectrum.isnumeric(), "Spectrum should contain numeric values")

    def test_full_workflow(self):
        """
        Test the full workflow from data loading to visualization.
        This test simulates the typical user workflow.
        """
        data = sp.load_data(self.sample_data_path)
        preprocessed_data = sp.preprocess_data(data)
        spectrum = sp.compute_spectrum(preprocessed_data)
        analysis_result = sp.analyze_spectrum(spectrum)

        self.assertIsNotNone(analysis_result, "Analysis result should not be None")
        # Check if the function runs without errors
        try:
            sp.plot_spectrum(spectrum)
        except Exception as e:
            self.fail(f"Visualization failed with an exception: {e}")

    def test_empty_data_handling(self):
        """
        Test how the system handles empty data inputs.
        This is an edge case test.
        """
        empty_data = pd.DataFrame()
        with self.assertRaises(ValueError):
            sp.preprocess_data(empty_data)

if __name__ == '__main__':
    unittest.main()

# To run the tests, use the command:

# python -m unittest test_integration.py
