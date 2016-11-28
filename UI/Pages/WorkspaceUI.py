
# Imports
# =======

import os
import pickle
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
        self.built = False
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
        if defaultState is None:
            self.post_options = QtGui.QLabel('Model not built.')
            self.post_options.setAlignment(QtCore.Qt.AlignCenter)
            self.post_options.setObjectName('Placeholder')
        else:
            self.post_options = PostAnalysisOptions(self, defaultState)
            self.built = True
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
        self.built = True

    def save(self, newfile=True):
        if not self.built:
            self.stat.showMessage('Build the model first.')
            return
        if 'Filename' not in self.post_options.workspace:
            newfile = True

        if newfile is True:
            home = os.path.expanduser('~')
            filter_ = ('Exoplanet Workspace (*.exws)')
            dtitle = 'Save As' if newfile else 'Save'
            fname = QtGui.QFileDialog.getSaveFileName(self, dtitle, home,
                                                      filter=filter_)
        else:
            fname = self.post_options.workspace['Filename']
        if not fname:
            self.stat.showMessage('File not saved.')
            return
        with open(fname, 'wb') as workfile:
            try:
                pickle.dump(self.post_options.workspace, workfile, -1)
                self.stat.showMessage('Saved Workspace.')
                self.post_options.workspace['Filename'] = fname
                ftitle = os.path.splitext(os.path.split(fname)[1])[0]
                ind = self.parent().parent().currentIndex()
                self.parent().parent().parent().setTabText(ind, ftitle)
            except pickle.PicklingError as err:
                self.stat.showMessage('Save failed. Try again.')
