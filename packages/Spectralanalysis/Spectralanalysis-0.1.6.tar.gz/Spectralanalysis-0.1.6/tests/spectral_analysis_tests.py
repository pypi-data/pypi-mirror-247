# TESTS
import pytest
from spectral_analysis import SpectralAnalysis

# Initialize the SpectralAnalysis instance
sa = SpectralAnalysis()

def test_compute_spectrum():
    """
    Tests the compute_spectrum method.
    """
    data = [1, 2, 3]
    expected_result = [2, 4, 6]
    assert sa.compute_spectrum(data) == expected_result, "compute_spectrum did not return the expected results"

def test_analyze_spectrum():
    """
    Tests the analyze_spectrum method.
    """
    spectrum = [2, 4, 6]
    analysis = sa.analyze_spectrum(spectrum)
    assert analysis["max"] == 6, "analyze_spectrum did not find the correct max value"
    assert analysis["min"] == 2, "analyze_spectrum did not find the correct min value"

def test_compute_spectrum_empty():
    """
    Test compute_spectrum with empty input.
    """
    data = []
    expected_result = []
    assert sa.compute_spectrum(data) == expected_result, "Empty compute_spectrum failed"

def test_compute_spectrum_negative():
    """
    Test compute_spectrum with negative values.
    """
    data = [-1, -2, -3]
    expected_result = [-2, -4, -6]
    assert sa.compute_spectrum(data) == expected_result, "Negative values compute_spectrum failed"

def test_analyze_spectrum_basic():
    """
    Test analyze_spectrum with basic input.
    """
    spectrum = [2, 4, 6]
    analysis = sa.analyze_spectrum(spectrum)
    assert analysis["max"] == 6, "Basic analyze_spectrum failed to find the correct max value"
    assert analysis["min"] == 2, "Basic analyze_spectrum failed to find the correct min value"

def test_analyze_spectrum_empty():
    """
    Test analyze_spectrum with empty input.
    """
    spectrum = []
    with pytest.raises(ValueError):
        _ = sa.analyze_spectrum(spectrum)

def test_analyze_spectrum_negative():
    """
    Test analyze_spectrum with negative values.
    """
    spectrum = [-2, -4, -6]
    analysis = sa.analyze_spectrum(spectrum)
    assert analysis["max"] == -2, "Negative values analyze_spectrum failed to find the correct max value"
    assert analysis["min"] == -6, "Negative values analyze_spectrum failed to find the correct min value"
