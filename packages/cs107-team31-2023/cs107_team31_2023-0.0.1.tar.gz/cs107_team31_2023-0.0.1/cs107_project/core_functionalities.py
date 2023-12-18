#!/usr/bin/env python3

# File       : core_functionalities.py
# Description: Core functionalities module for spectral data analysis
# License    : MIT License
# Copyright 2023 Harvard University. All Rights Reserved.
import sys
print(sys.path)
import pandas as pd
from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
import numpy as np
import matplotlib.pyplot as plt
import astroML
import os 
import requests
from astroML.datasets import fetch_sdss_spectrum
from scipy.stats import zscore
from scipy.interpolate import interp1d



class CoreFunctionalities:

    def __init__(self, query, data=None):
        """
        Initializes the base class for spectral analysis.

        Args:
            query (str): ADQL query string for the SDSS database.
            data (astropy.table.Table, optional): Spectral data as an Astropy Table object. Defaults to None.
        """
        self.query = query

        if data is not None and not isinstance(data, Table):
            raise ValueError("Provided data should be in Astropy Table format.")

        self.data = data

    @staticmethod
    def query_validation(query: str):
        if 'select' not in query.lower() or 'from' not in query.lower():
            raise ValueError("Provided query does not meet the basic format requirements.")

    def execute_query(self):
        """
        Executes the SQL query on the SDSS database.
        """
        try:
            self.query_validation(self.query)
            result = SDSS.query_sql(self.query)
            self.data = Table(result)
        except (RemoteServiceError, TimeoutError, ValueError) as e:
            print(f"Failed to execute query: {e}")
        except RequestException as e:
            print(f"Network or request error: {e}")
        else:
            print("Query successfully executed; results are now available.")

    def download_fits(self, obj_id, target_dir='fits_files'):
        """
        Downloads the FITS file for a given object identifier.

        Args:
            obj_id (str): The object identifier for which the FITS file will be downloaded.
            target_dir (str): Directory to save the downloaded FITS file.
        """
        fits_url = self.construct_fits_url(obj_id)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        try:
            response = requests.get(fits_url)
            response.raise_for_status()
            file_path = os.path.join(target_dir, f"{obj_id}.fits")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"FITS file for obj_id {obj_id} downloaded successfully.")
            return file_path
        except requests.exceptions.RequestException as e:
            print(f"Error downloading FITS file: {e}")

    @staticmethod
    def construct_fits_url(obj_id):
        # Construct the URL based on the object ID. This is a placeholder.
        # The actual URL construction will depend on the database's API.
        base_url = "https://example.com/sdss/fits/"
        return f"{base_url}{obj_id}.fits"
    
class MetaDataExtractor(CoreFunctionalities):

    def __init__(self, query, data=None):
        """
        Initializes MetadataExtractor class.
        """
        super().__init__(query, data)

    def extract_identifiers(self):
        """
        Extracts identifiers from the data.
        """
        if self.data is None:
            raise ValueError("Data is unavailable for identifier extraction.")

        identifiers = self.data['bestObjID']
        return identifiers

    def extract_coordinates(self):
        """
        Extracts coordinates from the data.
        """
        if self.data is None:
            raise ValueError("Data is unavailable for coordinate extraction.")

        coordinates = self.data['ra', 'dec']
        return coordinates

    def extract_metallicity(self):
        """
        Extracts metallicity data.
        """
        if self.data is None:
            raise ValueError("Data is unavailable for metallicity extraction.")

        metallicity = self.data['elodieFeH']
        return metallicity

    def extract_redshifts(self):
        """
        Extracts redshift values.
        """
        if self.data is None:
            raise ValueError("Data is unavailable for redshift extraction.")

        redshifts = self.data['elodieZ']
        return redshifts
    
    def extract_class_type(self):
            if self.data is None:
                raise ValueError("Data is unavailable for class extraction.")
            class_info = self.data['class']
            return class_info
    
    def extract_ml_data(self, specObjID=None):

        if specObjID is not None:
        # If specObjID is provided, requery the data for this specific ID
            query = f"SELECT plate, fiberID, mjd, class FROM specObj WHERE specObjID = {specObjID}"
            try:
                result = SDSS.query_sql(query)
                if result is None or len(result) == 0:
                    raise ValueError(f"No data found for specObjID {specObjID}")
                data = Table(result)
            except Exception as e:
                raise ValueError(f"Failed to execute query for specObjID {specObjID}: {e}")
        elif self.data is None:
            raise ValueError("Initial data is unavailable for ML data extraction.")
        else:
            data = self.data

        # Initialize an empty DataFrame for the results
        ml_data = pd.DataFrame()

        # Iterate over each row in the data
        for row in data:
            plate, fiber, mjd = row['plate'], row['fiberID'], row['mjd']
            class_info = row['class']

            # Fetch the spectrum using the identifiers
            spec = fetch_sdss_spectrum(plate=plate, fiber=fiber, mjd=mjd)

            # Extract wavelength and flux
            wavelength = spec.wavelength()
            flux = spec.spectrum

            # Append to the DataFrame
            temp_df = pd.DataFrame({
                'Class': [class_info] * len(wavelength),  # Repeat the class info for each wavelength entry
                'Wavelength': wavelength,
                'Flux': flux
            })
            ml_data = pd.concat([ml_data, temp_df])
        print(dir(spec))    
        return ml_data

    @staticmethod
    def extract_viz_data(plate=None, fiber=None, mjd=None):
        plate = 274
        fiber = 102
        mjd = 51913
        spec = fetch_sdss_spectrum(plate=plate, fiber=fiber, mjd=mjd)
        print(dir(spec))
        print(spec.hdulist)
        
        wavelength = spec.wavelength()
        flux = spec.spectrum

        df = pd.DataFrame({
        'Wavelength': wavelength,
        'Flux': flux
        })
        return df
        
