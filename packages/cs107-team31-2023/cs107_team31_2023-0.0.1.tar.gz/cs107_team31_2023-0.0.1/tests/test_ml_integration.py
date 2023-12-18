from cs107_project.machine_learning import knn_classifier
from cs107_project.core_functionalities import MetaDataExtractor
import numpy as np
import pytest
# from sklearn.neighbors import KNeighborsClassifier as sk_knn

label_map = {
    "STAR": 0, 
    "GALAXY": 1, 
    "QSO": 2
}

class Test_ML_integration:
    @staticmethod
    def execute_core_functions(name):
        tool = MetaDataExtractor(query = None)
        df = tool.extract_ml_data(name)
        wavelen = df["Wavelength"].tolist()
        flux = df["Flux"].tolist()
        Class = df["Class"].tolist()
        X = np.array([wavelen, flux]).T
        y = np.array(df["Class"].values)
        print(X.shape)
        y_int = np.array([label_map[y_i] for y_i in y])
        return X, y_int
    
    

    def template_good_ex(self, object_name, k, strict = False):
        ## using strict = True means that you must have <= 3 kinds of labels in y
        X, y = self.execute_core_functions(object_name)
        num_labels = len(np.unique(y))
        if strict:
            assert num_labels <= 3
        knn = knn_classifier(k)
        knn.fit(X, y)
        y_pred = knn.predict(X)
        y_pred_proba = knn.predict_proba(X)
        if k == 1:
            assert np.array_equal(y, y_pred)
        assert len(y_pred) == len(y)
        assert len(y_pred_proba) == len(y)
        assert y_pred_proba.shape[-1] == 3
    
    def test_good_ex(self):
        ## doing K * |name| tests
        names = [1059619742102349824, ]
        for n in names:
            for k in range(1, 5):
                self.template_good_ex(n, k)
    
    def test_bad_name(self):
        with pytest.raises(Exception):
            self.template_good_ex(self, "asdfghjiytredsxcvbn", 2)

    
    def test_bad_k(self):
        good_name = None ## TODO: change here
        with pytest.raises(Exception):
            self.template_good_ex(self, good_name, -1)
    
    def test_bad_k_2(self):
        good_name = None ## TODO: change here
        with pytest.raises(Exception):
            self.template_good_ex(self, good_name, 1e20)

if __name__ == "__main__":
    a = Test_ML_integration()
    a.test_good_ex()


        
            






        

    

