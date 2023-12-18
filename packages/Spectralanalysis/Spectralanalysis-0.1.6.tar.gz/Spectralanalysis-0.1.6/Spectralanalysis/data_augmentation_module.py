import pandas as pd
import numpy as np
from scipy.misc import derivative

class DataAugment:
    def compute_derivatives(self, data):
        """
        Computes the first-order derivatives of the spectral data.
        Args:
            data (pd.DataFrame): The spectral data.
        Returns:
            pd.DataFrame: First-order derivatives of the spectral data.
        """
        # Computing first-order derivatives
        derivative_data = data.apply(np.gradient, axis=0)
        derivative_data.columns = [f'{col}_derivative' for col in data.columns]
        return derivative_data

    def compute_fracderivatives(self, data, order=0.5):
        """
        Computes fractional derivatives of the spectral data.
        Args:
            data (pd.DataFrame): The spectral data.
            order (float): The order of the derivative (e.g., 0.5 for half-derivative).
        Returns:
            pd.DataFrame: Fractional derivatives of the spectral data.
        """
        # Define a function to compute fractional derivative for a single column
        def frac_derivative(column):
            x = np.linspace(0, len(column) - 1, len(column))
            return np.array([derivative(lambda t: np.interp(t, x, column), 
                                        xi, n=order, dx=1e-6) for xi in x])

        # Computing fractional derivatives
        frac_derivative_data = data.apply(frac_derivative)
        frac_derivative_data.columns = [f'{col}_frac_derivative' for col in data.columns]
        return frac_derivative_data

# Example usage
# da = DataAugment()
# data = pd.DataFrame(...)  # Replace with actual spectral data
# derivatives = da.compute_derivatives(data)
# frac_derivatives = da.compute_fracderivatives(data, order=0.5)
