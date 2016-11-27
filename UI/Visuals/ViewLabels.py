
# Imports
# =======

import numpy as np
from os import path
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase
import logging


# Prediction UI
# ========== ==

class ViewLabels(QtGui.QDialog):

    '''
    Page that displays the predicted labels of data and allows you to save
    these labels.
    '''

    def __init__(self, parent, workspace):
        super().__init__(parent)
        self.matrix = self.viewMatrix(workspace)
        self.setupDialogLayout()

    def viewMatrix(self, workspace):
        data = workspace['Data'].post_data
        table = []
        table.append((*workspace['Data'].headers, 'Predicted Labels'))
        y_pred = workspace['Predicted']

        if workspace['Learning Type'] != 'Clustering':
            X = data['Testing'].data
            y_true = data['Testing'].labels
            mat = np.insert(X, X.shape[1], y_true, axis=1)
            mat = np.insert(mat, mat.shape[1], y_pred, axis=1)
            for i in range(mat.shape[0]):
                row = []
                for j in range(mat.shape[1]-2):
                    row.append(str(mat[i, j]))
                row.append(data['Labels'][int(mat[i, j+1])])
                row.append(data['Labels'][int(mat[i, j+2])])
                table.append(row)

        else:
            mat = np.insert(data, data.shape[1], y_pred, axis=1)
            for i in range(mat.shape[0]):
                row = []
                for j in range(mat.shape[1]):
                    row.append(str(mat[i, j]))
                table.append(row)
        return table

    def setupDialogLayout(self):
        '''
        Create the layout for the Predict page.
            1. Creates QPushButtons to save labels.
            2. Places the table that shows the predicted labels.
        '''
        table = self.buildTable()
        table.setMaximumSize(self.tableSize(table))
        table.setMinimumSize(table.maximumSize())

        savebtn = QtGui.QPushButton('Save Labels')

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table)
        vbox.addStretch(1)
        vbox.addWidget(savebtn, 1, QtCore.Qt.AlignHCenter)
        vbox.setSpacing(25)
        vbox.setMargin(20)
        self.setLayout(vbox)

    def buildTable(self):
        '''
        Creates the table that displays the predicted labels along with the
        attribute values and fills in the required labels.
        '''
        table = QtGui.QTableWidget(self)

        rows = len(self.matrix)
        cols = max(len(row) for row in self.matrix)

        table.setRowCount(rows)
        table.setColumnCount(cols)

        table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        table.verticalHeader().hide()
        table.horizontalHeader().hide()

        for i, head in enumerate(self.matrix[0]):
            lab = QtGui.QLabel(head, self)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')
            table.setCellWidget(0, i+1, lab)

        for i in range(1, len(self.matrix)):
            lab = QtGui.QLabel(str(i), self)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')
            table.setCellWidget(i, 0, lab)

        for i, row in enumerate(self.matrix[1:]):
            for j, val in enumerate(row):
                lab = QtGui.QLabel(val, self)
                lab.setAlignment(QtCore.Qt.AlignCenter)
                table.setCellWidget(i+1, j+1, lab)

        blank = QtGui.QLabel('')
        blank.setObjectName('BlankLabel')
        table.setCellWidget(0, 0, blank)

        table.resizeColumnsToContents()

        return table

    def tableSize(self, table):
        '''
        Sets the size of the table appropriately.
        '''
        w = 2
        h = 2

        for i in range(table.columnCount()):
            w += table.columnWidth(i)
        for i in range(table.rowCount()):
            h += table.rowHeight(i)

        parent_height = self.parent().size().height()
        parent_width = self.parent().size().width()

        if w > parent_width*0.7:
            w = parent_width*0.7
            h += table.horizontalScrollBar().height()
        return QtCore.QSize(w, h)
