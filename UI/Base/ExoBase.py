'''
ExoPlanet Widget Base Class
Copyright (C) 2016  Abhijit J. Theophilus, Mohinish L. Reddy

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

import sys
from PyQt4 import QtGui, QtCore


# Base Widget
# ==== ======

class ExoBase(QtGui.QWidget):

    """
    Common functions for Widgets defined here.
    createVBox  -- Return QVBoxLayout object with listed objects.
    createHBox  -- Return QHBoxLayout object with listed objects.
    paintEvent  -- Draw Widget characteristics.
    """

    def __init__(self, parent):
        super().__init__(parent)

    def createVBox(self, *objectlist, vbox=None):
        """
        Return QVBoxLayout object with listed objects/spaces added in order to
        a new vbox layout or an existing one.
            1. Creates Vertical Box Layout if vbox is None.
            2. Adds Widgets/Layouts/Spaces in object list
        """
        if vbox is None:
            vbox = QtGui.QVBoxLayout()
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                vbox.addWidget(qitem)
            elif isinstance(qitem, QtGui.QLayout):
                vbox.addLayout(qitem)
            elif isinstance(qitem, int):
                vbox.addStretch(qitem)
        return vbox

    def createHBox(self, *objectlist, hbox=None):
        """
        Return QHBoxLayout object with listed objects/spaces added in order to
        a new hbox layout or an existing one.
            1. Creates Horizontal Box Layout if hbox is None.
            2. Adds Widgets/Layouts/Spaces in object list to the layout.
        """
        if hbox is None:
            hbox = QtGui.QHBoxLayout()
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                hbox.addWidget(qitem)
            if isinstance(qitem, QtGui.QLayout):
                hbox.addLayout(qitem)
            if isinstance(qitem, int):
                hbox.addStretch(qitem)
        return hbox

    def paintEvent(self, event):
        """
        Draw Widget characteristics.
        """
        opt = QtGui.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
