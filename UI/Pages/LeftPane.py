
# Imports
# =======

import logging
from os import path
from json import load
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, LoadFileWidget, ComboBox, Slider
from .ParameterForm import ParameterForm
from Core import Data


# Required Information
# ====================

learning_types = ('Classification', 'Clustering', 'Regression')


# Pre Analysis Widget
# ===================

class LeftPane(ExoBase):

    '''
    Displays a form for specifying:
        1. Analysis type and Algorithm.
        2. Data Set and metadata pertaining to it.
        3. Parameters for the Algorithm.
    '''

    def __init__(self, parent, defaultState=None):
        super().__init__(parent)
        self.data = None
        self.loadAlgorithms()
        self.setupWidgetLayout()
        self.setupConnections()
        # self.initialiseState(defaultState)

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
        header = QtGui.QLabel('Set Input Values')
        header.setObjectName('Header')
        header.setAlignment(QtCore.Qt.AlignHCenter)

        form = QtGui.QFormLayout()
        self.setupAlgoLayout(form)
        self.setupDataLayout(form)
        self.setupAParLayout(form)
        form.setVerticalSpacing(20)
        form.setLabelAlignment(QtCore.Qt.AlignRight)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(header, 1)
        layout.addLayout(form, 4)
        layout.setSpacing(20)
        self.setLayout(layout)

    def setupAlgoLayout(self, layout):
        self.tcombo = ComboBox(self)
        self.tcombo.addItems(learning_types)
        layout.addRow('Learning Type', self.tcombo)

        self.acombo = ComboBox(self)
        cur = learning_types[0]
        self.acombo.addItems(self.algorithms[cur])
        layout.addRow('Algorithm', self.acombo)

    def setupDataLayout(self, layout):
        self.dbrwse = LoadFileWidget(self)
        self.dloadf = QtGui.QPushButton('Load Data', self)
        layout.addRow('Data set', self.dbrwse)
        loadLayout = QtGui.QHBoxLayout()
        loadLayout.addWidget(self.dloadf, 0, QtCore.Qt.AlignRight)
        loadLayout.setMargin(0)
        layout.addRow(loadLayout)

        slabel = QtGui.QLabel('Size of partitions', self)
        self.sslidr = Slider(self, 'Training Set', 'Testing Set')
        self.sslidr.setDisabled(True)
        layout.addRow(slabel, self.sslidr)

        hlabel = QtGui.QLabel('Headers present?', self)
        self.hchkbx = QtGui.QCheckBox(self)
        self.hchkbx.setDisabled(True)
        layout.addRow(hlabel, self.createHBox(self.hchkbx, 1))

        llabel = QtGui.QLabel('Labels column', self)
        self.lcombo = ComboBox(self)
        self.lcombo.setDisabled(True)
        self.lcombo.addItem('Attribute 1')
        layout.addRow(llabel, self.lcombo)

    def setupAParLayout(self, layout):
        ltype = self.tcombo.currentText()
        algo = self.acombo.currentText()
        self.pform = ParameterForm(self, algo, ltype)
        layout.addWidget(self.pform)

    def setupConnections(self):
        self.tcombo.currentIndexChanged[str].connect(self.changeLType)
        self.acombo.currentIndexChanged[str].connect(self.changeAlgorithm)
        self.dloadf.clicked.connect(self.loadData)
        self.hchkbx.stateChanged[int].connect(self.headerSwitch)

    def changeLType(self, ltype):
        self.acombo.clear()
        self.acombo.addItems(self.algorithms[ltype])
        if self.data is not None:
            if ltype == 'Clustering':
                self.sslidr.setDisabled(True)
                self.lcombo.setDisabled(True)
            else:
                self.sslidr.setDisabled(False)
                self.lcombo.setDisabled(False)

    def changeAlgorithm(self, algo):
        del self.pform
        ltype = self.tcombo.currentText()
        self.pform = ParameterForm(self, algo, ltype)

    def loadData(self):
        data_file = self.dbrwse.getFilePath()
        self.data = Data(data_file)
        if self.data.check() is False:
            self.parent().stat.showMessage('Data load failed.')
        else:
            self.hchkbx.setDisabled(False)
            self.lcombo.clear()
            self.lcombo.addItems(self.data.headers)
            curLType = self.tcombo.currentText()
            if not curLType == 'Clustering':
                self.sslidr.setDisabled(False)
                self.lcombo.setDisabled(False)

    def headerSwitch(self, state):
        if state == 2:
            self.data.enableHeaders()
        elif state == 0:
            self.data.disableHeaders()
        self.lcombo.clear()
        self.lcombo.addItems(self.data.headers)
