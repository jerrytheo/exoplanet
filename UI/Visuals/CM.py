
# Imports
# =======

import csv
import logging
from os import path
from sklearn.metrics import confusion_matrix
from ..Base import ExoCanvas
from PyQt4 import QtGui, QtCore


# Classification Visuals Widget
# ============== ======= ======

class ConfusionMatrix(QtGui.QDialog):

    def __init__(self, parent, workspace):
        super().__init__(parent)
        self._labels = workspace['Data'].post_data['Labels']
        self.conf = self.generateConfusionMatrix(workspace)
        self.setupDialogLayout()

    def generateConfusionMatrix(self, workspace):
        X = workspace['Data'].post_data['Testing'].data
        y_true = workspace['Data'].post_data['Testing'].labels
        y_pred = workspace['Model'].predictData(X)
        try:
            C = confusion_matrix(y_true, y_pred)
        except Exception as err:
            logging.error('Evaluation:Confusion Matrix:' + str(err))
            C = None
        return C

    def setupDialogLayout(self):
        self.confMat = CMatrix(self, self.conf, self._labels)
        savebtn = QtGui.QPushButton('Save', self)
        savebtn.clicked.connect(self.saveVisual)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.confMat)
        layout.addSpacing(25)
        layout.addLayout(saveLayout)
        layout.addWidget(savebtn, 1, QtCore.Qt.AlignHCenter)
        layout.setMargin(10)

        self.setLayout(layout)

    def saveVisual(self):
        home = path.expanduser('~')
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Save Folder',
                                                       home)
        self.confMat.save(dname)
        self.parent().parent().stat.showMessage('Confusion Matrix saved')
        logging.info('ClassVis:Confusion Matrix saved')


# Confusion Matrix Widget
# ========= ====== ======

