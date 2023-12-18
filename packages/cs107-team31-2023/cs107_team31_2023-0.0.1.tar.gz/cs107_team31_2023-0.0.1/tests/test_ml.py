# import sys
# sys.path.append('../src')
from cs107_project.machine_learning import knn_classifier
import numpy as np
import pytest
from sklearn.neighbors import KNeighborsClassifier as sk_knn

class Test_knn_classifier:

    @staticmethod
    def test_knn_good_example():
        knn = knn_classifier(1)
        X_train = np.array(
            [[1, 2, 3, 1, 2, 3, 1],
             [-1, 2, -2, 1, -3, 2, -1],
             [-10000, -200, -10000, -2, 3, -100, -900],
             [100,200, 700, 100, 3000, 2100, 900]]
        )
        y_train = np.array([0, 1, 2, 1])
        knn.fit(X_train, y_train)
        X_test = np.array(
             [[-11000, -210, -10030, -20, 30, -120, -980],
             [120, 2089, 770, 120, 3030, 2101, 9001]]
        )
        y_reference = np.array([2, 1])
        proba_reference = np.array([[0, 0, 1], [0, 1, 0]])
        y_pred = knn.predict(X_test)
        proba_pred = knn.predict_proba(X_test)

        assert np.array_equal(y_reference, y_pred)
        assert np.array_equal(proba_reference, proba_pred)
    
    def test_knn_unequal_len(self):
        knn = knn_classifier(1)
        X_train = np.array(
            [[1, 2, 3, 1, 2, 3, 1],
             [-1, 2, -2, 1, -3, 2, -1],
             [-10000, -200, -10000, -2, 3, -100, -900],
             [100,200, 700, 100, 3000, 2100, 900]]
        )
        y_train = np.array([0, 1, 2, 1, 2])
        with pytest.raises(Exception):
            knn.fit(X_train, y_train)
    
    def test_knn_bad_label(self):
        knn = knn_classifier(1)
        X_train = np.array(
            [[1, 2, 3, 1, 2, 3, 1],
             [-1, 2, -2, 1, -3, 2, -1],
             [-10000, -200, -10000, -2, 3, -100, -900],
             [100,200, 700, 100, 3000, 2100, 900]]
        )
        y_train = np.array([0, 1, 2, -1])
        with pytest.raises(Exception):
            knn.fit(X_train, y_train)
    
    def test_knn_bad_k(self):
        knn = knn_classifier(5)
        X_train = np.array(
            [[1, 2, 3, 1, 2, 3, 1],
             [-1, 2, -2, 1, -3, 2, -1],
             [-10000, -200, -10000, -2, 3, -100, -900],
             [100,200, 700, 100, 3000, 2100, 900]]
        )
        y_train = np.array([0, 1, 2, -1])
        with pytest.raises(Exception):
            knn.fit(X_train, y_train)
    
    def test_knn_bad_k_2(self):
        with pytest.raises(Exception):
            knn = knn_classifier(-1)
            X_train = np.array(
                [[1, 2, 3, 1, 2, 3, 1],
                [-1, 2, -2, 1, -3, 2, -1],
                [-10000, -200, -10000, -2, 3, -100, -900],
                [100,200, 700, 100, 3000, 2100, 900]]
            )
            y_train = np.array([0, 1, 2, -1])
            knn.fit(X_train, y_train)
    
    def test_knn_larger_example(self):
        knn = knn_classifier(5)
        X_train = np.random.rand(100, 10)
        y_train = np.random.randint(low = 0, high = 3, size = 100)
        knn.fit(X_train, y_train)
        X_test = np.random.rand(10, 10)
        y_pred = knn.predict(X_test)
        proba_pred = knn.predict_proba(X_test)
        assert len(y_pred) == 10
        sum_prob = np.sum(proba_pred, -1)
        for s in sum_prob: 
            assert s == 1
        
        ## compare with sklearn's KNN implementation 
        sklearn_knn = sk_knn(5)
        sklearn_knn.fit(X_train, y_train)
        sk_y_pred = sklearn_knn.predict(X_test)
        assert np.array_equal(sk_y_pred, y_pred)
        y_test = np.random.randint(low = 0, high = 3, size = 10)
        assert np.array_equal(knn.confusion_matrix(y_test, y_pred), knn.confusion_matrix_sklearn(y_test, y_pred))

        




    