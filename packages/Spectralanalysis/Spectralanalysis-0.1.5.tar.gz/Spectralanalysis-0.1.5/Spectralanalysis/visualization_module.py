import matplotlib.pyplot as plt

class Visualization:
    def plot_spectrum(self, spectrum):
        """
        Creates an interactive plot of a single spectrum.
        Args:
            spectrum (pd.Series): Spectral data to plot.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(spectrum, label='Spectrum')
        plt.xlabel('Wavelength')
        plt.ylabel('Intensity')
        plt.title('Spectral Data')
        plt.legend()
        plt.show()

    def visualize_comparison(self, spectra):
        """
        Compares multiple spectra through interactive visualizations.
        Args:
            spectra (dict): Dictionary of spectral data to compare.
                            Keys are labels, values are pd.Series of data.
        """
        plt.figure(figsize=(10, 6))
        for label, spectrum in spectra.items():
            plt.plot(spectrum, label=label)
        plt.xlabel('Wavelength')
        plt.ylabel('Intensity')
        plt.title('Comparison of Spectral Data')
        plt.legend()
        plt.show()

# Example usage
# viz = Visualization()
# viz.plot_spectrum(pd.Series(...))  # Replace with actual spectral data
# spectra = {
#     'spectrum1': pd.Series(...),  # Replace with actual spectral data
#     'spectrum2': pd.Series(...)   # Replace with actual spectral data
# }
# viz.visualize_comparison(spectra)
