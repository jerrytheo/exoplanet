'''
ExoPlanet Post-Analysis Options
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

from os import path
from PyQt4 import QtGui, QtCore
from Core import Data
from ..Base import ExoBase, LoadFileWidget
from ..Visuals import ROC, ConfusionMatrix
from ..Visuals import PCoPlot
from ..Visuals import RegressionLine
from ..Visuals import ViewLabels


# Required Information
# ====================

visuals_available = {
    'Classification': {
        'Confusion Matrix': ConfusionMatrix,
        'Receiver Operating Characteristic': ROC
    },
    'Clustering': {
        'Parallel Co-Ordinates Plot': PCoPlot
    },
    'Regression': {
        'Regression Line': RegressionLine
    }
}


# Training Completion UI
# ======== ========== ==

class PostAnalysisOptions(ExoBase):

    def __init__(self, parent, workspace):
        super().__init__(parent)
        self.workspace = workspace
        self.stat = self.parent().stat
        self.setupWidgetLayout()

    def setupWidgetLayout(self):
        layout = QtGui.QVBoxLayout()
        layout.setMargin(40)

        title = '{0} — {1}'.format(self.workspace['Learning Type'],
                                   self.workspace['Algorithm'])
        header1 = QtGui.QLabel(title, self)
        header1.setObjectName('Header')
        header1.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(header1)
        layout.addSpacing(15)
        self.setupInfoLayout(layout)
        layout.addSpacing(40)

        header2 = QtGui.QLabel('Results', self)
        header2.setObjectName('Header')
        header2.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(header2)
        layout.addSpacing(15)
        self.setupResultsLayout(layout)
        layout.addSpacing(40)

        header3 = QtGui.QLabel('Apply Model', self)
        header3.setObjectName('Header')
        header3.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(header3)
        layout.addSpacing(15)
        self.setupApplyLayout(layout)

        self.setLayout(layout)

    def setupInfoLayout(self, layout):
        left = ['Data Set', 'Size', 'Attributes']
        right = [
            self.workspace['Data'].filename,
            '{0} Rows, {1} Attributes'.format(*self.workspace['Data'].size),
            ', '.join(self.workspace['Data'].headers)
        ]

        if self.workspace['Learning Type'] == 'Classification':
            left.append('Classes')
            right.append(', '.join(self.workspace['Data'].post_data['Labels']))
            left.append('Accuracy')
            right.append(self.getAccuracy('Classification'))
        elif self.workspace['Learning Type'] == 'Regression':
            left.append('Coefficient of Determination')
            right.append(self.getAccuracy('Regression'))

        form = QtGui.QFormLayout()
        for lval, rval in zip(left, right):
            llabel = QtGui.QLabel(lval, self)
            rlabel = QtGui.QLabel(rval, self)
            rlabel.setObjectName('Info')
            form.addRow(llabel, rlabel)
        form.setSpacing(10)
        form.setMargin(0)
        layout.addLayout(self.createHBox(1, form, 1))

    def setupResultsLayout(self, layout):
        visuals_list = [*visuals_available[self.workspace['Learning Type']]]
        visuals_list.append('View Labels')
        btnlayout = QtGui.QVBoxLayout()
        for vis in visuals_list:
            pbutn = QtGui.QPushButton(vis, self)
            pbutn.setObjectName('Visuals')
            pbutn.clicked.connect(self.showVisual)
            btnlayout.addWidget(pbutn)
        btnlayout.setSpacing(10)
        layout.addLayout(self.createHBox(1, btnlayout, 1))

    def setupApplyLayout(self, layout):
        form = QtGui.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignRight)
        form.setVerticalSpacing(20)

        dlabel = QtGui.QLabel('Data set')
        self.dbrwse = LoadFileWidget(self, self.workspace['Data'].filedir)
        form.addRow('Data set', self.dbrwse)

        self.hlabel = QtGui.QLabel('Headers present?', self)
        self.hchkbx = QtGui.QCheckBox(self)
        form.addRow(self.hlabel, self.createHBox(self.hchkbx, 1))

        prdbtn = QtGui.QPushButton('Predict Labels')
        prdbtn.setObjectName('Predict')
        prdbtn.clicked.connect(self.predictLabels)
        form.addRow(self.createHBox(1, prdbtn, 1))

        layout.addLayout(form)

    def loadData(self):
        pass

    def showVisual(self):
        src = self.sender()
        btn = src.text()
        if btn == 'View Labels':
            Visual = ViewLabels
        else:
            Visual = visuals_available[self.workspace['Learning Type']][btn]

        visual = Visual(self, self.workspace)
        visual.setWindowTitle('Exoplanet: {0}'.format(btn))
        visual.show()
        visual.raise_()
        visual.activateWindow()

    def getAccuracy(self, ltype):
        X = self.workspace['Data'].post_data['Testing'].data
        y_true = self.workspace['Data'].post_data['Testing'].labels
        if ltype == 'Classification':
            y_pred = self.workspace['Predicted']
            correct = 0
            for i in range(len(y_true)):
                if y_true[i] == y_pred[i]:
                    correct += 1
            acc = correct/len(y_true)
        elif ltype == 'Regression':
            acc = self.workspace['Model'].model.score(X, y_true)
        return '{0} %'.format(round(acc * 100, 3))

    def predictLabels(self):
        fpath = self.dbrwse.getFilePath()
        newdata = Data(fpath)
        if self.hchkbx.isChecked():
            newdata.enableHeaders()
        newdata.process('Clustering')
        pred = self.workspace['Model'].predictData(newdata.post_data)
        if pred is None:
            self.stat.showMessage('Prediction Failed.')
            return
        if self.workspace['Learning Type'] == 'Classification':
            labels = self.workspace['Data'].post_data['Labels']
            pred = [labels[int(i)] for i in pred]
        elif self.workspace['Learning Type'] == 'Clustering':
            pred = ['Class {0}'.format(i) for i in np.unique(pred)]
        ws_new = {
            'Learning Type': 'Prediction',
            'Data': newdata,
            'Predicted': pred
        }
        showDialog = ViewLabels(self, ws_new)
        showDialog.setWindowTitle('Exoplanet: Predicted Labels')
        showDialog.show()
        showDialog.raise_()
        showDialog.activateWindow()
