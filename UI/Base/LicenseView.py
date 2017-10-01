'''
ExoPlanet License View
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


from PyQt4 import QtGui, QtCore
from .ExoBase import ExoBase


# Text File Dialog
# ==== ==== ======

class LicenseDialog(QtGui.QDialog):

    def __init__(self, parent, fpath):
        super().__init__(parent)
        self.setupDialogLayout(fpath)

    def setupDialogLayout(self, fpath):
        try:
            with open(fpath) as txtfile:
                text = txtfile.read()
        except Exception as err:
            text = 'License not found.\n' + \
                'Please visit <http://www.gnu.org/licenses/>'

        textbox = QtGui.QPlainTextEdit(text, self)
        textbox.setReadOnly(True)
        textbox.setObjectName("TextBox")
        textbox.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        scr = QtGui.QScrollArea()
        scr.setWidget(textbox)
        scr.setWidgetResizable(True)
        scr.setMinimumWidth(textbox.width())
        scr.setMinimumHeight(500)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(scr)

        self.setLayout(vbox)
