
# Imports
# =======


import sys
from os import path
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MaterialShadow
import logging
from Core.Data import ClassData

#-----------------------------------------------------------------------------#

# Prompt for Algorithm and File
# ====== === ========= === ====


class AlgoFile(ExoBase):
    
    '''
    Page to select:
        1. Algorithm to run.
        2. Files to upload.
        3. For supervised learning, sizes of data sets.
    '''

    
    def __init__(self, parent, algolist=[None], labels=False):
        super().__init__(parent)
        self.algolist = algolist
        self.labels = labels
        self.delim = ','
        self.headers = False
        layout = self.createLayout()
        self.initUI(layout)
        
        
    def initUI(self, layout):
        '''
        Initialise the AlgoFile page.
            1. Sets layout for AlgoFile.
            2. Connects the clicked signals for dataBrowse, labelsBrowse,
               nextButton and backButton.
        '''

        super().initUI(layout)
        
        self.dataBrowse.clicked.connect(self.readPath)
        if self.labels: 
            self.labelsBrowse.clicked.connect(self.readPath)
            
        self.nextButton.clicked.connect(self.parent().buttonClicked)
    
    
    def createLayout(self):
        '''
        Create the layout for the AlgoFile page.
            1. Creates layout for selecting algorithm
            2. Creates layout for including files.
            3. Creates layout for setting file parameters.
            4. If supervised learning, creates layout to set dataset sizes.
        '''

        cards = []

        # Create Algorithm Section
        cards.append(self.createCard('Select Algorithm', self.algoboxLayout()))

        # Create File Section
        vboxFile = self.vcenter(self.fileLayout(), 40, self.fileParamLayout())
        cards.append(self.createCard('Select Files', vboxFile))

        # Create Dataset sizes Section <Supervised only>
        if self.labels:
            ques3 = QtGui.QLabel('Set Dataset Sizes')
            ques3.setObjectName('QuesLabel')
            self.fractions = {
                'Training'  : 0.7,
                'Validation': 0.2,
                'Testing'   : 0.1,
            }
            hboxSets = self.datasetSizesLayout()
            setsCard = self.createCard('Set Dataset Sizes', hboxSets)
            cards.append(setsCard)

        vbox = self.createCardLayout(*cards)
        vbox.addLayout(self.iterBtns(back=False))

        return vbox
    
    
    def algoboxLayout(self):
        '''
        Creates the layout to select algorithm.
            1. Creates a Combo Box and adds each algorithm.
        '''

        self.algoCombo = QtGui.QComboBox(self)
        for algo in self.algolist:
            self.algoCombo.addItem(algo)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(3)
        hbox.addWidget(self.algoCombo, 2)
        hbox.addStretch(3)
        return hbox


    def fileLayout(self):
        '''
        Creates the layout to select files.
            1. For the data file,
                1. Create a QLineEdit widget to enter path.
                2. Create a QPushButton to browse to file.
            2. If supervised learning, repeats the above steps for labels file.
        '''

        # Create Widgets
        dataLab = QtGui.QLabel('Data')
        dataLab.setObjectName('FormLabel')
        if isinstance(self.parent().workspace.data, ClassData):
            default = self.parent().workspace.data.dataFile
        else:
            default = path.expanduser('~')
            
        self.dataLE = QtGui.QLineEdit(default, self)
        self.dataBrowse = QtGui.QPushButton('Browse')
        self.dataBrowse.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dataBrowse.setGraphicsEffect(MaterialShadow(self))
        
        if self.labels:
            labelsLab = QtGui.QLabel('Labels')
            labelsLab.setObjectName('FormLabel')
            if isinstance(self.parent().workspace.data, ClassData):
                default = self.parent().workspace.data.labelsFile
            else:
                default = path.expanduser('~')
                
            self.labelsLE = QtGui.QLineEdit(default, self)
            self.labelsBrowse = QtGui.QPushButton('Browse')
            self.labelsBrowse.setFocusPolicy(QtCore.Qt.NoFocus)
            self.labelsBrowse.setGraphicsEffect(MaterialShadow(self))
        
        # Create Layouts
        hboxData = self.hboxCreate(self.dataLE, self.dataBrowse)
        hboxData.setSpacing(30)
        hboxData.setMargin(0)
        
        form = QtGui.QFormLayout()
        form.addRow(dataLab, hboxData)

        if self.labels:
            hboxLab = self.hboxCreate(self.labelsLE, self.labelsBrowse)
            hboxLab.setSpacing(30)
            hboxLab.setMargin(0)
            form.addRow(labelsLab, hboxLab)

        form.setLabelAlignment(QtCore.Qt.AlignLeft)
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(25)

        hbox = QtGui.QHBoxLayout()
        hbox.addSpacing(200)
        hbox.addLayout(form, 4)
        hbox.addSpacing(200)

        return hbox
    

    def datasetSizesLayout(self):
        '''
        Create the layout to set data set sizes.
            1. Initialises data set names, validator, tool tip basic format,
               dict editDict to store edited values.
            2. For each data set,
                1. Creates a QLineEdit widget to read size, and sets its
                   validator.
                2. Store the QLineEdit widget in editDict.
        '''

        datasets = ('Training', 'Validation', 'Testing')
        input_valid = QtGui.QDoubleValidator(bottom=0, top=1.0, decimals=6)
        tip = 'Set the relative size of {0} dataset.'
        formSets = QtGui.QFormLayout()
        self.editDict = {}

        # Create row for each data set
        for d_set in datasets:
            lab = QtGui.QLabel(d_set)
            lab.setObjectName('FormLabel')
            lab.setStatusTip(tip.format(d_set))
            
            edit = QtGui.QLineEdit(str(self.fractions[d_set]))
            edit.setValidator(input_valid)
            edit.setStatusTip(tip.format(d_set))
            edit.textEdited[str].connect(self.alterRatio)
            
            self.editDict[edit] = d_set

            formSets.addRow(lab, edit)

        
        formSets.setLabelAlignment(QtCore.Qt.AlignLeft)
        formSets.setVerticalSpacing(15)
        formSets.setHorizontalSpacing(25)
        hboxSets = self.hcenter(formSets)
        return hboxSets
    
    
    def fileParamLayout(self):
        '''
        Creates the layout to set file parameters.
            1. For delimiter setting,
                1. Creates QLineEdit widget to enter delimiter.
                2. Connects QLineEdit's textEdited signal to delimHeadChanged.
            2. For headers setting,
                1. Creates a QComboBox with options 'Yes' and 'No'.
                2. Connects QComboBox's currentIndexChanged signal to
                   delimHeadChanged.
        '''

        delimLab = QtGui.QLabel('Delimiter')
        delimLab.setStatusTip('Set csv file delimiter.')
        delimLab.setObjectName('FormLabel')
        self.delimEdit = QtGui.QLineEdit(self.delim)
        self.delimEdit.setStatusTip('Set csv file delimiter.')
        self.delimEdit.textEdited[str].connect(self.delimHeadChanged)
        sz = self.delimEdit.size()

        headLab = QtGui.QLabel('Headers')
        headLab.setStatusTip('Whether the csv file contains headers.')
        headLab.setObjectName('FormLabel')
        self.headCombo = QtGui.QComboBox()
        self.headCombo.addItem('No')
        self.headCombo.addItem('Yes')
        self.headCombo.setCurrentIndex(0)
        self.headCombo.currentIndexChanged[int].connect(self.delimHeadChanged)
        self.headCombo.setStatusTip('Whether the csv file contains headers.')

        formFile = QtGui.QFormLayout()
        formFile.addRow(delimLab, self.delimEdit)
        formFile.addRow(headLab, self.headCombo)
        formFile.setLabelAlignment(QtCore.Qt.AlignLeft)
        formFile.setSpacing(15)
        formFile.setHorizontalSpacing(25)
        hboxFile = QtGui.QHBoxLayout()
        hboxFile.addStretch(3)
        hboxFile.addLayout(formFile, 2)
        hboxFile.addStretch(3)

        return hboxFile
    
    
    def readPath(self):
        '''
        Functions as a slot to read file path when either Browse button is
        clicked.
            1. Reads file path from a File Dialog.
            2. If file path is not empty, sets QLineEdit's text to file path.
            3. If file path is empty, sets QLineEdit's text to user's home
               directory.
        '''

        sender = self.sender()
        if sender is self.dataBrowse:
            logging.info('AlgoFile:dataBrowse pressed')
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Data File',
                self.dataLE.text(), filter='CSV (*.csv) | *.csv')
            if fname != '':
                self.dataLE.setText(fname)
                if self.labels:
                    self.labelsLE.setText(path.dirname(fname))
            else:
                default = path.expanduser('~')
                self.dataLE.setText(default)

            logging.info('AlgoFile:' + fname)
                
        elif hasattr(self, 'labelsBrowse') and sender is self.labelsBrowse:
            logging.info('AlgoFile:labelsBrowse pressed')
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Labels File',
                self.labelsLE.text(), filter='CSV (*.csv) | *.csv')
            if fname != '':
                self.labelsLE.setText(fname)
            else:
                default = path.expanduser('~')
                self.labelsLE.setText(default)
            logging.info('AlgoFile:' + fname)
        

    def checkVal(self):
        '''
        Called before moving to next window, validates user input.
            1. Checks if data file path is valid.
            2. If supervised learning,
                1. Checks if labels file path is valid.
                2. Checks if data set sizes are correct.
            3. Returns dict dataInfo that stores file paths, data set sizes,
               and the header and delimiter setting.
        '''

        dataInfo = {}
        dataFile = self.dataLE.text()
        
        # Check valid data file.
        if not path.isfile(dataFile):
            self.parent().stat.showMessage('Enter valid path to data file.')
            default = path.expanduser('~')
            self.dataLE.setText(default)
            return None
        
        # Check valid label file and valid fractions
        if self.labels:
            labFile = self.labelsLE.text()
            if not path.isfile(labFile):
                self.parent().stat.showMessage(
                    'Enter valid path to labels file.')
                default = path.expanduser('~')
                self.labelsLE.setText(default)
                return None
            if round(sum(self.fractions.values()), 6) != 1:
                self.parent().stat.showMessage(
                    'Sum of fractional sizes must be 1.')
                return None
        
         
        dataInfo['dataFile'] = dataFile 
        if self.labels:
            dataInfo['labelsFile'] = labFile
            dataInfo['fractions'] = [
                self.fractions['Training'],
                self.fractions['Validation'],
                self.fractions['Testing'],
            ]

        if not self.delim:
            self.parent().stat.showMessage('Enter a delimiter.')
            return None

        dataInfo['headers'] = self.headers
        dataInfo['delim'] = self.delim
        
        algo = self.algoCombo.currentText()
        
        return algo, dataInfo


    def alterRatio(self, value):
        '''
        Changes data set sizes if valid fractions entered.
            1. Checks if fractional size entered is valid.
            2. If valid, saves the size.
            3. Set the corresponding QLineEdit's text to size.
        '''

        sender = self.sender()

        valid = sender.validator()
        if valid.validate(value, 0)[0] != 2:
            sender.setText(str(self.fractions[self.editDict[sender]]))
        else:
            self.fractions[self.editDict[sender]] = float(value)
            sender.setText(value)

    
    def delimHeadChanged(self, value):
        '''
        Changes delimiter or header setting.
            1. For delimiter, saves new delimiter.
            2. For headers, if 'Yes' save True otherwise False.
        '''

        sender = self.sender()
        if sender is self.delimEdit:
            self.delim = value

        elif sender is self.headCombo:
            if value == 0:
                self.headers = False
            elif value == 1:
                self.headers = True
        
        
#-----------------------------------------------------------------------------#