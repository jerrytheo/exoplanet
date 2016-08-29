
# Imports
# =======

from os import path
import sys
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MaterialShadow
import logging

#-----------------------------------------------------------------------------#

# Prediction UI
# ========== ==


class Predict(ExoBase):

    '''
    Page that displays the predicted labels of data and allows you to save
    these labels.
    '''

    def __init__(self, parent, data, labels):
        super().__init__(parent)
        layout = self.createLayout(data, labels)
        self.initUI(layout)
        
    
    def initUI(self, layout):
        '''
        Initialise the AlgoFile page.
            1. Sets layout for AlgoFile.
            2. Connects the clicked signals for backButton and saveBtn.
        '''

        super().initUI(layout)
        self.backButton.clicked.connect(self.parent().goBack)
        self.saveBtn.clicked.connect(self.parent().buttonClicked)


    def createLayout(self, data, labels):
        '''
        Create the layout for the Predict page.
            1. Creates QPushButtons to save labels.
            2. Places the table that shows the predicted labels.
        '''
        table = self.buildTable(data, labels)
        table.setMaximumSize(self.tableSize(table))
        table.setMinimumSize(table.maximumSize())
        self.saveBtn = QtGui.QPushButton('Save Labels')
        self.saveBtn.setGraphicsEffect(MaterialShadow(self))

        hboxSave = self.hcenter(self.saveBtn)
        hboxTabl = self.hcenter(table)
        hboxBtm = self.iterBtns(next=False)
        
        vboxPred = self.vboxCreate(hboxTabl, 40, hboxSave)
        predCard = self.createCard('Predicted Labels', vboxPred)
        vbox = self.createCardLayout(predCard)
        vbox.addSpacing(40)
        vbox.addLayout(hboxBtm)

        return vbox
        
    
    def buildTable(self, data, labels):
        '''
        Creates the table that displays the predicted labels along with the
        attribute values and fills in the required labels.
        '''
        table = QtGui.QTableWidget(self)
        dataVals = list(data.getPredictData())
        
        for i in range(len(dataVals)):
            dataVals[i] = list(dataVals[i])
            for j in range(len(dataVals[i])):
                dataVals[i][j] = round(float(dataVals[i][j]), 5)

        rows = len(dataVals) + 1
        cols = max( len(i) for i in dataVals ) + 2
        
        table.setRowCount(rows)
        table.setColumnCount(cols)
        
        if data.headers is not None:
            column_headers = [*data.headers, 'Label']
        else:
            column_headers = []
            for i in range(table.columnCount()-1):
                lab = 'Attribute ' + str(i+1)
                column_headers.append(lab)
            column_headers.append('Label')
        
        table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        table.setHorizontalHeaderLabels(column_headers)
        table.verticalHeader().hide()
        table.horizontalHeader().hide()

        for i in range(cols):
            lab = QtGui.QLabel(column_headers[i], self)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')
            table.setCellWidget(0, i+1, lab)

        for i in range(rows):
            lab = QtGui.QLabel(str(i+1), self)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')
            table.setCellWidget(i+1, 0, lab)

        for i in range(len(dataVals)):
            for j in range(len(dataVals[i])):
                lab = QtGui.QLabel(str(dataVals[i][j]), self)
                lab.setAlignment(QtCore.Qt.AlignCenter)
                table.setCellWidget(i+1, j+1, lab)
                
        for i in range(len(labels)):
            lab = QtGui.QLabel(labels[i], self)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            table.setCellWidget(i+1, cols-1, lab)

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
        
        if w > parent_width*0.7 :
            w = parent_width*0.7
            h += table.horizontalScrollBar().height()
        return QtCore.QSize(w, h)


#-----------------------------------------------------------------------------#