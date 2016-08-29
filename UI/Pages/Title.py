
# Imports
# =======


import sys
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MaterialShadow
from re import match

#-----------------------------------------------------------------------------#

# Getting Workspace Title UI
# ======= ========= ===== ==


class Title(ExoBase):

    '''
    First page of current Workspace. Allows you to set a name for the
    Workspace and select the type of learning to be performed:
        1. Clustering     - Unsupervised learning.
        2. Classification - Supervised learning with discrete labels.
        3. Regression     - Supervised learning with continuous labels.
    '''

    def __init__(self, parent):
        super().__init__(parent=parent)
        layout = self.createLayout()
        self.initUI(layout)

        
    def initUI(self, layout):
        '''
        Initialise the Title page.
            1. Sets layout for AlgoFile.
            2. Connects the clicked signals for nextButton.
        '''

        super().initUI(layout)
        self.clusButton.clicked.connect(self.parent().buttonClicked)
        self.clasButton.clicked.connect(self.parent().buttonClicked)
        self.regrButton.clicked.connect(self.parent().buttonClicked)
                
        
    def createLayout(self):
        '''
        Create the layout for the Title page.
            1. Creates a QLineEdit to enter Workspace name.
            2. Creates three QPushButtons to select either Clustering, Classification
               or Regression.
        '''

        # Title part of page.
        self.enterTitle = QtGui.QLineEdit()
        self.enterTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.enterTitle.setPlaceholderText(
            'Only alphanumeric characters. Must start with an alphabet.'
        )
        hboxLE = self.hboxCreate(220, self.enterTitle, 220)
        titleCard = self.createCard('Workspace Name', hboxLE)

        # Selecting the Analysis type.
        self.clusButton = QtGui.QPushButton('Clustering')
        self.clasButton = QtGui.QPushButton('Classification')
        self.regrButton = QtGui.QPushButton('Regression')
        
        self.clusButton.setStatusTip('Unsupervised learning')
        self.clasButton.setStatusTip(
                'Supervised learning for discrete labels.'
        )
        self.regrButton.setStatusTip(
                'Supervised learning for continuous labels.'
        )

        btns = [self.clusButton, self.clasButton, self.regrButton]
        for btn in btns:
            btn.setFocusPolicy(QtCore.Qt.NoFocus)
            btn.setGraphicsEffect(MaterialShadow(self))
        vboxBtn = self.vboxCreate(35, *btns)
        vboxBtn.setSpacing(15)

        hboxBtn = self.hboxCreate(400, vboxBtn, 400)
        typeCard = self.createCard('Analysis Type', hboxBtn)
        return self.createCardLayout(titleCard, typeCard)

    
    def checkVal(self):
        '''
        Checks if valid name is entered.
            1. Must start with an alphabet.
            2. Must have only Alphanumeric characters.
        '''
        
        title = self.enterTitle.text()
        
        if match('[a-zA-Z]+[a-zA-Z0-9_]*$', title) is None:
            return None
        
        else: return title
            
        
#-----------------------------------------------------------------------------#