
# Imports
# =======

import sys
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
        grid.setSpacing(0)
        grid.setMargin(0)
        self._comb = QtGui.QComboBox(self)
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
# -------- ------

class MaterialShadow(QtGui.QGraphicsDropShadowEffect):

    def __init__(self, parent, color='#ACACAC'):
        super().__init__(parent)
        self.setColor(QtGui.QColor(color))
        self.setOffset(0, 3)
        self.setBlurRadius(10)
