
# Imports
# =======


import sys
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase
import logging


#-----------------------------------------------------------------------------#

class Retry(ExoBase):
    
    def __init__(self, parent, msg='Retry'):
        
        super().__init__(parent)
        layout = self.createLayout(msg)
        self.initUI(layout)
        
    
    def initUI(self, layout):
        
        super().initUI(layout)
        if self.parent() is not None:
            self.retryBtn.clicked.connect(self.parent().goBack)
    
    
    def createLayout(self, msg):
        
        ques = QtGui.QLabel(msg, self)
        self.retryBtn = QtGui.QPushButton('Retry')
        
        hboxQues = self.hcenter(ques)
        hboxRetry = self.hcenter(self.retryBtn)
        
        vbox = self.vcenter(hboxQues)
        vbox.addLayout(hboxRetry)
        vbox.addStretch(1)
        
        return vbox
        
        
#-----------------------------------------------------------------------------#