"""
def fetch_features(id, id, id, feature_names: list ):
    ## give me a pandas dataframe that contains the features in feature_names
    ## data = get_sdss()
    df = pd.DataFrame({
        n: data.n for n in feature_names
    })
    return df
"""

class DataPreprocessor(MetaDataExtractor):
    def __init__(self, query, data=None):
        super().__init__(query, data)

    def preprocess_data(self, specObjID):
        # Extract the necessary data
        ml_data = self.extract_ml_data(specObjID)

        # Perform preprocessing steps
        ml_data = self.normalize_data(ml_data)
        ml_data = self.remove_outliers(ml_data)
        ml_data = self.interpolate_data(ml_data, new_wavelengths)
        ml_data = self.correct_redshift(ml_data)

        return ml_data

    def normalize_data(self, data):
        data_float64 = data.astype(np.float64)  # Convert to float64
        normalized_data = (data_float64 - np.mean(data_float64)) / np.std(data_float64)
        return normalized_data


    def remove_outliers(self, data, threshold=2.5):
        z_scores = np.abs(zscore(data))
        return data[z_scores < threshold]


    def interpolate_data(self, flux_data, original_wavelengths, new_wavelengths):
        if len(original_wavelengths) != len(flux_data):
            raise ValueError("Length of original wavelengths does not match length of flux data")

        interp_function = interp1d(original_wavelengths, flux_data, kind='cubic', fill_value="extrapolate", bounds_error=False)
        interpolated_values = interp_function(new_wavelengths)
        return interpolated_values

    def correct_redshift(self, data, redshift):
        # Correct for redshift
        corrected_data = data / (1 + redshift)
        return corrected_data    


class WavelengthAligner:
    def __init__(self, start_wavelength, end_wavelength, num_points):
        """
        Initializes the WavelengthAligner with a standard wavelength grid.

        Args:
            start_wavelength (float): The starting wavelength.
            end_wavelength (float): The ending wavelength.
            num_points (int): The number of points in the grid.
        """
        self.standard_wavelengths = np.linspace(start_wavelength, end_wavelength, num_points)

    def align_spectrum(self, original_wavelengths, original_flux):
        """
        Aligns a single spectrum to the standard wavelength grid.

        Args:
            original_wavelengths (np.array): The original wavelengths of the spectrum.
            original_flux (np.array): The original flux values of the spectrum.

        Returns:
            np.array: Aligned flux values.
        """
        interpolate = interp1d(original_wavelengths, original_flux, kind='linear', bounds_error=False, fill_value=np.nan)
        aligned_flux = interpolate(self.standard_wavelengths)
        return aligned_flux

    def align_spectra(self, spectra):
        """
        Aligns multiple spectra to the standard wavelength grid.

        Args:
            spectra (list): A list of tuples, where each tuple contains original wavelengths and flux values for a spectrum.

        Returns:
            list: A list of aligned flux arrays.
        """
        aligned_spectra = []
        for wavelengths, flux in spectra:
            aligned_flux = self.align_spectrum(wavelengths, flux)
            aligned_spectra.append(aligned_flux)
        return aligned_spectra
    
def main():
    query = "SELECT top 10 ra, dec, plate, fiberID, mjd, class, specObjID FROM specObj WHERE class = 'galaxy' AND z > 0.5 AND zWarning = 0"
    analysis_instance = MetaDataExtractor(query)
    analysis_instance.execute_query()
    print(analysis_instance.extract_coordinates())
    print(analysis_instance.extract_ml_data(1059619742102349824))
    # Uncomment the following line if you have implemented the extract_equivalent_widths method
    

if __name__ == "__main__":
    main()