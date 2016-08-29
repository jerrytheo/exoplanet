
# Imports
# =======

import sys
from PyQt4 import QtGui, QtCore
from .Misc import MaterialShadow

#-----------------------------------------------------------------------------#

# Base Widget
# ==== ======


class ExoBase(QtGui.QWidget):

    """
    Common functions for Widgets defined here.
    
    initUI      -- Initiate UI.
    vcenter     -- Return QVBoxLayout object with listed objects centralised.
    hcenter     -- Return QHBoxLayout object with listed objects centralised.
    paintEvent  -- Draw Widget characteristics.
    iterBtns    -- Returns QHBoxLayout object with Next and Back buttons.
    placecenter -- Place Widget at the center of screen or parent window.
    """

    def __init__(self, parent):
        super().__init__(parent)
        
    
    def initUI(self, layout, scroll=True):
        """
        Initiate UI
            1. Sets the layout of the widget.
            2. Sets size of the widget to the parent.
            3. Sets position of the widget to the center of parent.
        """
        if scroll:
            self.setLayout(self.createScroll(layout))
        else:
            self.setLayout(layout)
        
        sz = self.parent().size()
        w = sz.width()
        h = sz.height()
        self.resize(w, h)
        self.show()
    
    
    def vboxCreate(self, *objectlist, vbox=None):
        """
        Return QVBoxLayout object with listed objects/spaces added in order to
        a new vbox layout or an existing one.
            1. Creates Vertical Box Layout if vbox is None.
            2. Adds Widgets/Layouts/Spaces in object list
        """
        if vbox is None:
            vbox = QtGui.QVBoxLayout()
        
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                vbox.addWidget(qitem)
            if isinstance(qitem, QtGui.QLayout):
                vbox.addLayout(qitem)
            if isinstance(qitem, int):
                vbox.addSpacing(qitem)
        
        return vbox


    def hboxCreate(self, *objectlist, hbox=None):
        """
        Return QHBoxLayout object with listed objects/spaces added in order to
        a new hbox layout or an existing one.
            1. Creates Horizontal Box Layout if hbox is None.
            2. Adds Widgets/Layouts/Spaces in object list to the layout.
        """

        if hbox is None:
            hbox = QtGui.QHBoxLayout()
        
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                hbox.addWidget(qitem)
            if isinstance(qitem, QtGui.QLayout):
                hbox.addLayout(qitem)
            if isinstance(qitem, int):
                hbox.addSpacing(qitem)
        
        return hbox

    
    def vcenter(self, *objectlist):
        '''
        Centers the given set of widgets in a QVBoxLayout using a single space
        on either side.
        '''
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                vbox.addWidget(qitem)
            if isinstance(qitem, QtGui.QLayout):
                vbox.addLayout(qitem)
            if isinstance(qitem, int):
                vbox.addStretch(qitem)
        vbox.addStretch(1)
        
        return vbox
    
    
    def hcenter(self, *objectlist):
        '''
        Centers the given set of widgets in a QHBoxLayout using a single space
        on either side.
        '''
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        for qitem in objectlist:
            if isinstance(qitem, QtGui.QWidget):
                hbox.addWidget(qitem)
            if isinstance(qitem, QtGui.QLayout):
                hbox.addLayout(qitem)
            if isinstance(qitem, int):
                hbox.addStretch(qitem)
        hbox.addStretch(1)
        
        return hbox
        
    
    def iterBtns(self, next=True, back=True):
        """
        Returns QHBoxLayout object with Next and Back buttons.
            1. Creates a QHBoxLayout object
            2. If back is true, adds a back button.
            3. Adds a stretch space.
            4. If next is true, adds a next button.
        
        """
        hbox = QtGui.QHBoxLayout()
        
        if back:
            self.backButton = QtGui.QPushButton('Back')
            backShortcut = QtGui.QShortcut(QtGui.QKeySequence(
                QtCore.Qt.Key_Backspace), self)
            backShortcut.activated.connect(self.backButton.click)
            self.backButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.backButton.setGraphicsEffect(MaterialShadow(self))
            hbox.addWidget(self.backButton)

        
        hbox.addStretch(1)
        
        if next:
            self.nextButton = QtGui.QPushButton('Next')
            nextShortcut1 = QtGui.QShortcut(QtGui.QKeySequence(
                QtCore.Qt.Key_Enter), self)
            nextShortcut1.activated.connect(self.nextButton.click)
            nextShortcut2 = QtGui.QShortcut(QtGui.QKeySequence(
                QtCore.Qt.Key_Return), self)
            nextShortcut2.activated.connect(self.nextButton.click)
            self.nextButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.nextButton.setGraphicsEffect(MaterialShadow(self))
            hbox.addWidget(self.nextButton)
            
        return hbox
        
        
    def paintEvent(self, event):
        """
        Draw Widget characteristics.
        Features implemented so far:
            1. Sets bg color to white.
        """
        opt = QtGui.QStyleOption()
        opt.init(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)


    def createCard(self, title, layout):
        wid = QtGui.QWidget()
        wid.setGraphicsEffect(MaterialShadow(self))
        wid.setObjectName('Card')
        wid.setSizePolicy(QtGui.QSizePolicy.Preferred,
                QtGui.QSizePolicy.Minimum)

        titleLab = QtGui.QLabel(title)
        titleLab.setObjectName('CardLabel')
        titleLab.setGraphicsEffect(MaterialShadow(self))

        layout.setMargin(8)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(titleLab)
        vbox.addSpacing(40)
        vbox.addLayout(layout)
        vbox.addSpacing(40)
        vbox.setMargin(0)
        wid.setLayout(vbox)
        return wid


    def createScroll(self, layout):
        wid = QtGui.QWidget(self)
        wid.setLayout(layout)
        scr = QtGui.QScrollArea()
        scr.setWidget(wid)
        scr.setWidgetResizable(True)
        scr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(scr)
        hbox.setSpacing(0)
        hbox.setMargin(0)

        return hbox

    def createCardLayout(self, *cards):
        vbox = QtGui.QVBoxLayout()
        vbox.addSpacing(30)
        for card in cards:
            hbox = QtGui.QHBoxLayout()
            hbox.addSpacing(150)
            hbox.addWidget(card)
            hbox.addSpacing(150)
            vbox.addLayout(hbox)
            vbox.addSpacing(50)
        return vbox


#-----------------------------------------------------------------------------#