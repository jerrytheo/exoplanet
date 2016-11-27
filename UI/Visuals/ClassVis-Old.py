
# Imports
# =======

from os import path
import csv
from ..Base import ExoCanvas, ExoBase, MaterialShadow
from PyQt4 import QtGui, QtCore
import logging


#-----------------------------------------------------------------------------#

# Classification Visuals Widget
# ============== ======= ======


class ClassVis(ExoBase):

    def __init__(self, parent, visuals):
        super().__init__(parent)
        self.roc  = visuals['ROC Curves']
        self.conf = visuals['Confusion Matrix']
        self.labels = visuals['Labels']
        self.accuracy = visuals['Accuracy']
        layout = self.createLayout()
        self.initUI(layout)
    

    def initUI(self, layout):
        super().initUI(layout, scroll=False)
        self.replot(0)
        self.plotCombo.currentIndexChanged[int].connect(self.replot)


    def createLayout(self):
        # Build Main Visual widgets
        self.rocCanvas = ROCCanvas(self, self.labels)
        self.rocCanvas.setFixedSize(700, 700)
        self.confMat = CMatrix(self, self.conf, self.labels)
        
        # Build combo box
        self.plotCombo = QtGui.QComboBox()
        for i in range(len(self.labels)):
            self.plotCombo.addItem('Class {name}'.format(name=self.labels[i]))
        self.plotCombo.setStatusTip('Plot ROC for specified class.')
        
        # Build ROC Layout
        hboxROC = self.hcenter(self.rocCanvas)
        vboxROC = self.vboxCreate(15, hboxROC, 15,
                self.hcenter(self.plotCombo))
        self.rocCard = self.createCard('ROC Curve', vboxROC)
        
        # Build Conf layout
        vboxConf = self.vboxCreate(self.confMat)
        self.confCard = self.createCard('Confusion Matrix', vboxConf)

        # Build Accuracy layout
        accLab = QtGui.QLabel(str(self.accuracy * 100) + '%')
        accLab.setObjectName('Accuracy')
        self.accCard = self.createCard('Accuracy', self.hcenter(accLab))

        return self.createCardLayout(self.accCard, self.rocCard, self.confCard)


    def replot(self, ind):
        lab = self.labels[ind]
        logging.info('ClassVis:plotCombo index ' + str(ind) + ' selected.')
        self.rocCanvas.updatePlot(*self.roc[lab], lab)
    
    
    def saveVisual(self):
        home = path.expanduser('~')
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Save Folder',
                home)
        
        self.confMat.save(dname)
        for btn in self.plotButtons:
            btnI = self.plotButtons.index(btn)
            lab = self.labels[btnI]
            self.rocCanvas.updatePlot(*self.roc[lab], lab)
            self.rocCanvas.save(dname, lab)

        self.parent().parent().stat.showMessage('Visuals Saved')
        logging.info('ClassVis:Visuals Saved')


    def createFormWidget(self, *args, heads=False):
        hbox = QtGui.QHBoxLayout()
        for i in args:
            lab = QtGui.QLabel(str(i))
            lab.setAlignment(QtCore.Qt.AlignCenter)
            if heads:
                lab.setObjectName('FormLabel')
            hbox.addWidget(lab)
        hbox.setMargin(0)
        wid = QtGui.QWidget()
        wid.setLayout(hbox)
        return wid


#-----------------------------------------------------------------------------#

# ROC plot Canvas
# === ==== ======


class ROCCanvas(ExoCanvas):
    
    def __init__(self, parent, labels):
        super().__init__(parent, 75)
        self.initFigure([0,1], [0,1])
        self.figure.subplots_adjust(left=0.07, bottom=0.2, top=0.975,
                right=0.985)
        self.axes.set_xlabel('False Positive Rate')
        self.axes.set_ylabel('True Positive Rate')
        self.axes.hold(True)
        self.line = False
        self.labels = labels
        self.colors = ['b', 'g', 'r', 'y', 'm', 'c']
        
        
    def updatePlot(self, fpr, tpr, classname):
        ind = self.labels.index(classname)
        color = self.colors[ind % 6]
        if self.line:
            self.axes.lines.remove(self.axes.lines[1])
        self.axes.plot(fpr, tpr, '-', color=color)
        self.line = True
        self.draw()
        
    
    def save(self, dname, classname):
        figname = 'roc-class ' + classname
        super().save(dname, figname)    

        
#-----------------------------------------------------------------------------#

# Confusion Matrix Widget
# ========= ====== ======

class CMatrix(QtGui.QWidget):
    
    def __init__(self, parent, matrix, labels):
        super().__init__()
        self.setParent(parent)
        self.matrix = matrix
        self.labels = labels
        self.generateValues()
        layout = self.createLayout()
        self.initUI(layout)
        
    
    def initUI(self, layout):
        self.setLayout(layout)
        
    
    def createLayout(self):
        n = len(self.labels)
        
        # List of all Widgets to be added to the Table.
        prdMain = QtGui.QLabel('Predicted Labels')
        prdMain.setObjectName('MainLabel')
        prdMain.setAlignment(QtCore.Qt.AlignCenter)
        prdLabels = [ QtGui.QLabel(i) for i in self.labels ]
        for lab in prdLabels:
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')

        actMain = QtGui.QLabel('Actual Labels')
        actMain.setObjectName('MainLabel')
        actMain.setAlignment(QtCore.Qt.AlignCenter)
        actLabels = [ QtGui.QLabel(i) for i in self.labels ]
        for lab in actLabels:
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setObjectName('MainLabel')


        labelLab = QtGui.QLabel('Label Names')
        labelLab.setObjectName('MainLabel')
        labelLab.setAlignment(QtCore.Qt.AlignCenter)
        
        mat = []
        for i in range(n):
            row = []
            for j in range(n):
                lab = QtGui.QLabel(str(self.matrix[i, j]))
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
            lab.setObjectName('MainLabel')
            lab.setAlignment(QtCore.Qt.AlignCenter)
            table.setCellWidget(n+3+i, 1, lab)
            for j, val in enumerate(self.values[result]):
                lab_val = QtGui.QLabel( str(round(val, 6)) )
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

        return hbox
    
    
    def save(self, dname):
        fname = path.join(dname, 'conf-matrix.csv')
        with open(fname, 'w') as csvfile:
            wrt = csv.writer(csvfile)
            wrt.writerow( ('', *self.labels) )
            i = 0
            for row in self.matrix:
                wrt.writerow( (self.labels[i], *row) )
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
            sens.append( round(TP[i]/P[i], 3) )
            spec.append( round(TN[i]/N[i], 3) )
            accu.append( round((TP[i]+TN[i]) / (P[i]+N[i]), 3) )
            prec.append( round(TP[i] / (TP[i]-TN[i]+N[i]), 3) )
        self.values = {
            'Specificity' : sens,
            'Sensitivity' : spec,
            'Accuracy'    : accu,
            'Precision'   : prec
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
            TP.append(self.matrix[i,i])
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
                if (j != i): sm += sum(self.matrix[j,])
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


#-----------------------------------------------------------------------------#