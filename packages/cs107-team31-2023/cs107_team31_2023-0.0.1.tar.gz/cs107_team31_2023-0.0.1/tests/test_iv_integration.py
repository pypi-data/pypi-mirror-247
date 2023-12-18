from cs107_project.visualization_interactive import viz_tool_interactive
from cs107_project.core_functionalities import MetaDataExtractor
import numpy as np
import pytest


class test_iv_integration:
    @staticmethod
    def execute_core_functions(name):
        df = MetaDataExtractor.extract_viz_data(plate=name["plateid"], mjd=name["mjd"], fiber=name["fiberid"])
        wavelen = np.array(df["Wavelength"].tolist())
        flux = np.array(df["Flux"].tolist())
        assert len(wavelen) == len(flux)
        return wavelen, flux

    def template_run(self, name):
        wavelen, flux = self.execute_core_functions(name)

        tool = viz_tool_interactive()

        try:
            tool.interactive_spectral(wavelen, flux, "test")
            interactive_spectral_success = True
        except Exception as e:
            interactive_spectral_success = False

        assert interactive_spectral_success, "The interactive_spectral method failed to initialize or execute"
