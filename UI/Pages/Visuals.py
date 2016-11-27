
# Imports
# =======


import sys
from os import path
import csv
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MaterialShadow
from ..Visuals import ClassVis, RegrVis, ClusVis
import numpy as np


# Visual Evaluations UI
# ====== =========== ==


class Visual(ExoBase):

    '''
    Page that displays the visuals for each type of learning:
    Classification -
        1. Receiver Operating Characteristic Curve.
        2. Confusion Matrix.
    Clustering -
        1. Parallel Co-ordinates Plot.
    Regression -
        1. Regression Line.
    '''

    def __init__(self, parent, algotype, visuals):
        super().__init__(parent)
        self.algotype = algotype
        layout = self.createLayout(visuals)
        self.initUI(layout)

    def initUI(self, layout):
        '''
        Initialise the Visual page.
            1. Sets layout for Visual.
            2. Connects the clicked signals for saveBtn1, saveBtn2, rerunBtn
               and backButton.
        '''
        super().initUI(layout)
        self.saveBtn1.clicked.connect(self.parent().buttonClicked)
        self.rerunBtn.clicked.connect(self.parent().buttonClicked)
        self.backButton.clicked.connect(self.parent().goBack)
        self.saveBtn2.clicked.connect(self.visWidget.saveVisual)

    def createLayout(self, visuals):
        '''
        Creates the layout for the Visual page.
            1. Creates the QPushButtons necessary to save the Model, save the
               visuals and to change parameters for the model.
            2. Based on the algorithm type builds the visual object.
        '''
        # Build buttons
        self.saveBtn1 = QtGui.QPushButton('Save Model')
        self.saveBtn2 = QtGui.QPushButton('Save Visuals')
        self.rerunBtn = QtGui.QPushButton('Change parameters')
        self.saveBtn1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveBtn1.setGraphicsEffect(MaterialShadow(self))
        self.saveBtn2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveBtn2.setGraphicsEffect(MaterialShadow(self))
        self.rerunBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rerunBtn.setGraphicsEffect(MaterialShadow(self))
        hboxNext = self.hcenter(self.saveBtn1, self.rerunBtn, self.saveBtn2)
        hboxNext.setSpacing(30)
        hboxBtm = self.iterBtns(next=False)

        # Build Labels
        ques = QtGui.QLabel('Visuals', self)
        ques.setObjectName('QuesLabel')
        hboxQues = self.hcenter(ques)

        # Build Visual Widget
        if self.algotype == 'Classification':
            self.visWidget = ClassVis(self, visuals)
        elif self.algotype == 'Regression':
            self.visWidget = RegrVis(self, visuals)
        elif self.algotype == 'Clustering':
            self.visWidget = ClusVis(self, visuals)

        return self.vboxCreate(self.visWidget, 40, hboxNext, 40, hboxBtm)
