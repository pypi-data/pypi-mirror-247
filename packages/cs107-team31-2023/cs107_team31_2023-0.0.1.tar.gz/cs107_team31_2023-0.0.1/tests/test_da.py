from cs107_project.data_augmentation import data_augmentation
from scipy.interpolate import splrep, splev
import numpy as np
import pytest

class Test_data_augmentation:
    def test_simple_example(self):
        x = np.array([1.0, 2.0, 5.0, 4.0])
        y = np.array([10.0, 20.0, 30.0, 40.0])
        grad_ref = np.array([10, 10, -10, -10], dtype = float)
        result = data_augmentation.compute_gradient_finite_difference(x, y)
        grad, model = result["grad"], result["model"]
        assert len(grad) == 4
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient 
        assert np.array_equal(grad, grad_ref)
        pred_x = np.expand_dims(x, axis = 0).T
        y_reference = np.array([ 12.0,   6.0, -12.0,  -6.0])
        pred_y = model.predict(pred_x)
        assert np.allclose(pred_y , y_reference, atol = 1e-5)

    def test_good_example(self):
        x = np.random.normal(size = 100)
        y = 100 * x + np.random.normal(size = 100)
        result = data_augmentation.compute_gradient_finite_difference(x, y)
        grad, model = result["grad"], result["model"]
        assert len(grad) == 100
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient 
        pred_x = np.random.rand(100, 1)
        assert len(model.predict(pred_x)) == 100
    
    def test_good_example_2(self):
        x = np.random.normal(size = 100)
        y = 100 * x + np.random.normal(size = 100)
        x[1:10] = 1 ## the function must not fail where there are repeat x values 
        result = data_augmentation.compute_gradient_finite_difference(x, y)
        grad, model = result["grad"], result["model"]
        assert len(grad) == 100
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient 
        pred_x = np.random.rand(100, 1)
        assert len(model.predict(pred_x)) == 100

    def test_good_example_3(self):
        x = np.random.uniform(size = 100)
        y = 100 * x + np.random.uniform(size = 100)
        result = data_augmentation.compute_gradient_spline(x, y)
        grad, model = result["grad"], result["model"]
        assert len(grad) == 100
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient 
        pred_x = np.random.rand(100)
        assert len(splev(pred_x, model)) == 100
    
    def test_good_example_4(self):
        x = np.random.rand(100)
        y = 100 * x + np.random.rand(100)
        result = data_augmentation.compute_gradient_spline(x, y)
        grad, model = result["grad"], result["model"]
        assert len(grad) == 100
        assert np.sum(np.abs(grad)) != 0 ## must exist some gradient 
        pred_x = np.random.rand(100)
        assert len(splev(pred_x, model)) == 100
    
    
    def test_bad_example_1(self):
        x = np.ones((100, ))
        y = 100 * x + np.random.normal(size = 100)
        with pytest.raises(Exception):
            result = data_augmentation.compute_gradient_finite_difference(x, y)
            grad, model = result["grad"], result["model"]
            pred_x = np.random.rand(100, 1)
            assert len(model.predict(pred_x)) == 100
        ## the function must fail if all x avlues are the same 
    
    def test_bad_example_2(self):
        x = np.random.normal(size = 1000) ## unequal length
        y = np.random.normal(size = 100)
        with pytest.raises(Exception):
            result = data_augmentation.compute_gradient_finite_difference(x, y)
            grad, model = result["grad"], result["model"]
            pred_x = np.random.rand(100, 1)
            assert len(model.predict(pred_x)) == 100
    
    def test_bad_example_3(self):
        x = np.random.normal(size = 1000) ## unequal length
        y = np.random.normal(size = 100)
        with pytest.raises(Exception):
            result = data_augmentation.compute_gradient_spline(x, y)
            grad, model = result["grad"], result["model"]
    
    
