'''
ExoPlanet Model
Copyright (C) 2016  Abhijit J. Theophilus

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

import json
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, Lasso, Ridge


# Required Information
# ====================

_algorithms = {
    # Classification
    'K-Nearest Neighbors': KNeighborsClassifier,
    'Decision Tree': DecisionTreeClassifier,
    'Linear Discriminant Analysis': LinearDiscriminantAnalysis,
    'Support Vector Classifier': SVC,
    'Gaussian Naive Bayes': GaussianNB,

    # Clustering
    'K-Means': KMeans,

    # Regression
    'Linear': LinearRegression,
    'Lasso': Lasso,
    'Ridge': Ridge,
}


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
        self.model = _algorithms[algorithm](**params)

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
