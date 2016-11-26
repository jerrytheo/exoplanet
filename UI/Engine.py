
# Imports
# =======

# Packages
# --------
import sys
from os import path
import logging
import pickle
from PyQt4 import QtGui, QtCore

# UIs
# ---
from .Pages import WorkspaceUI, Start
from .Base import ExoBase


# Widget Control Engine
# ====== ======= ======

class Engine(ExoBase):

    '''
    Controls the flow of control of the app.
        1. Decides the next page to display.
        2. If back pressed, decides the page to display.
        3. Saves and Loads the workspace.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupEngine()
        self.setObjectName('Engine')

    def setupEngine(self):
        '''
        Designs the layout of the Engine.
            1. Sets size to parent size.
            2. Sets position to the center of parent.
            3. Creates the first page to display.
        '''
        self.stat = self.parent().parent().stat
        self.activePage = Start(self)
        self.layout = self.createVBox(self.activePage)
        self.setLayout(self.layout)
        self.setObjectName('Engine')
        self.layout.setMargin(0)

    def startEngine(self):
        '''
        Changes the active page.
            1. Closes the current active page.
            2. Creates the next page to display
            3. Applies the styles required after page creation.
        '''
        self.activePage.close()
        del(self.activePage)
        self.activePage = WorkspaceUI(self)
        self.activePage.setObjectName('ActivePage')
        self.layout.addWidget(self.activePage)

    def paintEvent(self, event):
        """
        Draw Widget characteristics.
        """
        opt = QtGui.QStyleOption()
        opt.initFrom(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
