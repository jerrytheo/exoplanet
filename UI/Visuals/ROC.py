
# Imports
# =======

from os import path
from sklearn.metrics import roc_curve
from sklearn.multiclass import OneVsRestClassifier
from ..Base import ExoCanvas, ComboBox
from PyQt4 import QtGui, QtCore


# Classification Visuals Widget
# =============================

class ROC(QtGui.QDialog):

    def __init__(self, parent, workspace):
        super().__init__(parent)
        self.roc = self.generateROCValues(workspace)
        self.setupDialogLayout()
        if self.roc is not None:
            self.setInitialState()

    def setInitialState(self):
        self.replot(0)
        self.plotCombo.currentIndexChanged[int].connect(self.replot)

    def setupDialogLayout(self):
        # Build Main Visual widgets
        if self.roc is not None:
            self.rocCanvas = ROCCanvas(self, self._labels)
            self.rocCanvas.setFixedSize(500, 500)
        else:
            self.rocCanvas = QtGui.QLabel('ROC Unavailable.', self)
            self.rocCanvas.setAlignment(QtCore.Qt.AlignCenter)

        # Build combo box
        self.plotCombo = ComboBox()
        for i in range(len(self._labels)):
            self.plotCombo.addItem('Class: {0}'.format(self._labels[i]))
        self.plotCombo.addItem('All Classes')
        self.plotCombo.setStatusTip('Plot ROC for specified class.')
        plotLayout = QtGui.QHBoxLayout()
        plotLayout.addSpacing(15)
        plotLayout.addWidget(self.plotCombo)
        plotLayout.addSpacing(15)

        # Save Button
        savebtn = QtGui.QPushButton('Save', self)
        savebtn.clicked.connect(self.saveVisual)

        # Build ROC Layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.rocCanvas)
        layout.addSpacing(25)
        layout.addLayout(plotLayout)
        layout.addStretch(1)
        layout.addWidget(savebtn, 1, QtCore.Qt.AlignHCenter)
        layout.setMargin(10)

        self.setLayout(layout)

    def generateROCValues(self, workspace):
        train_data = workspace['Data'].post_data['Training'].data
        train_labels = workspace['Data'].post_data['Training'].labels
        ovr_clf = OneVsRestClassifier(workspace['Model'].model)
        ovr_clf.fit(train_data, train_labels)

        X = workspace['Data'].post_data['Testing'].data
        y_true = workspace['Data'].post_data['Testing'].labels
        y_pred = ovr_clf.predict_proba(X)
        self._labels = workspace['Data'].post_data['Labels']
        rocVals = {}
        try:
            for i in range(y_pred.shape[1]):
                fpr, tpr, thr = roc_curve(y_true, y_pred[:, i], pos_label=i)
                rocVals[self._labels[i]] = (fpr, tpr)
        except Exception as err:
            rocVals = None
        return rocVals

    def replot(self, ind):
        if ind == len(self._labels):
            self.rocCanvas.showAll(self.roc)
        else:
            lab = self._labels[ind]
            self.rocCanvas.updatePlot(*self.roc[lab], lab)

    def saveVisual(self):
        home = path.expanduser('~')
        dname = QtGui.QFileDialog.getExistingDirectory(self, 'Save Folder',
                                                       home)
        for lab in self._labels:
            self.rocCanvas.updatePlot(*self.roc[lab], lab)
            self.rocCanvas.save(dname, lab)
        self.rocCanvas.showAll(self.roc)
        self.rocCanvas.save(dname, 'All Classes')

        self.parent().stat.showMessage('ROC saved')

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


# ROC plot Canvas
# === ==== ======


class ROCCanvas(ExoCanvas):

    def __init__(self, parent, labels):
        super().__init__(parent, 75)
        self.initFigure([0, 1], [0, 1])
        self.figure.subplots_adjust(left=0.1, bottom=0.2, top=0.975,
                                    right=0.97)
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
            for i in range(1, len(self.axes.lines)):
                self.axes.lines.remove(self.axes.lines[-1])
        self.axes.plot(fpr, tpr, '-', color=color)
        self.line = True
        self.draw()

    def showAll(self, rocdata):
        if self.line:
            for i in range(1, len(self.axes.lines)):
                self.axes.lines.remove(self.axes.lines[i])
        for class_lab in rocdata:
            ind = self.labels.index(class_lab)
            data = rocdata[class_lab]
            color = self.colors[ind % 6]
            self.axes.plot(data[0], data[1], '-', color=color)
            self.line = True
            self.draw()

    def save(self, dname, classname):
        figname = 'roc-class ' + classname
        super().save(dname, figname)
