
# Imports
# =======

import logging
import numpy as np
from os import path
from .ViewLabels import ViewLabels
from PyQt4 import QtGui, QtCore


# Prediction UI
# ========== ==

class PredictedLabels(ViewLabels):

    def viewMatrix(self, tableinfo):
        X = tableinfo['Data']
        X = [[str(X[i, j]) for j in range(X.shape[1])]
             for i in range(X.shape[0])]
        y = tableinfo['Predicted']
        if tableinfo['Learning Type'] == 'Classification':
            y = [tableinfo['Labels'][int(i)] for i in y]
        elif tableinfo['Learning Type'] == 'Clustering':
            y = ['Class {0}'.format(i+1) for i in y]
        else:
            y = [str(i) for i in y]

        table = [xrow.append(yval) for xrow, yval in zip(X, y)]
        table.insert(0, [*tableinfo['Headers'], 'Predicted Labels'])

        return table
