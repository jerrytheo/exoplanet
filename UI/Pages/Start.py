
# Imports
# =======


from os import path
import sys
from PyQt4 import QtGui, QtCore, Qt
from ..Base import ExoBase, MaterialShadow


#-----------------------------------------------------------------------------#

# Start App UI
# ===== === ==


class Start(ExoBase):

    '''
    Initial page of the app. Allows you to either:
        1. Start a new Workspace.
        2. Load an existing Workspace.
    '''
    
    def __init__(self, parent):
        super().__init__(parent)
        layout = self.createLayout()
        self.initUI(layout)

    
    def initUI(self, layout):
        '''
        Initialise UI for the evaluations page.
            1. Sets layout.
            2. Connects the clicked signals for createButton and loadButton.
        '''
        super().initUI(layout, scroll=False)
        self.createButton.clicked.connect(self.parent().buttonClicked)
        self.loadButton.clicked.connect(self.parent().buttonClicked)
    
    
    def createLayout(self):
        '''
        Creates the layout of the Start page.
            1. Creates a QPushButton to start a new Workspace.
            2. Creates a QPushButton to load an existing Workspace.
        '''
        # Create Widgets.
        self.createButton = QtGui.QPushButton('Create a new Workspace.')
        self.loadButton = QtGui.QPushButton('Load an existing Workspace.')
        
        self.createButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.createButton.setObjectName('LabelStyle')

        self.loadButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loadButton.setObjectName('LabelStyle')
    
        # Create Logo
        logoImage = QtGui.QPixmap(path.join('Info', 'Images',
                'logo.png'), 'PNG')
        logoImage = logoImage.scaledToHeight(200,
                QtCore.Qt.SmoothTransformation)
        logo = Qt.QLabel()
        logo.setPixmap(logoImage)
        logo.setGraphicsEffect(MaterialShadow(self))

        # Create college logo
        clogoImage = QtGui.QPixmap(path.join('Info', 'Images',
                'pesit.png'), 'PNG')
        clogoImage = clogoImage.scaledToHeight(125,
                QtCore.Qt.SmoothTransformation)
        clogo = QtGui.QLabel()
        clogo.setPixmap(clogoImage)

        ques = QtGui.QLabel('What would you like to do?')
        ques.setObjectName('QuesLabel')

        vboxButton = self.vcenter(ques, 2, self.createButton, self.loadButton)
        vboxButton.setSpacing(20)
        hboxButton = self.hcenter(vboxButton)

        vboxCLogo = QtGui.QVBoxLayout()
        vboxCLogo.addWidget(clogo)
        vboxCLogo.addStretch(4)
        vboxCLogo.setSpacing(0)
        vboxCLogo.setMargin(20)

        vboxLogoBtn = QtGui.QVBoxLayout()
        vboxLogoBtn.addStretch(2)
        vboxLogoBtn.addWidget(logo)
        vboxLogoBtn.addStretch(2)
        vboxLogoBtn.addLayout(hboxButton)
        vboxLogoBtn.addStretch(1)
        vboxLogoBtn.setSpacing(15)
        vboxLogoBtn.setMargin(0)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(3)
        hbox.addLayout(vboxLogoBtn, 2)
        hbox.addStretch(2)
        hbox.addLayout(vboxCLogo)

        return hbox


#-----------------------------------------------------------------------------#