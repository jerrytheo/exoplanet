
# Imports
# =======

from importlib import import_module
import json
import logging


# Required Information
# ====================

_algorithms = {
    # Classification
    'K-Nearest Neighbors': ('sklearn.neighbors', 'KNeighborsClassifier'),
    'Decision Tree': ('sklearn.tree', 'DecisionTreeClassifier'),
    'Linear Discriminant Analysis':
        ('sklearn.discriminant_analysis', 'LinearDiscriminantAnalysis'),
    'Support Vector Classifier': ('sklearn.svm', 'SVC'),
    'Gaussian Naive Bayes': ('sklearn.naive_bayes', 'GaussianNB'),

    # Clustering
    'K-Means': ('sklearn.cluster', 'KMeans'),

    # Regression
    'Gaussian Process': ('sklearn.gaussian_process', 'GaussianProcess'),
    'Linear': ('sklearn.linear_model', 'LinearRegression'),
    'Lasso': ('sklearn.linear_model', 'Lasso'),
    'Ridge': ('sklearn.linear_model', 'Ridge'),
}


# Import required modules.
# =======================

def _importsklearnAPI(algorithm):
    """
    Calls _import to import and append the algorithm's API from the sklearn
    package.

    Parameters
    ----------
    algorithm -- Algorithm whose API to import.
    """
    API = _algorithms[algorithm]
    pkg = API[0]
    mod = API[1]
    cls = getattr(import_module(pkg), mod)
    return cls


# Algorithm Model
# ===============

class Model:

    """
    Provides a convenience wrapper for built model.

    Data Members
    ------------
    model          -- Scikit-learn API object for algorithm.

    Methods
    -------
    fit_data()     -- Trains the model to the training dataset.
    predict_data() -- Predicts data values on new data.
    addAlgorithm() -- Pipeline algorithm.
    """

    def __init__(self, algorithm, params):
        try:
            self.model = _importsklearnAPI(algorithm)(**params)
        except ImportError as err:
            logging.error('ModelBuild:' + str(err))
            logging.error('ModelBuild:Package import failed.')
        else:
            logging.info('ModelBuild:Import successful.')

    def fitData(self, data, labels=None):
        try:
            if labels is None:
                self.model.fit(data)
            else:
                self.model.fit(data, labels)
        except Exception as err:
            logging.error('ModelBuild:Error in training')
            logging.error('ModelBuild:' + str(err))
        else:
            logging.info('ModelBuild:Model fit successful.')

    def predictData(self, data):
        y_pred = None
        try:
            y_pred = self.model.predict(data)
        except Exception as err:
            logging.error('ModelBuild:Error in predicting')
            logging.error('ModelBuild:' + str(err))
        else:
            logging.info('ModelBuild:Prediction Successful')
        return y_pred
