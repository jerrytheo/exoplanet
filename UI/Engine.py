
# Imports
# =======


# Packages
# --------
import sys
from os import path
import logging
import pickle
from PyQt4 import QtGui, QtCore

# UIs
# ---
from .Pages import Start, Title, AlgoFile, Eval, Visual, Predict, Params
from .Defaults import NoSupport, Retry

# Backend Elements
# ------- --------
from Core import Workspace, algoEngine


#-----------------------------------------------------------------------------#

# List of Algorithms
# ==== == ==========

algos = {

    'Classification' : {
        'algolist' : [
            'Decision Tree',
            'K-Nearest Neighbors',
            'Linear Discriminant Analysis',
            'Support Vector Classifier',
            'Gaussian Naive Bayes',
        ],
        'labels' : True
    },

    'Regression' : {
        'algolist' : [
            'Linear',
            'Lasso',
            'Ridge',
        ],
        'labels' : True
    },

    'Clustering' : {
        'algolist' : [
            'K-Means',
        ],
        'labels' : False
    }

}


#-----------------------------------------------------------------------------#

# Widget Control Engine
# ====== ======= ======


class Engine(QtGui.QWidget):

    '''
    Controls the flow of control of the app.
        1. Decides the next page to display.
        2. If back pressed, decides the page to display.
        3. Saves and Loads the workspace.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = self.createLayout()
        self.initUI()
        self.setObjectName('Engine')


    def createLayout(self):
        '''
        Designs the layout of the Engine.
            1. Sets size to parent size.
            2. Sets position to the center of parent.
            3. Creates the first page to display.
        '''
        self.stat = self.parent().parent().stat
        vbox = QtGui.QVBoxLayout()
        self.activePage = Start(self)
        vbox.addWidget(self.activePage)
        self.setObjectName('Engine')
        vbox.setMargin(0)

        return vbox


    def initUI(self):
        '''
        Sets the layout of the Engine and displays the Engine.
        '''
        self.setLayout(self.layout)
    

    def buttonClicked(self):
        '''
        Decides the action to be taken for most buttons in each page. The
        actions performed for each button in each page are as follows,
        Start:
            1. createButton - Create a new Workspace.
            2. loadButton   - Load an existing Workspace.
        Title:
            1. nextButton - Set the name of the Workspace if valid and go to
                            the Type page.
        Type:
            1. clusButton - Set the algorithm type to Clustering.
            2. clasButton - Set the algorithm type to Classification.
            3. regrButton - Set the algorithm type to Regression.
        AlgoFile:
            1. nextButton - Check input and if valid go to the Params page.
        Params:
            1. startButton - Check parameter values and if valid, initiate
                             training. After completion of training, go to the
                             Eval page.
        Eval:
            1. evalBtn - Builds visuals and go to the Visual page. If
                         classification, read data set to use from user first.
            2. predBtn - Read data from file specified and predict labels for
                         the data and go to the Predict page.
            3. saveBtn - (Clustering only) Save generated labels to a csv file.
        Visual:
            1. saveBtn1 - Saves the Workspace.
            2. rerunBtn - Go to the Params page.
        Predict:
            1. saveBtn - Save the predicted labels.
        '''

        sender = self.sender()
        source = self.activePage
        
        
        # Start buttons.
        if isinstance(source, Start):

            if sender is source.createButton:
                logging.info('Start:createButton pressed.')
                self.nextWindow(Title)
            
            elif sender is source.loadButton:
                logging.info('Start:loadButton pressed.')
                try:
                    self.loadWorkspace()
                except Exception as err:
                    logging.error('Start:Load failed')
                    logging.error('Start:' + str(err))
                    self.stat.showMessage(
                        'Failed to load file. Please retry.')
                else:
                    self.nextWindow(Eval, self.workspace.algotype,
                        self.workspace.dataDir)
                    ind = self.parent().currentIndex()
                    self.parent().parent().setTabText(ind,
                        ' {0} '.format(self.workspace.title))
            
        
        # Title buttons.
        elif isinstance(source, Title):
        
            logging.info('Title:nextButton pressed.')
            title = source.checkVal()
            
            if title is not None:
                logging.info('Title:Creating workspace: ' + title)
                self.workspace = Workspace(title)
                ind = self.parent().currentIndex()
                self.parent().parent().setTabText(ind, ' {0} '.format(title))
            
                if sender is source.clusButton:
                    logging.info('Type:clusButton pressed.')
                    self.workspace.setType('Clustering')
                    self.nextWindow(AlgoFile, **algos['Clustering'])
                    
                elif sender is source.clasButton:
                    logging.info('Type:clasButton pressed.')
                    self.workspace.setType('Classification')
                    self.nextWindow(AlgoFile, **algos['Classification'])
                    
                elif sender is source.regrButton:
                    logging.info('Type:regrButton pressed.')
                    self.workspace.setType('Regression')
                    self.nextWindow(AlgoFile, **algos['Regression'])
                
            else:
                logging.error('Title:Invalid title entered')
                self.stat.showMessage('Please enter a valid title.')
            
            
        # AlgoFile buttons
        elif isinstance(source, AlgoFile):
            
            if sender is source.nextButton:
                logging.info('AlgoFile:nextButton pressed')
                chk1 = source.checkVal()
                if chk1 is not None:
                    self._algo, dataInfo = chk1
                    chk = self.workspace.uploadData(dataInfo)
                    if not chk:
                        logging.info('AlgoFile:Upload Data complete.')
                        algo, types = algoEngine(self._algo)
                        self.nextWindow(Params, algo, types)
                        self.stat.showMessage('Upload Data complete.')
                    else:
                        logging.error('AlgoFile:Upload Data failed.')
                        self.stat.showMessage('Upload Data failed.')
        
        # Params buttons
        elif isinstance(source, Params):
            
            if sender is source.startButton:
                logging.info('Params:startButton pressed')
                try:
                    params = source.getVal()
                    logging.info('Engine:' + str(params))
                    self.stat.showMessage('Building model.')
                    self.workspace.buildModel(self._algo, params)
                    self.nextWindow(Eval, self.workspace.algotype,
                        self.workspace.dataDir)
                except ValueError:
                    logging.warning('Params:Invalid parameters')
                    self.stat.showMessage('Invalid parameters')
                    self.nextWindow(Retry, msg='Error in parameters. Retry.')
                    
        # Eval buttons
        elif isinstance(source, Eval):
            
            try:
                if sender is source.evalBtn:
                    dataset = [False, True, 'both']
                    logging.info('Eval:evalBtn pressed')
                    if self.workspace.algotype == 'Clustering':
                        self.workspace.buildVisuals()
                    else:
                        ind = source.setCombo.currentIndex()
                        self.workspace.buildVisuals(dataset[ind])

                    self.nextWindow(Visual, algotype=self.workspace.algotype,
                        visuals=self.workspace.visEval.Visuals)
            
                elif sender is source.predBtn:
                    logging.info('Eval:predBtn pressed')
                    dataInfo = source.checkVal()
                    try:
                        data = self.workspace.predictLabels(dataInfo)
                        labels = self.workspace.getLabels(data)
                    except:
                        self.stat.showMessage('Prediction failed.')
                        return
                    
                    self.nextWindow(Predict, data, labels)

                elif hasattr(sender, 'saveBtn') and sender is source.saveBtn:
                    logging.info('Eval:saveBtn pressed')
                    self.workspace.saveLabels()
                    self.stat.showMessage('Labels saved.')
                    return

                
            except UnboundLocalError as err:
                self.nextWindow(Retry, msg='Error in building visuals.')
            
                
        # Visual buttons
        elif isinstance(source, Visual):
            
            if sender is source.saveBtn1:
                logging.info('Visual:saveBtn1 pressed')
                self.saveWorkspace()
            elif sender is source.rerunBtn:
                logging.info('Visual:rerunBtn pressed')
                params = self.workspace.getParameters()
                algo, types = algoEngine(self._algo)
                self.nextWindow(Params, algo, types, params)
        
        
        # Predict buttons    
        elif isinstance(source, Predict):
            
            if sender is source.saveBtn:
                logging.info('Predict:saveButton pressed')
                if self.workspace.algotype == 'Clustering':
                    self.workspace.saveLabels(True)
                else:
                    reply = QtGui.QMessageBox.question(self, 'Save New Data',
                        'Append new data to existing data?',
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                        QtGui.QMessageBox.Yes)
                    
                    if reply == QtGui.QMessageBox.Yes:
                        self.workspace.saveLabels(append=True)
                    elif reply == QtGui.QMessageBox.No:
                        self.workspace.saveLabels(append=False)
                self.stat.showMessage('Save complete.')
            
        
    
    def nextWindow(self, Window, *args, **kwargs):
        '''
        Changes the active page.
            1. Closes the current active page.
            2. Creates the next page to display
            3. Applies the styles required after page creation.
        '''

        self.activePage.close()
        del(self.activePage)
        self.activePage = Window(self, *args, **kwargs)
        self.activePage.setObjectName('ActivePage')
        self.layout.addWidget(self.activePage)


    def goBack(self):
        '''
        Decides the page to go to if the back button is pressed.
            1. AlgoFile  -> Type.
            2. Params    -> AlgoFile
            3. Visual    -> Eval
            4. Predict   -> Eval
            5. NoSupport -> Type
            6. Retry     -> AlgoFile
        '''

        source = self.activePage
        self.activePage.close()
        
        if isinstance(source, NoSupport):
            self.nextWindow(Type)
        
        elif isinstance(source, Params):
            self.nextWindow(AlgoFile, **algos[self.workspace.algotype])
        
        elif isinstance(source, Visual):
            self.nextWindow(Eval, self.workspace.algotype,
                self.workspace.dataDir)
        
        elif isinstance(source, Predict):
            self.nextWindow(Eval, self.workspace.algotype,
                self.workspace.dataDir)
            
        elif isinstance(source, Retry):
            self.nextWindow(AlgoFile, **algos[self.workspace.algotype])
    
    
    def saveWorkspace(self):
        '''
        Saves the Workspace.
        '''
        
        logging.info('Engine:Saving Workspace')
        home = path.expanduser('~')
        fname = QtGui.QFileDialog.getSaveFileName(self,
                    'Save file location', home,
                    filter=('Exoplanet Workspace (*.exws)'))
        
        if fname == '': return
        
        fname = fname.split('.')
        if fname[-1] != 'exws':
            fname.append('exws')
        fname = '.'.join(fname)
        
        try:
            with open(fname, 'wb') as workfile:
                pickle.dump(self.workspace, workfile, -1)
            self.stat.showMessage('Saved Workspace.')
        except Exception as err:
            logging.error('Engine:Save failed')
            logging.error('Engine:' + str(err))
            self.stat.showMessage('Save failed. Try again.')
        
        logging.info('Engine:Stored at ' + fname)
        
    
    def loadWorkspace(self):
        '''
        Loads an existing Workspace.
        '''
        
        logging.info('Engine:Loading Workspace')
        home = path.expanduser('~')
        fname = QtGui.QFileDialog.getOpenFileName(self, 'File location', home,
                    filter=('Exoplanet Workspace (*.exws) | *.exws') )
        with open(fname, 'rb') as workfile:
            self.workspace = pickle.load(workfile)
        
        if not isinstance(self.workspace, Workspace):
            raise ValueError('File does not contain Workspace object.')
        
        self._algo = self.workspace.getAlgorithm()

        
#-----------------------------------------------------------------------------#