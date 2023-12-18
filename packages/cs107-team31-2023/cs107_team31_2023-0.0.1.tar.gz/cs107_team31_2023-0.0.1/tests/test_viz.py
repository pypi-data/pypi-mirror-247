from cs107_project.visualization import viz_tool
import numpy as np
import pytest
import os 

class Test_visualization:
    """
    There is really no way to test the correctness of the plot automatically, you would need to look at the plot to see if it's legit
    """

    def test_viz(self):
        ## testing for base visualization
        wavelen = np.random.normal(size=  100) * 100
        flux = wavelen ** 2 + np.random.normal(size = 100) * 200
        flux[1:10] += 100000
        tool = viz_tool()
        tool.plot_spectral(wavelen, flux, name = "test")
        assert os.path.exists("test_spectral.png")
        # os.remove("test_spectral.png")
        print("The plot exists, but you need to check whether it looks right!")

        ## test for visualization with absorption and emission line included
        tool.plot_spectral_ea(wavelen, flux, name = "test")
        assert os.path.exists("test_spectral_ea.png")
        assert os.path.exists("test_absorption.png")
        assert os.path.exists("test_emission.png")
        # os.remove("test_spectral.png")
        # os.remove("test_absorption.png")
        # os.remove("test_emission.png")
        print("The plot exists, but you need to check whether it looks right!")
    
    def test_viz_bad_examples(self):
        wavelen = np.random.normal(size=  100) * 100
        flux = np.random.normal(size=  1000) * 100
        with pytest.raises(Exception):
            tool = viz_tool()
            tool.plot_spectral(wavelen, flux, name = "test")
        with pytest.raises(Exception):
            tool = viz_tool()
            tool.plot_spectral_ea(wavelen, flux, name = "test")
    
    def test_viz_bad_examples(self):
        # test when the name is empty--cannot have this because we need to store the plot somewhere
        wavelen = np.random.normal(size=  100) * 100
        flux = np.random.normal(size=  1000) * 100
        with pytest.raises(Exception):
            tool = viz_tool()
            tool.plot_spectral(wavelen, flux, name = "")
        with pytest.raises(Exception):
            tool = viz_tool()
            tool.plot_spectral_ea(wavelen, flux, name = "")
    



