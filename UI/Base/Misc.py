
# Imports
# =======

import sys
from os import path
from PyQt4 import QtGui, QtCore


# Get Integer Widget
# === ======= ======

class MultiInput(QtGui.QWidget):

    '''
    Widget that allows a combination of a QComboBox and a QLineEdit that allows
    you to further enter integral or floating point values corresponding to a
    selection made in the QComboBox.
    '''

    def __init__(self, parent, intIP=True, floatIP=True, **kwargs):
        super().__init__(parent)
        self.opts = kwargs['opts']
        self.vals = kwargs['vals']
        layout = self.createLayout(intIP, floatIP, **kwargs)
        self.setLayout(layout)
        try:
            self.setDefault(kwargs)
        except:
            pass
        self.show()

    def createLayout(self, intIP, floatIP, **info):
        '''
        Creates the layout of the widget.
            1. Creates a QComboBox and adds the respective items.
            2. If an item needs an integral or floating point input, creates a
               QLineEdit and sets a validator to ensure valid input.
        '''
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.setMargin(0)
        self._comb = ComboBox(self)
        self._comb.addItems(self.opts)
        self._comb.currentIndexChanged[int].connect(self.changeUI)
        grid.addWidget(self._comb, 0, 0)

        if intIP:
            self.opts.append('int')
            self._comb.addItem('Enter Integer')
            self._edit_int = QtGui.QLineEdit(self)
            input_valid = QtGui.QIntValidator()
            if 'min' in info:
                input_valid.setBottom(info['min'])
            if 'max' in info:
                input_valid.setTop(info['max'])

            self._edit_int.setValidator(input_valid)
            if 'default' in info:
                self._edit_int.setText(str(info['default']))
            self._edit_int.setVisible(False)
            grid.addWidget(self._edit_int, 0, 1)

        if floatIP:
            self.opts.append('float')
            self._comb.addItem('Enter Fraction')
            input_valid = QtGui.QDoubleValidator()
            input_valid.setDecimals(6)
            if 'fmin' in info:
                input_valid.setBottom(info['fmin'])
            if 'fmax' in info:
                input_valid.setTop(info['fmax'])

            self._edit_float = QtGui.QLineEdit(self)
            self._edit_float.setValidator(input_valid)
            if 'fdefault' in info:
                self._edit_float.setText(str(info['fdefault']))
            grid.addWidget(self._edit_float, 0, 1)
            self._edit_float.setVisible(False)

        return grid

    def changeUI(self, index):
        '''
        Displays the QLineEdit widget only if needed and disables it otherwise.
        '''
        if self.opts[index] == 'int':
            self._edit_int.setVisible(True)
            if 'float' in self.opts:
                self._edit_float.setVisible(False)
        elif self.opts[index] == 'float':
            self._edit_float.setVisible(True)
            if 'int' in self.opts:
                self._edit_int.setVisible(False)
        else:
            if 'int' in self.opts:
                self._edit_int.setVisible(False)
            if 'float' in self.opts:
                self._edit_float.setVisible(False)

    def getValue(self):
        '''
        Read either the integer, float or selected index based on option
        selected.
        '''
        index = self._comb.currentIndex()
        if self.opts[index] == 'int':
            val = self._edit_int.text()
            chk = self._edit_int.validator()
            if chk.validate(val, 0)[0] == 2:
                return int(val)
        elif self.opts[index] == 'float':
            val = self._edit_float.text()
            chk = self._edit_float.validator()
            if chk.validate(val, 0)[0] == 2:
                return float(val)
        else:
            return self.vals[index]

        raise ValueError

    def setDefault(self, info):
        '''
        Sets the default state of the widget.
        '''
        if isinstance(info['default'], int):
            ind = self.opts.index('int')
            self._comb.setCurrentIndex(ind)
            self._edit_int.setText(str(info['default']))
        elif isinstance(info['default'], float):
            ind = self.opts.index('float')
            self._comb.setCurrentIndex(ind)
            self._edit_float.setText(str(info['default']))
        elif isinstance(info['default'], str):
            ind = self.opts.index(info['default'])
            self._comb.setCurrentIndex(ind)


# Material Shadow
# ===============

class MaterialShadow(QtGui.QGraphicsDropShadowEffect):

    def __init__(self, parent, color='#ACACAC'):
        super().__init__(parent)
        self.setColor(QtGui.QColor(color))
        self.setOffset(0, 3)
        self.setBlurRadius(10)


# Browse Files
# ============

class LoadFileWidget(QtGui.QWidget):

    def __init__(self, parent, default=None):
        super().__init__(parent)
        fpath = path.expanduser('~') if default is None else default
        self.createLayout(fpath)

    def createLayout(self, fpath):
        fpath = 'C:/Users/Jerry/Projects/datasets/Datafiles/' \
            + 'Combined Cycle Power Plant/ccpp.csv'
        self.ledit = QtGui.QLineEdit(fpath, self)
        pbutn = QtGui.QPushButton('Browse', self)
        pbutn.clicked.connect(self.loadFile)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.ledit)
        layout.addWidget(pbutn)
        layout.setMargin(0)
        layout.setSpacing(20)
        self.setLayout(layout)

    def loadFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select Data file.',
                                                  self.ledit.text(),
                                                  filter='CSV (*.csv) | *.csv')
        if fname != '':
            self.ledit.setText(fname)

    def getFilePath(self):
        fpath = self.ledit.text()
        if path.isfile(fpath) and fpath.lower().endswith('.csv'):
            return fpath
        else:
            return None

    def setFilePath(self, fpath):
        if path.isfile(fpath) or path.isdir(fpath):
            self.ledit.setText(fpath)


# Combo Box
# =========

class ComboBox(QtGui.QComboBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lview = QtGui.QListView(self)
        lview.setObjectName('ComboView')
        self.setView(lview)
        self.setStyle(QtGui.QStyleFactory.create("Polyester"))


# Slider with Labels
# ==================

class LabelledSlider(QtGui.QWidget):

    def __init__(self, parent, label1, label2):
        super().__init__(parent)
        self.setupLayout(label1, label2)
        self.slider.valueChanged[int].connect(self.changeLabels)

    def setupLayout(self, label1, label2):
        self.val1 = QtGui.QLabel('70%', self)
        self.val1.setObjectName('ComboValue')
        self.val2 = QtGui.QLabel('30%', self)
        self.val2.setObjectName('ComboValue')

        self.label1 = QtGui.QLabel(label1, self)
        self.label1.setObjectName('ComboLabel')
        self.label2 = QtGui.QLabel(label2, self)
        self.label2.setObjectName('ComboLabel')

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(10, 90)
        self.slider.setValue(70)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.val1)
        layout.addWidget(self.slider)
        layout.addWidget(self.val2)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def changeLabels(self, value):
        self.val1.setText('{0}%'.format(value))
        self.val2.setText('{0}%'.format(100 - value))

    def value(self):
        return self.slider.value()
