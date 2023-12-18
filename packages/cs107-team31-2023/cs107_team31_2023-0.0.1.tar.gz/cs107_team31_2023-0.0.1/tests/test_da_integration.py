from cs107_project.data_augmentation import data_augmentation
from cs107_project.core_functionalities import MetaDataExtractor
from scipy.interpolate import splrep, splev
import numpy as np
import pytest

class Test_data_augmentation_integration:
    @staticmethod
    def execute_core_functions(name):
        tool = MetaDataExtractor(query = None)
        df = tool.extract_ml_data(name)
        wavelen = np.array(df["Wavelength"].tolist())
        flux = np.array(df["Flux"].tolist())
        return wavelen, flux
    
    def template_run(self, name):
        wavelen, flux = self.execute_core_functions(name)
        tool = data_augmentation()
        result = tool.compute_gradient_finite_difference(wavelen, flux)
        grad, model = result["grad"], result["model"]
        assert len(grad) == len(wavelen)
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient
        x = np.random.rand(100, 1)
        grad_pred = model.predict(x)
        assert len(x) == 100

        result = tool.compute_gradient_spline(wavelen, flux)
        grad, model = result["grad"], result["model"]
        assert len(grad) == len(wavelen)
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient
        x = np.random.rand(100)
        grad_pred = splev(x, model)
        assert len(grad_pred) == 100
    
    def test_good_ex(self):
        ## doing K * |name| tests
        names = [1059619742102349824, ]
        for n in names:
            self.template_run(n)
    
    def test_bad_name(self):
        with pytest.raises(Exception):
            self.template_good_ex(self, "asdfghjiytredsxcvbn")
    
    


    

    



