
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
