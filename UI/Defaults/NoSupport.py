
# Imports
# =======


import sys
from os import path
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase
import logging


#-----------------------------------------------------------------------------#

class NoSupport(ExoBase):
    
    def __init__(self, parent):
        
        super().__init__(parent)
        layout = self.createLayout()
        self.initUI(layout)
        
    
    def initUI(self, layout):
        
        super().initUI(layout)
        if self.parent() is not None:
            self.backButton.clicked.connect(self.parent().goBack)
    
    
    def createLayout(self):
        
        ques = QtGui.QLabel('Not yet supported.', self)
        
        hboxBtm  = self.iterBtns(next=False)
        hboxQues = self.hcenter(ques)
        
        vbox = self.vcenter(hboxQues)
        vbox.addStretch(1)
        vbox.addLayout(hboxBtm)
        
        return vbox
        
        
#-----------------------------------------------------------------------------#
