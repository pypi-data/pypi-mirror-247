

import pytest
from unittest.mock import patch, MagicMock
from cs107_project.core_functionalities import CoreFunctionalities, MetaDataExtractor, DataPreprocessor, WavelengthAligner
from astropy.table import Table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astroML.datasets import fetch_sdss_spectrum
from scipy.stats import zscore
from scipy.interpolate import interp1d

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Sample data for testing
sample_spec_line_data = Table({
    'specObjId': [12345, 54321],
    'specLineID': [12345,12344],
    'ew': [1.5, 2.3]
})

# Updated sample data to include 'class'
# Updated sample data
sample_data = Table({
    'ra': [10.684, 20.123],
    'dec': [41.269, -10.123],
    'bestObjID': [12345, 54321],
    'elodieFeH': [-0.5, 0.2],  # Example values
    'elodieZ': [0.004, 0.003]   # Example values
})
sample_data2 = Table({
    'class': ['GALAXY','STAR','QSO']
})

sample_data3 = Table({
    'plate': [274, 274],
    'fiberID': [102, 102],
    'mjd': [51913, 51913],
    'class': ['GALAXY', 'STAR']
})


@pytest.fixture
def sample_query():
    return "SELECT top 10 ra, dec, plateID, fiberID, mjd, class, bestObjID FROM specObj WHERE class = 'galaxy' AND z > 0.5 AND zWarning = 0"


def test_core_functionalities_init(sample_query):
    # Testing initialization with only query
    cf = CoreFunctionalities(sample_query)
    assert cf.query == sample_query
    assert cf.data is None

    # Testing initialization with query and data
    cf = CoreFunctionalities(sample_query, sample_data)
    assert cf.data is sample_data


def test_core_functionalities_invalid_data_type(sample_query):
    with pytest.raises(ValueError):
        CoreFunctionalities(sample_query, "not a table")


def test_query_validation():
    with pytest.raises(ValueError):
        CoreFunctionalities.query_validation("invalid query")


@patch('cs107_project.core_functionalities.SDSS.query_sql')
def test_execute_query_success(mock_query_sql, sample_query):
    mock_query_sql.return_value = sample_data

    cf = CoreFunctionalities(sample_query)
    cf.execute_query()

    for col_name in sample_data.colnames:
        assert all(cf.data[col_name] == sample_data[col_name])



@patch('cs107_project.core_functionalities.SDSS.query_sql', side_effect=Exception("Query Error"))
def test_execute_query_failure(mock_query_sql, sample_query):
    cf = CoreFunctionalities(sample_query)
    with pytest.raises(Exception):
        cf.execute_query()


def test_metadata_extractor_init(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data)
    assert mde.query == sample_query
    assert mde.data is sample_data


def test_extract_identifiers_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_identifiers()


def test_extract_identifiers(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data)
    assert list(mde.extract_identifiers()) == [12345, 54321]


def test_extract_coordinates_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_coordinates()

def test_extract_coordinates(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data)
    coordinates = mde.extract_coordinates()
    assert list(coordinates['ra']) == [10.684, 20.123]
    assert list(coordinates['dec']) == [41.269, -10.123]

def test_extract_metallicity_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_metallicity()

def test_extract_metallicity(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data)
    metallicity = mde.extract_metallicity()
    assert list(metallicity) == [-0.5, 0.2]

def test_extract_redshifts_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_redshifts()

def test_extract_redshifts(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data)
    redshifts = mde.extract_redshifts()
    assert list(redshifts) == [0.004, 0.003]

def test_extract_class_type_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_class_type()

def test_extract_class_type(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data2)
    class_type = mde.extract_class_type()
    assert list(class_type) == ["GALAXY", "STAR", "QSO"]  # Replace with actual expected values

def test_extract_ml_data(sample_query):
    plate = 274
    fiber = 102
    mjd = 51913

    # Call your extract_ml_data function
    mde = MetaDataExtractor(sample_query, sample_data3)
    df = mde.extract_ml_data()

    # Check if df is a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check if 'Wavelength' and 'Flux' columns exist
    assert 'Wavelength' in df.columns
    assert 'Flux' in df.columns

    # Check if 'Wavelength' and 'Flux' columns have numeric data
    assert np.issubdtype(df['Wavelength'].dtype, np.number)
    assert np.issubdtype(df['Flux'].dtype, np.number)

@patch('cs107_project.core_functionalities.SDSS.query_sql')
def test_extract_ml_data_with_specObjID_success(mock_query_sql, sample_query):
    specObjID = 12345678
    mock_query_sql.return_value = sample_data3  # Assuming sample_data has the required columns

    mde = MetaDataExtractor(sample_query, sample_data3)
    df = mde.extract_ml_data(specObjID)

    assert isinstance(df, pd.DataFrame)
    assert 'Wavelength' in df.columns
    assert 'Flux' in df.columns
    assert 'Class' in df.columns


