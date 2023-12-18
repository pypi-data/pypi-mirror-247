import unittest
import pandas as pd
import numpy as np
from scipy.fft import fft

# Import data
# from data_module import data


class data_processing:
    def clean_data(self, data):
        """
        Removes noise or irrelevant information from the data.
        Assumes data is a pandas DataFrame.
        """
        # Example: Remove columns with more than 50% missing values
        cleaned_data = data.dropna(axis=1, thresh=len(data) * 0.5)
        return cleaned_data

    def normalize_data(self, data):
        """
        Normalizes the data using Min-Max scaling.
        Assumes data is a pandas DataFrame.
        """
        normalized_data = (data - data.min()) / (data.max() - data.min())
        return normalized_data

    def transform_data(self, data, method):
        """
        Applies various transformations to the data.
        Currently supports: Fourier transform.
        Assumes data is a pandas DataFrame.
        """
        if method.lower() == "fourier":
            transformed_data = fft(data.values)
            return transformed_data
        else:
            raise NotImplementedError("Transformation method not supported.")
            
    def correct_redshift(self, data, wavelength_col, redshift):
        """
        Corrects the data for redshift.
        Assumes data has a column for wavelengths and a known redshift value.
        Args:
            data (pd.DataFrame): Spectral data.
            wavelength_col (str): The name of the column containing the wavelengths.
            redshift (float): The redshift value to correct for.
        Returns:
            pd.DataFrame: The redshift-corrected data.
        """
        if wavelength_col not in data.columns:
            raise ValueError(f"{wavelength_col} column not found in data")

        # Correcting for redshift
        # The formula used: observed_wavelength = emitted_wavelength * (1 + redshift)
        corrected_wavelengths = data[wavelength_col] / (1 + redshift)
        corrected_data = data.copy()
        corrected_data[wavelength_col] = corrected_wavelengths
        return corrected_data
    
    def align_spectra(self, spectra, wavelength_range):
        """
        Aligns all spectra to a predefined wavelength range.
        
        Args:
            spectra (list of pd.DataFrame): List of spectral data DataFrames.
            wavelength_range (np.array): Array of wavelengths for alignment.
        
        Returns:
            list of pd.DataFrame: Aligned spectral data.
        """
        aligned_spectra = []
        for spectrum in spectra:
            interp_func = interp1d(spectrum['wavelength'], spectrum['intensity'], 
                                   kind='linear', bounds_error=False, fill_value="extrapolate")
            aligned_intensity = interp_func(wavelength_range)
            aligned_spectrum = pd.DataFrame({'wavelength': wavelength_range, 
                                             'intensity': aligned_intensity})
            aligned_spectra.append(aligned_spectrum)
        return aligned_spectra
            
# Example usage
# dp = data_processing()
# cleaned = dp.clean_data(pd.DataFrame(...))
# normalized = dp.normalize_data(pd.DataFrame(...))
# transformed = dp.transform_data(pd.DataFrame(...), 'Fourier')
# redshift_corrected = dp.correct_redshift(pd.DataFrame(...), 'wavelength', 0.03)
# aligned_spectra = dp.align_spectra(list_of_spectral_dfs, np.linspace(start_wl, end_wl, num_points))
