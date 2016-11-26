
# Imports
# =======


import sys
from ..Base import ExoBase
from .LeftPane import LeftPane
from PyQt4 import QtGui, QtCore


# Workspace UI
# ========= ==

class WorkspaceUI(ExoBase):

    def __init__(self, parent, defaultState=None):
        super().__init__(parent=parent)
        self.stat = self.parent().stat
        self.setupWidget(defaultState)

    def setupWidget(self, defaultState):
        '''
        Create the layout for the Workspace.
        '''
        layout = QtGui.QHBoxLayout()
        layout.addWidget(LeftPane(self, defaultState), 1)

        # Temporary
        layout.addWidget(QtGui.QLabel('Right Pane', self), 1)

        self.setLayout(layout)
