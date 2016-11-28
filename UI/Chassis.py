'''
ExoPlanet Chassis
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

# Packages
# --------
from PyQt4 import QtGui, QtCore

# UIs
# ---
from .Engine import Engine


# Engine Support Widget
# ====== ======= ======

class Chassis(QtGui.QTabWidget):

    '''
    Widget that produces tabs.
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.setProperties()
        self.newTab()
        self.setObjectName('Chassis')

    def setProperties(self):
        '''
        Sets properties of the tab.
        '''
        self.setUsesScrollButtons(True)
        tBar = self.tabBar()
        tBar.setTabsClosable(True)
        tBar.tabCloseRequested[int].connect(self.closeTab)
        tBar.setFocusPolicy(QtCore.Qt.NoFocus)
        tBar.setShape(QtGui.QTabBar.TriangularNorth)

    def newTab(self):
        '''
        Creates a new tab.
        '''
        self.addTab(Engine(self), 'Untitled')

    def closeTab(self, index=None):
        '''
        Closes a tab. If it's the last tab, creates a new tab in its place.
        '''
        if index is None:
            index = self.currentIndex()
        wd = self.widget(index)
        wd.close()
        del(wd)
        self.removeTab(index)
        if (self.tabBar().count() == 0):
            self.newTab()
