import sys
import numpy as np
import pandas as pd
import pytest
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from cs107_project.core_functionalities import MetaDataExtractor
from cs107_project.cross_match import extract_gaia_cross_match


label_map = {
    "STAR": 0,
    "GALAXY": 1,
    "QSO": 2
}

class TestCrossMatch:
    @staticmethod
    def execute_core_functions(name):
        tool = MetaDataExtractor(query=None)
        df = tool.extract_ml_data(name)
        wavelen = df["Wavelength"].tolist()
        flux = df["Flux"].tolist()
        Class = df["Class"].tolist()
        X = np.array([wavelen, flux]).T
        y = np.array(df["Class"].values)
        y_int = np.array([label_map[y_i] for y_i in y])
        return X, y_int

    def test_extract_gaia_cross_match(self):
        coords = {
            'ra': [10.0, 20.0, 30.0],
            'dec': [40.0, 50.0, 60.0]
        }
        radius = 1.0
        result = extract_gaia_cross_match(coords, radius)
        assert isinstance(result, pd.DataFrame)

    def test_extract_gaia_cross_match_empty_coords(self):
        coords = {}
        radius = 1.0
        with pytest.raises(Exception):
            extract_gaia_cross_match(coords, radius)

    def test_extract_gaia_cross_match_invalid_radius(self):
        coords = {
            'ra': [10.0, 20.0, 30.0],
            'dec': [40.0, 50.0, 60.0]
        }
        radius = -1.0
        with pytest.raises(ValueError):
            extract_gaia_cross_match(coords, radius)


if __name__ == "__main__":
    pytest.main(['-v', __file__])