@patch('cs107_project.core_functionalities.SDSS.query_sql', return_value=None)
def test_extract_ml_data_with_specObjID_no_data(mock_query_sql, sample_query):
    specObjID = 12345678

    mde = MetaDataExtractor(sample_query, sample_data)
    with pytest.raises(ValueError):
        mde.extract_ml_data(specObjID)


@patch('cs107_project.core_functionalities.SDSS.query_sql', side_effect=Exception("Query Error"))
def test_extract_ml_data_with_specObjID_query_failure(mock_query_sql, sample_query):
    specObjID = 12345678

    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_ml_data(specObjID)


def test_extract_ml_data_without_specObjID(sample_query):
    mde = MetaDataExtractor(sample_query, sample_data3)
    df = mde.extract_ml_data()

    assert isinstance(df, pd.DataFrame)
    assert 'Wavelength' in df.columns
    assert 'Flux' in df.columns
    assert 'Class' in df.columns


def test_extract_ml_data_without_specObjID_no_data(sample_query):
    mde = MetaDataExtractor(sample_query)
    with pytest.raises(ValueError):
        mde.extract_ml_data()

@pytest.fixture
def real_data():
    # Instantiate MetaDataExtractor and use the extract_viz_data method
    mde = MetaDataExtractor("Your SQL Query Here")
    return mde.extract_viz_data(plate=274, fiber=102, mjd=51913)

@pytest.fixture
def preprocessor_instance():
    query = "SELECT top 10 ra, dec, plate, fiberID, mjd, class, specObjID FROM specObj WHERE class = 'galaxy' AND z > 0.5 AND zWarning = 0"
    data_extractor = MetaDataExtractor(query)
    data_extractor.execute_query()
    return DataPreprocessor(query, data_extractor.data)


def test_normalize_data(preprocessor_instance, real_data):
    # Normalize real flux data
    normalized_data = preprocessor_instance.normalize_data(real_data['Flux'])
    assert np.isclose(normalized_data.mean(), 0, atol=0.1)
    assert np.isclose(normalized_data.std(), 1, atol=0.1)

def test_remove_outliers(preprocessor_instance, real_data):
    original_z_scores = np.abs(zscore(real_data['Flux']))
    high_z_score_indices = np.where(original_z_scores >= 2.5)[0]

    cleaned_data = preprocessor_instance.remove_outliers(real_data['Flux'])
    cleaned_z_scores = np.abs(zscore(cleaned_data))
    
    assert not any(index in cleaned_data.index for index in high_z_score_indices)

def test_interpolate_data(preprocessor_instance, real_data):
    # Define new wavelengths for interpolation
    original_wavelengths = real_data['Wavelength']
    new_wavelengths = np.linspace(original_wavelengths.min(), original_wavelengths.max(), 1000)
    interpolated_data = preprocessor_instance.interpolate_data(real_data['Flux'], original_wavelengths, new_wavelengths)
    assert len(interpolated_data) == len(new_wavelengths)


def test_correct_redshift(preprocessor_instance, real_data):
    # Use a sample redshift value for testing
    redshift = 0.1
    corrected_data = preprocessor_instance.correct_redshift(real_data['Flux'], redshift)
    # Check if the data has been scaled down by the factor of 1 + redshift
    assert corrected_data.equals(real_data['Flux'] / (1 + redshift))


class TestWavelengthAligner:

    @pytest.fixture
    def aligner(self):
        # Create a WavelengthAligner instance for testing
        return WavelengthAligner(start_wavelength=3800, end_wavelength=9200, num_points=1000)

    @pytest.fixture
    def test_spectra(self):
        # Fetch real spectra data from SDSS
        mde1 = MetaDataExtractor("Your SQL Query Here")
        data1 = mde1.extract_viz_data(plate=274, fiber=102, mjd=51913)

        mde2 = MetaDataExtractor("Your SQL Query Here")
        data2 = mde2.extract_viz_data(plate=414, fiber=410, mjd=51869)

        spectra = [
            (data1['Wavelength'].values, data1['Flux'].values),
            (data2['Wavelength'].values, data2['Flux'].values)
        ]
        return spectra

    def test_align_spectrum(self, aligner, test_spectra):
        # Test aligning a single spectrum
        for original_wavelengths, original_flux in test_spectra:
            aligned_flux = aligner.align_spectrum(original_wavelengths, original_flux)
            assert len(aligned_flux) == 1000  # Number of points in the standard grid
            # Additional assertions can be added here

    def test_align_spectra(self, aligner, test_spectra):
        # Test aligning multiple spectra
        aligned_spectra = aligner.align_spectra(test_spectra)
        assert len(aligned_spectra) == len(test_spectra)
        for aligned_flux in aligned_spectra:
            assert len(aligned_flux) == 1000  # Each spectrum should have 1000 data points

if __name__ == "__main__":
    pytest.main()

