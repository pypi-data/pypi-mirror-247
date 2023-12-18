import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.interpolate import splrep, splev

class data_augmentation:
    @staticmethod 
    def compute_gradient_finite_difference(x, y):
        """"
        computes the gradient of y w.r.t. x, use finite differencing method

        input:
        x: np array, [n, ]
        y: np array, [n, ]

        output: dictionary 
        grad: np array [n], grad[i] = dy/dx (x[i])
        model: linear regression model trained on X = x and y = grad
        """
        assert len(x) == len(y)
        assert len(np.unique(x)) > 1
        result = np.zeros((len(x), ))
        for i in range(len(x)):
            x_i = x[i]
            y_i = y[i]
            abs_distance_x_i = np.abs(x - x_i)
            abs_distance_x_i[abs_distance_x_i == 0] = np.inf ## otherwise lead to div by 0 error
            min_id = np.argmin(abs_distance_x_i)
            grad_i = (y[i] - y[min_id]) / (x[i] - x[min_id])  ## finite differencing 
            result[i] = grad_i
        model = LinearRegression()
        model.fit(np.expand_dims(x, axis = 0).T, result)
        return {
            "grad": result, 
            "model": model,
        }
    
    @staticmethod 
    def compute_gradient_spline(x, y, delta = 1e-2):
        """"
        computes the gradient of y w.r.t. x, use finite differencing method

        input:
        x: np array, [n, ]
        y: np array, [n, ]

        output: dictionary 
        grad: np array [n], grad[i] = dy/dx (x[i])
        model: linear regression model trained on X = x and y = grad
        """
        assert len(x) == len(y)
        assert len(np.unique(x)) > 1
        ind = np.argsort(x)
        x_sorted = x[ind]
        y_sorted = y[ind]
        result = np.zeros((len(x), ))
        spline = splrep(x_sorted,y_sorted,s=1e50)
        for i in range(len(x)):
            x_i = x[i]
            y_i = y[i]
            y_j = splev(np.array([x[i] + delta]),spline).item()
            grad_i = (y_j - y_i) / (delta)  ## finite differencing 
            result[i] = grad_i
        model = spline
        return {
            "grad": result, 
            "model": model,
        }
    


    # @staticmethod
    # def compute_gradient_package(x, y):
    #     """"
    #     computes the gradient of y w.r.t. x, use external package

    #     input:
    #     x: np array, [n, ]
    #     y: np array, [n, ]

    #     output:
    #     grad: np array [n], grad[i] = dy/dx (x[i])
    #     """
    #     return None ## TODO




