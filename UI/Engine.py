
# Imports
# =======

# Packages
# --------
import pickle
from os import path
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

    def startEngine(self, defaultState):
        '''
        Changes the active page.
            1. Closes the current active page.
            2. Creates the next page to display
            3. Applies the styles required after page creation.
        '''
        self.activePage.close()
        del(self.activePage)
        if defaultState is False:
            self.activePage = WorkspaceUI(self, None)
        else:
            self.activePage = WorkspaceUI(self, defaultState)
        self.activePage.setObjectName('ActivePage')
        self.layout.addWidget(self.activePage)

    def save(self):
        if isinstance(self.activePage, Start):
            self.stat.showMessage('You can\'t save here.')
            return
        else:
            self.activePage.save(False)

    def saveAs(self):
        if isinstance(self.activePage, Start):
            self.stat.showMessage('You can\'t save here.')
            return
        else:
            self.activePage.save(True)

    def load(self):
        '''
        Loads an existing Workspace.
        '''
        home = path.expanduser('~')
        filter_ = ('Exoplanet Workspace (*.exws)')
        fname = QtGui.QFileDialog.getOpenFileName(self, 'File location', home,
                                                  filter=filter_)
        with open(fname, 'rb') as workfile:
            defaultState = pickle.load(workfile)

        ftitle = path.splitext(path.split(fname)[1])[0]
        ind = self.parent().parent().currentIndex()
        self.parent().parent().setTabText(ind, ftitle)
        self.startEngine(defaultState)
