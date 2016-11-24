
# Imports
# =======

from os import path
from json import loads
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MaterialShadow
import logging
from Core.Data import ClassData


# Required Information
# ====================

learning_types = ('Classification', 'Clustering', 'Regression')


# Pre Analysis Widget
# ===================

class LeftPane(QtGui.QWidget):

    '''
    Displays a form for specifying:
        1. Analysis type and Algorithm.
        2. Data Set and metadata pertaining to it.
        3. Parameters for the Algorithm.
    '''

    def __init__(self, parent, defaultState=None):
        super().__init__(parent)
        self.loadAlgorithms()
        self.setupWidgetLayout()
        self.setupConnections()
        self.initialiseState(defaultState)

    def loadAlgorithms(self):
        '''Loads the list of Algorithms available to select from.'''
        self.algorithms = {}
        for ltype in learning_types:
            pfilepath = ltype + '.json'
            pfilepath = path.join('Info', 'Parameters', pfilepath)
            with open(pfilepath) as pfile:
                jsondata = load(pfile)
                self.algorithms[ltype] = list(jsondata[ltype].keys())
                self.algorithms[ltype].sort()

    def setupWidgetLayout(self):
        '''Creates a layout for the widget.'''
        layout = QtGui.QVBoxLayout()
        self.setupAlgoLayout(layout)
        self.setupDataLayout(layout)
        self.setupAParLayout(layout)
        self.setLayout(layout)

    def setupAlgoLayout(self, layout):
        tlabel = QtGui.QLabel('Learning Type', self)
        tcombo = QtGui.QComboBox(self)
        tcombo.addItems(learning_types)
        layout.addLayout(self.rowLayout(tlabel, tcombo))

        alabel = QtGui.QLabel('Algorithm', self)
        acombo = QtGui.QComboBox(self)
        cur = learning_types[0]
        acombo.addItems(tuple(self.algorithms[cur].keys))
        layout.addLayout(self.rowLayout(alabel, acombo))

        dlabel = QtGui.QLabel('Data set', self)
        dledit = QtGui.QLineEdit(self)
        dledit.setPlaceholderText('Must be a .csv file.')
        dlbrowse



    def rowLayout(self, wid1, wid2):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(wid1)
        layout.addWidget(wid2)
        return layout

