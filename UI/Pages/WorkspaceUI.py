
# Imports
# =======


import sys
from ..Base import ExoBase
from .PreAnalysisForm import PreAnalysisForm
from .PostAnalysisOptions import PostAnalysisOptions
from PyQt4 import QtGui, QtCore
from Core.ModelBuild import Model


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

        self.rightScroll = QtGui.QScrollArea(self)
        self.rightScroll.setObjectName('RightScroll')
        self.post_options = QtGui.QLabel('Model not built.')
        self.post_options.setAlignment(QtCore.Qt.AlignCenter)
        self.post_options.setObjectName('Placeholder')
        self.rightScroll.setWidget(self.post_options)
        self.rightScroll.setWidgetResizable(True)
        layout.addWidget(self.rightScroll, 1)

        self.setLayout(layout)

    def analyseData(self):
        workspace = self.pre_form.value()
        mdl = Model(workspace['Algorithm'], workspace['Parameters'])

        if workspace['Learning Type'] == 'Clustering':
            mdl.fitData(workspace['Data'].post_data)
            pred = mdl.predictData(workspace['Data'].post_data)

        else:
            mdl.fitData(workspace['Data'].post_data['Training'].data,
                        workspace['Data'].post_data['Training'].labels)
            pred = mdl.predictData(workspace['Data'].post_data['Testing'].data)

        workspace['Model'] = mdl
        workspace['Predicted'] = pred
        self.post_options.close()
        del(self.post_options)
        self.post_options = PostAnalysisOptions(self, workspace)
        self.rightScroll.setWidget(self.post_options)
