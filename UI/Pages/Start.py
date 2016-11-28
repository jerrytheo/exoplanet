'''
ExoPlanet Start Page
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


from os import path
from PyQt4 import QtGui, QtCore, Qt
from ..Base import ExoBase


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
        self.setupWidget()
        self.makeConnections()

    def makeConnections(self):
        '''
        Connects the clicked signals for createButton and loadButton.
        '''
        self.createButton.clicked.connect(self.parent().startEngine)
        self.loadButton.clicked.connect(self.parent().load)

    def setupWidget(self):
        '''
        Creates the layout of the Start page.
        '''
        # Create Widgets.
        self.createButton = QtGui.QPushButton('Start a new Project.')
        self.loadButton = QtGui.QPushButton('Pick up where I left off.')

        self.createButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loadButton.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create Logo
        logoImage = QtGui.QPixmap(path.join('Info', 'Images',
                                            'logo.png'), 'PNG')
        logoImage = logoImage.scaledToHeight(200,
                                             QtCore.Qt.SmoothTransformation)
        logo = Qt.QLabel()
        logo.setPixmap(logoImage)
        shadow = QtGui.QGraphicsDropShadowEffect(self)
        shadow.setColor(QtGui.QColor('#ACACAC'))
        shadow.setOffset(0, 3)
        shadow.setBlurRadius(10)
        logo.setGraphicsEffect(shadow)

        # Create college logo
        clogoImage = QtGui.QPixmap(path.join('Info', 'Images',
                                             'pesit.png'), 'PNG')
        clogoImage = clogoImage.scaledToHeight(125,
                                               QtCore.Qt.SmoothTransformation)
        clogo = QtGui.QLabel()
        clogo.setPixmap(clogoImage)

        ques = QtGui.QLabel('What would you like to do?')
        ques.setObjectName('QuesLabel')

        # Layout for the question and choices.
        vboxButton = QtGui.QVBoxLayout()
        vboxButton.addStretch(1)
        vboxButton.addWidget(ques)
        vboxButton.addStretch(2)
        vboxButton.addWidget(self.createButton)
        vboxButton.addWidget(self.loadButton)
        vboxButton.setSpacing(20)
        hboxButton = QtGui.QHBoxLayout()
        hboxButton.addStretch(1)
        hboxButton.addLayout(vboxButton)
        hboxButton.addStretch(1)

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

        self.setLayout(hbox)