class CMatrix(QtGui.QWidget):

    def __init__(self, parent, matrix, labels):
        super().__init__()
        self.setParent(parent)
        self.matrix = matrix
        self.labels = labels
        self.generateValues()
        self.setupWidgetLayout()

    def setupWidgetLayout(self):
        n = len(self.labels)

        # List of all Widgets to be added to the Table.
        prdMain = QtGui.QLabel('Predicted Labels')
        prdMain.setObjectName('MainLabel')
        prdMain.setAlignment(QtCore.Qt.AlignCenter)
        prdLabels = [QtGui.QLabel(i) for i in self.labels]
        for lab in prdLabels:
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('SubLabel')

        actMain = QtGui.QLabel('Actual Labels')
        actMain.setObjectName('MainLabel')
        actMain.setAlignment(QtCore.Qt.AlignCenter)
        actLabels = [QtGui.QLabel(i) for i in self.labels]
        for lab in actLabels:
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('SubLabel')

        labelLab = QtGui.QLabel('Label Names')
        labelLab.setObjectName('MainLabel')
        labelLab.setAlignment(QtCore.Qt.AlignCenter)

        mat = []
        for i in range(n):
            row = []
            for j in range(n):
                lab = QtGui.QLabel(str(self.matrix[i, j]))
                lab.setObjectName('InfoLabel')
                lab.setAlignment(QtCore.Qt.AlignCenter)
                row.append(lab)
            mat.append(row)

        blank00 = QtGui.QLabel('')
        blank00.setObjectName('BlankLabel')
        blank01 = QtGui.QLabel('')
        blank01.setObjectName('BlankLabel')
        blank10 = QtGui.QLabel('')
        blank10.setObjectName('BlankLabel')

        # Create Table
        table = QtGui.QTableWidget()
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setRowCount(n+7)
        table.setColumnCount(n+2)

        # Confusion Matrix
        table.setCellWidget(0, 0, blank00)
        table.setCellWidget(0, 1, blank01)
        table.setCellWidget(1, 0, blank10)
        table.setCellWidget(0, 2, prdMain)
        table.setCellWidget(2, 0, actMain)
        table.setCellWidget(1, 1, labelLab)
        for i in range(n):
            table.setCellWidget(1, i+2, prdLabels[i])
            table.setCellWidget(i+2, 1, actLabels[i])
        for i in range(n):
            for j in range(n):
                table.setCellWidget(i+2, j+2, mat[i][j])
        table.setSpan(0, 2, 1, n)
        table.setSpan(2, 0, n, 1)

        # Confusion Matrix Results
        blankn0 = QtGui.QLabel('')
        blankn0.setObjectName('BlankLabel')
        table.setCellWidget(2+n, 0, blankn0)
        table.setSpan(2+n, 0, 1, n+2)

        resMain = QtGui.QLabel('Results')
        resMain.setObjectName('MainLabel')
        resMain.setAlignment(QtCore.Qt.AlignCenter)
        table.setCellWidget(n+3, 0, resMain)
        table.setSpan(n+3, 0, 4, 1)

        for i, result in enumerate(self.values):
            lab = QtGui.QLabel(result)
            lab.setObjectName('SubLabel')
            lab.setAlignment(QtCore.Qt.AlignCenter)
            table.setCellWidget(n+3+i, 1, lab)
            for j, val in enumerate(self.values[result]):
                lab_val = QtGui.QLabel(str(round(val, 6)))
                lab_val.setObjectName('InfoLabel')
                lab_val.setAlignment(QtCore.Qt.AlignCenter)
                table.setCellWidget(n+3+i, j+2, lab_val)

        table.resizeColumnToContents(0)
        table.resizeColumnToContents(1)
        table.resizeRowsToContents()
        table.setMaximumSize(self.tableSize(table))
        table.setMinimumSize(table.maximumSize())
        table.verticalHeader().hide()
        table.horizontalHeader().hide()

        self.table = table

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(table)
        hbox.setMargin(0)
        hbox.setSpacing(0)
        self.setLayout(hbox)

    def save(self, dname):
        fname = path.join(dname, 'conf-matrix.csv')
        with open(fname, 'w') as csvfile:
            wrt = csv.writer(csvfile)
            wrt.writerow(('', *self.labels))
            i = 0
            for row in self.matrix:
                wrt.writerow((self.labels[i], *row))
                i += 1

    def generateValues(self):
        n, n = self.matrix.shape
        TP = self.getTP(n)
        TN = self.getTN(n)
        P = self.getP(n)
        N = self.getN(n)
        sens = []
        spec = []
        accu = []
        prec = []
        for i in range(n):
            sens.append(round(TP[i]/P[i], 3))
            spec.append(round(TN[i]/N[i], 3))
            accu.append(round((TP[i]+TN[i]) / (P[i]+N[i]), 3))
            prec.append(round(TP[i] / (TP[i]-TN[i]+N[i]), 3))
        self.values = {
            'Specificity': sens,
            'Sensitivity': spec,
            'Accuracy': accu,
            'Precision': prec
        }

    def showValues(self):
        source = self.parent().sender()
        vals = self.values[source]
        title = source.text()
        message = []
        for i, val in enumerate(self.labels):
            msg = "{class_lab}: {value}".format(class_lab=val, value=vals[i])
            message.append(msg)
        message = '\n'.join(message)
        txt = "{title}:\n{message}".format(title=title,
                                           message=message)
        self.parent().valLab.setText(txt)

    def getTP(self, n):
        TP = []
        for i in range(n):
            TP.append(self.matrix[i, i])
        return TP

    def getTN(self, n):
        TN = []
        for i in range(n):
            sm = 0
            for j in range(n):
                for k in range(n):
                    if (j != i and k != i):
                        sm += self.matrix[j, k]
            TN.append(sm)
        return TN

    def getP(self, n):
        P = []
        for i in range(n):
            P.append(sum(self.matrix[i,]))
        return P

    def getN(self, n):
        N = []
        for i in range(n):
            sm = 0
            for j in range(n):
                if (j != i):
                    sm += sum(self.matrix[j,])
            N.append(sm)
        return N

    def tableSize(self, table):
        w = 2
        h = 2
        for i in range(table.columnCount()):
            w += table.columnWidth(i)
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        parent_h = self.parent().parent().parent().size().height()
        parent_w = self.parent().parent().parent().size().width()
        if w > parent_w*0.8 :
            w = parent_w*0.8
            h += table.horizontalScrollBar().height() - 20
        return QtCore.QSize(w, h)
