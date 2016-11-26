
# Imports
# =======


# Importing Packages
import sys
import os
from PyQt4 import QtGui, QtCore

# Importing Windows
from .Chassis import Chassis
from .Base import TextFileDialog


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
        self.createMenu()

        self.setWindowTitle('ExoPlanet')
        self.setWindowIcon(QtGui.QIcon(os.path.join('Info', 'Images',
                                                    'appicon.ico')))
        self.showMaximized()

    def createMenu(self):
        # Menus
        self.menu = self.menuBar()
        fileMenu = self.menu.addMenu('File')
        helpMenu = self.menu.addMenu('Help')

        # Actions.
        # Quit
        quitAct = QtGui.QAction('Quit', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.triggered.connect(QtGui.QApplication.quit)
        # New Tab
        newAct = QtGui.QAction('New Tab', self)
        newAct.setShortcut('Ctrl+N')
        newAct.triggered.connect(self.centralWidget().newTab)
        # Close Tab
        closeAct = QtGui.QAction('Close Tab', self)
        closeAct.setShortcut('Ctrl+X')
        closeAct.triggered.connect(self.centralWidget().closeTab)

        fileMenu.addAction(newAct)
        fileMenu.addAction(closeAct)
        fileMenu.addAction(quitAct)

        # Help Menu
        readmeView = QtGui.QAction('View Readme', self)
        readmeView.triggered.connect(self.openReadme)
        licenseView = QtGui.QAction('View License', self)
        licenseView.triggered.connect(self.openLicense)

        helpMenu.addAction(readmeView)
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

    def openReadme(self):
        readmefile = "README.txt"
        TextFileDialog(self, readmefile, "Readme")

    def openLicense(self):
        readmefile = "COPYING.txt"
        TextFileDialog(self, readmefile, "License")
