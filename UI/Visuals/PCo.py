
# Imports
# =======


import logging
import numpy as np
from os import path
from math import ceil
from random import shuffle
from PyQt4 import QtGui, QtCore, Qt
from ..Base import ExoCanvas, ComboBox


# Clustering Visuals Widget
# ========== ======= ======

class PCoPlot(QtGui.QDialog):

    def __init__(self, parent, workspace):
        super().__init__(parent)
        self._headers = workspace['Data'].headers
        self.pcoPlot = self.generatePCoPlot(workspace)
        self.setupWidgetLayout()
        self.makeConnections()

    def makeConnections(self):
        for chk in self.chkList:
            chk.stateChanged[int].connect(self.rePlot)
        self.scaleCombo.currentIndexChanged[int].connect(self.rePlot)

    def generatePCoPlot(self, workspace):
        y = workspace['Predicted']
        data = workspace['Data'].post_data
        return (data, y)

    def setupWidgetLayout(self):
        X = self.pcoPlot[0]
        y = self.pcoPlot[1]
        n_y = len(set(y))

        # Build Check Boxes.
        self.chkList = []
        for i in range(n_y):
            chk = QtGui.QCheckBox('Cluster ' + str(i+1), self)
            chk.setFocusPolicy(QtCore.Qt.NoFocus)
            chk.setChecked(True)
            self.chkList.append(chk)

        vboxChkList = QtGui.QVBoxLayout()
        for i in range(0, len(self.chkList)-1, 4):
            hbox = QtGui.QHBoxLayout()
            for j in range(i, i+4):
                hbox.addWidget(self.chkList[j])
            vboxChkList.addLayout(hbox)

        # Build Scale
        scaleLabel = QtGui.QLabel('Scale Type', self)
        scaleLabel.setObjectName('FormLabel')
        self.scaleCombo = ComboBox(self)
        self.scaleCombo.addItems(['None', 'Rescale to [0,1]', 'Normalize'])

        # Build Canvas
        self.pcoCanvas = PCoCanvas(self, X, y, self._headers)
        self.pcoCanvas.setFixedSize(750, 450)
        hboxPCo = QtGui.QHBoxLayout()
        hboxPCo.addStretch(1)
        hboxPCo.addWidget(self.pcoCanvas)
        hboxPCo.addStretch(1)

        # Save Button
        savebtn = QtGui.QPushButton('Save', self)
        savebtn.clicked.connect(self.saveVisual)

        # Build Layouts
        formScale = QtGui.QFormLayout()
        formScale.addRow(scaleLabel, self.scaleCombo)
        formScale.setHorizontalSpacing(25)
        formScale.setVerticalSpacing(15)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hboxPCo)
        vbox.addSpacing(25)
        vbox.addLayout(vboxChkList)
        vbox.addStretch(1)
        vbox.addLayout(formScale)
        vbox.addStretch(1)
        vbox.addWidget(savebtn, 1, QtCore.Qt.AlignHCenter)
        vbox.setMargin(10)
        self.setLayout(vbox)

    def saveVisual(self):
        home = path.expanduser('~')
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Save Folder',
                                                       home)
        self.pcoCanvas.save(dname)
        self.parent().parent().stat.showMessage('Visuals Saved')
        logging.info('ClusVis:Visuals Saved')

    def rePlot(self, state):
        sender = self.sender()
        if sender is self.scaleCombo:
            if state == 0:
                X, y = self.pcoPlot
                logging.info('ClusVis:Changed scaling to None')
            else:
                X, y = self.scaleFeatures(state)
            self.pcoCanvas.createPlot(X, y, self._headers)
            for ind, chk in enumerate(self.chkList):
                if chk.checkState() == 0:
                    line_state = 'off'
                else:
                    line_state = 'on'
                self.pcoCanvas.updatePlot(ind, line_state)

        else:
            ind = self.chkList.index(sender)
            if state == 0:
                line_state = 'off'
                logging.info('ClusVis:Line' + str(ind) + ' turned off.')
            else:
                line_state = 'on'
                logging.info('ClusVis:Line' + str(ind) + ' turned on.')
            self.pcoCanvas.updatePlot(ind, line_state)

    def scaleFeatures(self, type):
        X = np.array(self.pcoPlot[0], copy=True)
        y = self.pcoPlot[1]
        n_samp, n_feat = X.shape
        if type == 1:
            logging.info('ClusVis:Changed scaling to Rescale')
            for i in range(n_feat):
                mx = max(X[:, i])
                mn = min(X[:, i])
                X[:, i] = (X[:, i] - mn)/(mx - mn)
        elif type == 2:
            logging.info('ClusVis:Changed scaling to Normalize')
            mu = np.mean(X, 0)
            sd = np.std(X, 0)
            for i in range(n_feat):
                X[:, i] = (X[:, i] - mu[i])/sd[i]
        return X, y


# Parallel Co-ordinates Canvas
# ======== ============ ======

class PCoCanvas(ExoCanvas):

    def __init__(self, parent, X, y, heads):
        super().__init__(parent, 75)
        self.figure.subplots_adjust(left=0.05, bottom=0.1, top=0.975,
                                    right=0.97)
        self.axes.hold(True)
        self.tick_pos = [i for i in range(len(heads))]
        self.axes.set_xticks(self.tick_pos)
        self.createPlot(X, y, heads)

    def createPlot(self, X, y, heads):
        if hasattr(self, 'clusters'):
            self.axes.cla()
            del(self.clusters)

        self.axes.set_ylabel('Value')
        self.axes.set_xlabel('Features')
        self.axes.set_xticks(self.tick_pos)
        self.axes.set_xticklabels(heads)
        self.clusters = [[] for i in range(max(y)+1)]
        n_samp, n_feat = X.shape
        x_val = [i for i in range(n_feat)]
        colors = ['b', 'g', 'r', 'y', 'm', 'c', 'k']
        for i in range(n_samp):
            self.clusters[y[i]].append(*self.axes.plot(x_val, X[i],
                                       c=colors[y[i] % 7]))
        self.draw()

    def updatePlot(self, index, state):
        if state == 'on':
            for line in self.clusters[index]:
                line.set_visible(True)
        elif state == 'off':
            for line in self.clusters[index]:
                line.set_visible(False)
        self.draw()

    def save(self, dname):
        figname = 'cluster_parallel-coordinates'
        super().save(dname, figname)
