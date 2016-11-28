
# Imports
# =======

import logging
from os import path
from json import load
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, LoadFileWidget, ComboBox, LabelledSlider
from .ParameterForm import ParameterForm
from Core import Data


# Required Information
# ====================

learning_types = ('Classification', 'Clustering', 'Regression')


# Pre Analysis Widget
# ===================

class PreAnalysisForm(ExoBase):

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
        if defaultState is not None:
            self.initialiseState(defaultState)
            self.loadData(True)

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
        header1 = QtGui.QLabel('Algorithm and Data')
        header1.setObjectName('Header')
        header1.setAlignment(QtCore.Qt.AlignHCenter)

        form1 = QtGui.QFormLayout()
        self.setupAlgoLayout(form1)
        self.setupDataLayout(form1)
        form1.setVerticalSpacing(20)
        form1.setLabelAlignment(QtCore.Qt.AlignRight)

        header2 = QtGui.QLabel('Algorithm Parameters')
        header2.setObjectName('Header')
        header2.setAlignment(QtCore.Qt.AlignHCenter)

        self.pform_layout = QtGui.QVBoxLayout()
        self.setupAParLayout(self.pform_layout)

        self.runBtn = QtGui.QPushButton('Analyse', self)
        self.runBtn.setVisible(False)
        self.runBtn.setObjectName('RunButton')

        layout = QtGui.QVBoxLayout()
        layout.addWidget(header1, 1)
        layout.addLayout(form1, 4)
        layout.addSpacing(40)
        layout.addWidget(header2, 1)
        layout.addLayout(self.pform_layout, 4)
        layout.addSpacing(40)
        layout.addLayout(self.createHBox(1, self.runBtn, 1))
        layout.setSpacing(20)
        layout.setMargin(40)

        self.setLayout(layout)

    def initialiseState(self, defaultState):
        # Learning Type
        ltype = self.tcombo.findText(defaultState['Learning Type'])
        self.tcombo.setCurrentIndex(ltype)
        # Algorithm
        algo = self.acombo.findText(defaultState['Algorithm'])
        self.acombo.setCurrentIndex(algo)
        # Data
        self.data = defaultState['Data']
        fpath = path.join(self.data.filedir, self.data.filename)
        if path.isfile(fpath):
            self.dbrwse.setFilePath(fpath)
        else:
            self.stat.showMessage('Filepath invalid.')
        # Parameters
        self.pform.setDefaults(defaultState['Parameters'])

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

        self.slabel = QtGui.QLabel('Size of partitions', self)
        self.sslidr = LabelledSlider(self, 'Training Set', 'Testing Set')
        self.slabel.setVisible(False)
        self.sslidr.setVisible(False)
        layout.addRow(self.slabel, self.sslidr)

        self.hlabel = QtGui.QLabel('Headers present?', self)
        self.hchkbx = QtGui.QCheckBox(self)
        self.hlabel.setVisible(False)
        self.hchkbx.setVisible(False)
        layout.addRow(self.hlabel, self.createHBox(self.hchkbx, 1))

        self.llabel = QtGui.QLabel('Labels column', self)
        self.lcombo = ComboBox(self)
        self.lcombo.setVisible(False)
        self.llabel.setVisible(False)
        self.lcombo.addItem('Attribute 1')
        layout.addRow(self.llabel, self.lcombo)

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
        self.runBtn.clicked.connect(self.parent().analyseData)

    def changeLType(self, ltype):
        self.acombo.clear()
        self.acombo.addItems(self.algorithms[ltype])
        if self.data is not None:
            if ltype == 'Clustering':
                self.slabel.setVisible(False)
                self.sslidr.setVisible(False)
                self.llabel.setVisible(False)
                self.lcombo.setVisible(False)
            else:
                self.slabel.setVisible(True)
                self.sslidr.setVisible(True)
                self.llabel.setVisible(True)
                self.lcombo.setVisible(True)

    def changeAlgorithm(self, algo):
        if not algo:
            return
        ltype = self.tcombo.currentText()
        self.pform.close()
        del(self.pform)
        self.pform = ParameterForm(self, algo, ltype)
        self.pform_layout.addWidget(self.pform)

    def loadData(self, pre=False):
        if not pre:
            data_file = self.dbrwse.getFilePath()
            self.data = Data(data_file)
        self.hchkbx.setCheckState(QtCore.Qt.Unchecked)
        if self.data.check() is False:
            self.parent().stat.showMessage('Data load failed.')
            return
        self.hlabel.setVisible(True)
        self.hchkbx.setVisible(True)
        self.runBtn.setVisible(True)
        self.lcombo.clear()
        self.lcombo.addItems(self.data.headers)
        curLType = self.tcombo.currentText()
        if not curLType == 'Clustering':
            self.slabel.setVisible(True)
            self.sslidr.setVisible(True)
            self.llabel.setVisible(True)
            self.lcombo.setVisible(True)

    def headerSwitch(self, state):
        if state == 2:
            self.data.enableHeaders()
        elif state == 0:
            self.data.disableHeaders()
        self.lcombo.clear()
        self.lcombo.addItems(self.data.headers)

    def value(self):
        ltype = self.tcombo.currentText()
        if ltype == 'Clustering':
            self.data.process(ltype)
        else:
            self.data.process(ltype,
                              self.sslidr.value(),
                              self.lcombo.currentIndex())
        model_info = {
            'Learning Type': self.tcombo.currentText(),
            'Algorithm': self.acombo.currentText(),
            'Data': self.data,
            'Parameters': self.pform.getParameters()
        }
        return model_info
