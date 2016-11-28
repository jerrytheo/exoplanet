
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
        #saveAct.triggered.connect(centralWid.currentWidget().save(new=False))

        # Save As
        saveasAct = QtGui.QAction('Save As', self)
        saveasAct.setShortcut('Ctrl+Shift+S')
        #saveasAct.triggered.connect(centralWid.currentWidget().save(new=True))

        # Open
        openAct = QtGui.QAction('Open', self)
        openAct.setShortcut('Ctrl+O')
        #openAct.triggered.connect(centralWid.currentWidget().load())

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
