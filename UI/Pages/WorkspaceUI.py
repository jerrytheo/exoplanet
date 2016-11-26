
# Imports
# =======


import sys
from ..Base import ExoBase
from .PreAnalysisForm import PreAnalysisForm
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

        leftScroll = QtGui.QScrollArea(self)
        leftScroll.setObjectName('LeftScroll')
        self.pre_form = PreAnalysisForm(self, defaultState)
        leftScroll.setWidget(self.pre_form)
        leftScroll.setWidgetResizable(True)
        layout.addWidget(leftScroll, 1)

        self.post_form = QtGui.QLabel('Post Form')
        self.post_form.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.post_form, 1)

        self.setLayout(layout)

    def analyseData(self):
        model_info = self.pre_form.value()
