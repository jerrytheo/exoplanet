
# Imports
# =======

import logging
import numpy as np
from os import path
from PyQt4 import QtGui, QtCore


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
        if workspace['Learning Type'] == 'Classification':
            X = data['Testing'].data
            X = [[str(X[i, j]) for j in range(X.shape[1])]
                 for i in range(X.shape[0])]
            labels = data['Labels']
            y_tr = data['Testing'].labels
            y_pr = workspace['Predicted']
            y_tr = [labels[int(i)] for i in y_tr]
            y_pr = [labels[int(i)] for i in y_pr]
            table = [[*xrow, tr, pr] for xrow, tr, pr in zip(X, y_tr, y_pr)]

        elif workspace['Learning Type'] == 'Regression':
            X = data['Testing'].data
            X = [[str(X[i, j]) for j in range(X.shape[1])]
                 for i in range(X.shape[0])]
            y_tr = data['Testing'].labels
            y_tr = [str(i) for i in y_tr]
            y_pr = [str(i) for i in workspace['Predicted']]
            table = [[*xrow, tr, pr] for xrow, tr, pr in zip(X, y_tr, y_pr)]

        else:
            X = data
            X = [[str(X[i, j]) for j in range(X.shape[1])]
                 for i in range(X.shape[0])]
            y_pr = [str(i) for i in workspace['Predicted']]
            table = [[*xrow, pr] for xrow, pr in zip(X, y_pr)]

        table.insert(0, [*workspace['Data'].headers, 'Predicted Labels'])
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

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(table)

        vbox.addStretch(1)
        savebtn = QtGui.QPushButton('Save Labels')
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

        table.setRowCount(rows-1)
        table.setColumnCount(cols)

        table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)

        table.setHorizontalHeaderLabels(self.matrix[0])
        for i, row in enumerate(self.matrix[1:]):
            for j, val in enumerate(row):
                lab = QtGui.QLabel(val, self)
                lab.setAlignment(QtCore.Qt.AlignCenter)
                lab.setObjectName('InfoLabel')
                table.setCellWidget(i, j, lab)

        table.resizeColumnsToContents()

        return table

    def tableSize(self, table):
        '''
        Sets the size of the table appropriately.
        '''
        w = 4
        h = 4

        for i in range(table.columnCount()):
            w += table.columnWidth(i)
        for i in range(table.rowCount()):
            h += table.rowHeight(i)

        parent_height = self.parent().size().height()
        parent_width = self.parent().size().width()

        if w > parent_width*0.9:
            w = parent_width*0.9
            h += table.horizontalScrollBar().height()
        if h > parent_height*0.7:
            h = parent_height*0.7
            w += table.verticalScrollBar().width()
        return QtCore.QSize(w, h)
