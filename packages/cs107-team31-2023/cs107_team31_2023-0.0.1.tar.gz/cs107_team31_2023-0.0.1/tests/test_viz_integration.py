from cs107_project.visualization import viz_tool
from cs107_project.core_functionalities import MetaDataExtractor
import numpy as np
import pytest
import os 

class Test_viz_integration:
    @staticmethod
    def execute_core_functions(name):
        df = MetaDataExtractor.extract_viz_data(plate = name["plateid"], mjd = name["mjd"], fiber = name["fiberid"])
        wavelen = np.array(df["Wavelength"].tolist())
        flux = np.array(df["Flux"].tolist())
        return wavelen, flux
    
    def template_run(self, name):
        wavelen, flux = self.execute_core_functions(name)
        tool = viz_tool()
        tool.plot_spectral(wavelen, flux, name = "test")

        assert os.path.exists("test_spectral.png")
        # os.remove("test_spectral.png")
        print("The plot exists, but you need to check whether it looks right!")

        ## test for visualization with absorption and emission line included
        features = tool.plot_spectral_ea(wavelen = wavelen, flux = flux, name = "test")
        assert os.path.exists("test_spectral_ea.png")
        assert os.path.exists("test_absorption.png")
        assert os.path.exists("test_emission.png")
        # os.remove("test_spectral.png")
        # os.remove("test_absorption.png")
        # os.remove("test_emission.png")
        assert len(features["wavelen"]) == len(features["flux"]) == len(features["infered_continuum"]) == len(features["absorption"]) == len(features["emission"])
        print("The plot exists, but you need to check whether it looks right!")
    
    def test_good_examples(self):
        ## runs many tests with good examples
        names = [
            {"plateid": 274, "mjd" : 51913, "fiberid": 102}
        ]
        for n in names:
            self.template_run(n)
    
    def test_bad_name(self):
        with pytest.raises(Exception):
            self.template_run("xdftyuikmnbvcxdftyuik,mnbv")
    
    def test_bad_name_2(self):
        with pytest.raises(Exception):
            self.template_run("fyuikjnbvcdfrtyujk")
    
    

if __name__ == "__main__":
    a = Test_viz_integration()
    a.test_good_examples()

    
        

    

