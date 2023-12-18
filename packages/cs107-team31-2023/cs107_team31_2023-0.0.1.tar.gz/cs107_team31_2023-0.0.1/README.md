# Astronomy Research Library

The Astronomy Research Library is a Python library designed to facilitate astronomical research, particularly focusing on the classification of stars, galaxies, and quasars (QSOs). It interfaces with Sloan Digital Sky Survey (SDSS) services to access spectral data and related information.

## Modules Overview

### Core Functionalities
This module provides tools to query the SDSS database and APIs using ADQL (Astronomical Data Query Language).

- **Classes & Functions**:
  - `CoreFunctionalities`: Constructs ADQL query strings and Handles HTTP requests and responses to/from SDSS services.
  - `MetaDataExtractor`: Extracts metadata from queried objects
  - 'DataPreprocessor': Responsible for preparing raw spectral data for analysis, including normalization, outlier removal, and interpolation, and RedshiftCorrection
  - 'Wavelength Aligner' - handles spectral alignment to a common wavelength range
  - `get_ml_data`: Extracts wavelength and flux data from SDSS for use in later modules



### Visualization
Offers visualization tools for spectral data using Matplotlib, with capabilities for overlaying inferred continua.

- **Classes & Functions**:
  - `Vizualization`: Provides functionalities to plot and overlay spectral features.

### Data Augmentation
Enhances the dataset by calculating derivatives and fractional derivatives of spectral data.

- **Classes & Functions**:
  - `data_augmentation`: Computes and appends derivatives to each spectral data point.

### Machine Learning
Implements a machine learning model for classifying astronomical objects.

- **Classes & Functions**:
  - `knn_clasifier`: A model that distinguishes between stars, galaxies, and QSOs.

### Cross Matching
Enables cross matching between SDSS and Gaia.

- **Classes & Functions**:
  - `extract_gaia_cross_match`: Facilitates the selection and analysis of pure matches between SDSS and Gaia.

### Spectral Feature Extraction
Extracts spectral features defining emission and absorption lines as those with flux
levels exceeding 2 sigma from the continuum

### Interactive Visualization
- **Classes & Functions**:
  - `viz_tool_interactive`: interactive visualization tool


# Workflow Status

[![Python application test with coverage](https://code.harvard.edu/CS107/team31_2023/actions/workflows/code_coverage.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team31_2023/actions/workflows/code_coverage.yml)
[![Run Tests](https://code.harvard.edu/CS107/team31_2023/actions/workflows/tests.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team31_2023/actions/workflows/tests.yml)

