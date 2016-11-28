'''
ExoPlanet Model
Copyright (C) 2016  Abhijit J. Theophilus, Mohinish L. Reddy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# Imports
# =======

from importlib import import_module
import json


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
        self.model = _importsklearnAPI(algorithm)(**params)

    def fitData(self, data, labels=None):
        if labels is None:
            self.model.fit(data)
        else:
            self.model.fit(data, labels)

    def predictData(self, data):
        try:
            y_pred = self.model.predict(data)
        except Exception as err:
            y_pred = None
        return y_pred
