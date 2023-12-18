# Module: Data Input/Output

import pandas as pd
import unittest
import os

class DataIO:
    def load_data(self, format, filepath):
        """
        Loads spectral data from a file.
        Args:
            format (str): The file format (e.g., 'csv').
            filepath (str): The path to the file.
        Returns:
            pd.DataFrame: Loaded data.
        Raises:
            FileNotFoundError: If the file is not found.
            ValueError: If the file format is unsupported.
            IOError: For other I/O related errors.
        """
        format = format.lower()
        if format == "csv":
            try:
                return pd.read_csv(filepath)
            except FileNotFoundError:
                raise FileNotFoundError("File not found.")
            except Exception as e:
                raise IOError(f"Error loading data: {e}")
        else:
            raise ValueError("Unsupported file format.")

    def save_data(self, data, format, filepath):
        """
        Saves spectral data to a file.
        Args:
            data (pd.DataFrame): The spectral data to be saved.
            format (str): The file format (e.g., 'csv').
            filepath (str): The destination file path.
        Raises:
            ValueError: If the file format is unsupported or data is not a DataFrame.
            IOError: For other I/O related errors.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")

        format = format.lower()
        if format == "csv":
            try:
                data.to_csv(filepath, index=False)
            except Exception as e:
                raise IOError(f"Error saving data: {e}")
        else:
            raise ValueError("Unsupported file format.")
