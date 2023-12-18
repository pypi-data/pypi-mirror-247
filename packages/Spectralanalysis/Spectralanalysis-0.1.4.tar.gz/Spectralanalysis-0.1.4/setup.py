from setuptools import setup, find_packages

setup(
    name="Spectralanalysis",
    version="0.1.4",
    author="Olivia Berreby",
    author_email="oliviaberreby@college.harvard.edu",
    description="A package for spectral analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://code.harvard.edu/CS107/team22_2023.git",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
