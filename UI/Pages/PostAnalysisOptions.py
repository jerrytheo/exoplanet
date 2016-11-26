
# Imports
# =======

from os import path
import sys
import logging
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase


# Required Information
# ====================

visuals_available = {
    'Classification': ('Confusion Matrix', 'Receiver Operating Characteristic'),
    'Clustering': ('Parallel Co-Ordinates Plot'),
    'Regression': ('Regression Line')
}


# Training Completion UI
# ======== ========== ==

class PostAnalysisOptions(ExoBase):

    def __init__(self, parent, model_info):
        super().__init__(parent)
        self.setupWidgetLayout(model_info)

    def setupWidgetLayout(self, model_info):
        pass