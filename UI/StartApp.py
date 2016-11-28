'''
ExoPlanet Main Window
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

import sys
import os
from PyQt4 import QtGui, QtCore
from .Chassis import Chassis
from .Base import LicenseDialog


# Application Main Window
# =========== ==== ======


class ExoPlanet(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.workspace = {}
        self.addFonts()
        self.initUI()

    def initUI(self):
        self.stat = self.statusBar()
        self.setCentralWidget(Chassis(self))
        self.createMenus()

        self.setWindowTitle('ExoPlanet')
        self.setWindowIcon(QtGui.QIcon(os.path.join('Info', 'Images',
                                                    'appicon.ico')))
        self.showMaximized()

    def createMenus(self):
        # Menus
        self.menu = self.menuBar()
        self.createFileMenu()
        self.createHelpMenu()

    def createFileMenu(self):
        fileMenu = self.menu.addMenu('File')
        centralWid = self.centralWidget()

        # New Tab
        newAct = QtGui.QAction('New Tab', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(centralWid.newTab)

        # Close Tab
        closeAct = QtGui.QAction('Close Tab', self)
        closeAct.setShortcut('Ctrl+X')
        closeAct.triggered.connect(centralWid.closeTab)

        # Save
        saveAct = QtGui.QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(centralWid.currentWidget().save)

        # Save As
        saveasAct = QtGui.QAction('Save As', self)
        saveasAct.setShortcut('Ctrl+Shift+S')
        saveasAct.triggered.connect(centralWid.currentWidget().saveAs)

        # Open
        openAct = QtGui.QAction('Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(centralWid.currentWidget().load)

        # Quit
        quitAct = QtGui.QAction('Quit', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.triggered.connect(QtGui.QApplication.quit)

        fileMenu.addAction(newAct)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveasAct)
        fileMenu.addSeparator()
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(closeAct)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAct)

    def createHelpMenu(self):
        helpMenu = self.menu.addMenu('Help')
        # Help Menu
        licenseView = QtGui.QAction('License', self)
        licenseView.triggered.connect(self.openLicense)

        helpMenu.addAction(licenseView)

    def addFonts(self):
        fontBaseDir = os.path.join('Info', 'Styles', 'fonts')
        fontdirs = os.listdir(fontBaseDir)
        for fontdir in fontdirs:
            fontdir = os.path.join(fontBaseDir, fontdir)
            fontfiles = os.listdir(fontdir)
            for fontfile in fontfiles:
                if fontfile.split('.')[1] not in ('ttf', 'otf'):
                    continue
                fontpath = os.path.join(fontdir, fontfile)
                QtGui.QFontDatabase.addApplicationFont(fontpath)

    def openLicense(self):
        licensefile = "COPYING.txt"
        ldialog = LicenseDialog(self, licensefile)
        ldialog.setWindowTitle('Exoplanet: License GNU GPLv3')
        ldialog.show()
        ldialog.raise_()
        ldialog.activateWindow()
