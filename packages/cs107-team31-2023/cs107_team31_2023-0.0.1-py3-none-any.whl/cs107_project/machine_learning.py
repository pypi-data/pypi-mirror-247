import numpy as np 
from sklearn.metrics import confusion_matrix
class knn_classifier:
    def __init__(self, n_neighbors, num_labels = 3):
        """
        initialize the knn classifier 
        input:
        n_neighbor: number of neighbors in the KNN classifier. need k > 0
        n_labels: the number of labels. default to 3 for STAR, GALAXY, QSO
        """
        self.k = n_neighbors
        self.num_labels = num_labels
        assert self.k > 0
    
    def predict(self, X):
        """
        predicts y from X based on the model 
        input: 
        X: numpy array, size [n, m], n: number of samples, m: number of features

        returns:
        y: [n], y[i] the predicted class for each sample in X 
        """
        d = self._distance_matrix(X, self.X)
        sort_index = np.argsort(d, axis = -1)
        topk_index = sort_index[:, :self.k]
        topk_y = self.y[topk_index]
        return self._mode_2darray(topk_y)
        
    def predict_proba(self, X):
        """
        predicts the probability y from X based on the model. 
        input: 
        X: numpy array, size [n, m], n: number of samples, m: number of features

        returns:
        y: [n, num_labels], y[i, j] the predicted probability of sample i belonging to class j
        """
        d = self._distance_matrix(X, self.X)
        sort_index = np.argsort(d, axis = -1)
        topk_index = sort_index[:, :self.k]
        topk_y = self.y[topk_index]
        proba = self._counts_to_proba(topk_y)
        return proba
    
    def fit(self, X, y):
        """
        fits the KNN model given features X and labels y
        input: 
        X: numpy array, size [n, m], n: number of samples, m: number of features
        y: numpy array, size [n, ], y[i] = the class of sample i, 0 <= y[i] < num_class for all i
        """
        assert len(X) == len(y)
        assert min(y) >= 0
        assert max(y) < self.num_labels 
        assert len(X) >= self.k
        self.X = X
        self.y = y
    
    def confusion_matrix(self, y_true, y_pred):
        """
        implements the confusin matrix from scratch
        input: 
        y_true: numpy array, size [n], true label
        y_ored: numpy array, size [n], predicted label
        """
        ## implements from scratch 
        matrix = np.zeros((self.num_labels, self.num_labels))
        for t, p in zip(y_true, y_pred):
            matrix[t, p] += 1
        return matrix 

    
    @staticmethod 
    def confusion_matrix_sklearn(y_true, y_pred):
        """
        implements the confusin matrix using sklearn's API
        input: 
        y_true: numpy array, size [n], true label
        y_ored: numpy array, size [n], predicted label
        """
        ## simply uses sklearn's implementation 
        return confusion_matrix(y_true, y_pred)

    
    @staticmethod 
    def _distance(x, X):
        """
        compute the distance between vector x and matrix X
        input: 
        x: numpy array, size (m)
        X: numpy array, size (n, m)
        return:
        numpy array d with size (n), where d[i] = ||x - X[i]||^2_2
        """
        d = []
        for x_i in X:
            d.append(np.sum(np.square(x - x_i)))
        return np.array(d)
    
    def _distance_matrix(self, X1, X2):
        """
        compute the distance between matrix X1 and matrix X2
        input: 
        x: numpy array, size (n1, m)
        X: numpy array, size (n2, m)
        return:
        numpy array d with size (n1, n2), where d[i, j] = ||X1[i] - X_2[j]||^2_2
        """
        d = []
        for x_i in X1:
            d.append(self._distance(x_i, X2).tolist())
        return np.array(d)
    
    @staticmethod 
    def _mode_2darray(X):
        """
        finds the mode of 2d array X along the -1 axis
        input: 
        X: numpy array, size (n, m)
        return:
        numpy array m with size (n), where m[i] = mode(X[i])
        """
        m = []
        for x in X:
            vals, counts = np.unique(x, return_counts=True)
            mode_index = np.argmax(counts)
            mode_i = vals[mode_index]
            m.append(mode_i)
        return np.array(m)
    
    def _counts_to_proba(self, y):
        """
        compute the probability distribution from counts
        input: 
        y: numpy array, size (n, m)
        return:
        numpy array P with size (n, num_label), where P[i, j] = counts(occurence of j in y[i]) / m
        """
        P = np.zeros((len(y), self.num_labels))
        for i in range(len(y)):
            y_i = y[i]
            for j in range(self.num_labels):
                P[i][j] = np.sum(y_i == j) / self.k
        for p_i in P:
            assert np.sum(p_i) == 1
        return P




        

