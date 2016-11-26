
# Imports
# =======


from PyQt4 import QtGui, QtCore
from .ExoBase import ExoBase


#-----------------------------------------------------------------------------#

# Text File Dialog
# ==== ==== ======

class TextFileDialog(QtGui.QDialog):
    
    def __init__(self, parent, textfile, label):
        super().__init__(parent)
        layout = self.createLayout(textfile, label)
        self.initUI(layout)


    def createLayout(self, textfile, label):
        wid = ExoDialogContent(self, textfile, label)
        scr = QtGui.QScrollArea()
        scr.setWidget(wid)
        scr.setWidgetResizable(True)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(scr)
        return vbox

    def initUI(self, layout):
        self.setLayout(layout)
        self.showMaximized()


#-----------------------------------------------------------------------------#

# Dialog Content

class ExoDialogContent(ExoBase):

    def __init__(self, parent, textfile, label):
        super().__init__(parent)
        layout = self.createLayout(textfile, label)
        self.initUI(layout)


    def createLayout(self, textfile, label):
        try:
            with open(textfile) as textpage:
                text = textpage.read()
        except FileNotFoundError as err:
            text = "{0} not found. Contact Author.".format(label)
        textbox = QtGui.QPlainTextEdit(text, self)
        textbox.setReadOnly(True)
        textbox.setObjectName("TextBox")
        textbox.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        card = self.createCard(label, self.hboxCreate(50, textbox))
        return self.createCardLayout(card)


#-----------------------------------------------------------------------------#