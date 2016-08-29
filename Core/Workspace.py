
# Imports
# =======

from os import path
import csv
import logging
from . import Data
from .ModelBuild import Model
from .Evaluation import VisEval
from .Algos import algoEngine


#-----------------------------------------------------------------------------#

# Workspace
# =========


class Workspace:

    """
    Builds a Workspace class object used as a handle for the user's data,
    model for the data and the visuals for the model.
    
    Data Members
    ------------
    title       -- Title of Workspace
    data        -- Data/Labelled_Data object build from user data.
    algorithm   -- Algorithm to execute.
    model       -- Built model.
    
    Methods
    -------
    __init__()        -- Initialises Data Members to None
    
    runAlgorithms()   -- Runs the algorithms specified.
        
    buildVisuals()    -- Builds the visuals for the algorithms run.
    
    save()            -- Saves the Workspace to a JSON file.
    
    """
    
    
    def __init__(self, title):
        self.title     = title
        self.data      = None
        self.model     = None
        self.visEval   = None
        self.algotype  = None
        self.dataDir   = None
    
    
    def setType(self, algotype):
        self.algotype = algotype
        
    
    def uploadData(self, dataInfo):
        tmp = dataInfo['dataFile']
        self.dataDir, tmp = path.split(tmp)
        
        if self.algotype == 'Classification':
            self.data = Data.ClassData(**dataInfo)
        elif self.algotype == 'Regression':
            self.data = Data.RegrData(**dataInfo)
        elif self.algotype == 'Clustering':
            self.data = Data.ClusData(**dataInfo)
        
        return self.data.isNone()
    
    
    def buildModel(self, algo, params):
        algo, types = algoEngine(algo)
        algo = list(algo)
        algo.reverse()
        self.model = Model(algo[0], params[algo[0]])
        algo = algo[1:]
        
        for al in algo:
            self.model.addAlgorithm(al, params[al])
        
        logging.info('Workspace:' + str(self.model.model))
        to_fit = self.data.getFitData()
        self.model.fitData(to_fit)

    
    def buildVisuals(self, test=False):
        self.visEval = VisEval(self.algotype, self.model, self.data, test)
        
    
    def predictLabels(self, dataInfo):
        self.newdata = Data.PredictData(**dataInfo)
        data = self.newdata.getPredictData()
        self.newdata.labels = self.model.predictData(data)
        if self.algotype == 'Classification':
            self.newdata.labelList = self.data.labelList

        return self.newdata
        
    
    def getLabels(self, data):
        labs = []
        for i in data.labels:
            if self.algotype == 'Classification':
                labs.append( data.labelList[i] )
            elif self.algotype == 'Clustering':
                labs.append( str(i+1) )
            elif self.algotype == 'Regression':
                labs.append( str(round(*i, 6)) )

        return labs
        

    def debugPrint(self):
        logging.debug('Workspace:\\')
        logging.debug('Title:' + self.title)
        logging.debug('Algo Type:'+ str(self.algotype) )
        logging.debug('Data Directory:' + self.dataDir)
        logging.debug('FitData:'+ str(self.data.getFitData()) )
        if self.algotype == 'Classification' or self.algotype == 'Regression':
            if self.algotype == 'Classification':
                logging.debug('Labels List:'+ str(self.data.labelList) )
            logging.debug('PredictData:')
            logging.debug('\tTrue:\n'+ str(self.data.getPredictData(True)) )
            logging.debug('\tFalse:\n'+ str(self.data.getPredictData(False)) )
            logging.debug('\tBoth:\n'+ str(self.data.getPredictData('both')) )
        logging.debug('Model:'+ str(self.model.model) )
        logging.debug('Visuals:'+ str(self.visEval.Visuals) )
        
    
    def saveLabels(self, append=False):
        if self.algotype == 'Classification' or self.algotype == 'Regression':
            self.supervisedSave(append)
            logging.info('Workspace:Saved Labels')
        elif self.algotype == 'Clustering':
            self.unsupervisedSave(append)
            logging.info('Workspace:Saved Labels')
            
    
    def supervisedSave(self, append=False):
        if append:
            dataFile = self.data.dataFile
            labelsFile = self.data.labelsFile
            
            with open(dataFile, 'a+') as csvfile:
                csvfile.seek(0)
                dialect = csv.Sniffer().sniff(csvfile.read())
                wrt = csv.writer(csvfile, dialect=dialect)
                for row in self.newdata.getFitData():
                    wrt.writerow(row)
            
            with open(labelsFile, 'a+') as csvfile:
                wrt = csv.writer(csvfile)
                for i in self.newdata.labels:
                    wrt.writerow( [self.newdata.labelList[i]] )
            
        else:
            tmp = self.data.dataFile.split('.')
            tmp[-2] += '-new'
            dataFile = '.'.join(tmp)
            
            labelsFile = self.data.labelsFile.split('.')
            labelsFile[-2] += '-new'
            labelsFile = '.'.join(labelsFile)
            
            with open(dataFile, 'w') as csvfile:
                wrt = csv.writer(csvfile)
                for row in self.newdata.getFitData():
                    wrt.writerow(row)
            
            with open(labelsFile, 'w') as csvfile:
                wrt = csv.writer(csvfile)
                for i in self.newdata.labels:
                    wrt.writerow( [self.newdata.labelList[i]] )
            
    
    def unsupervisedSave(self, new=False):
        tmp = self.data.dataFile.split('.')
        tmp[-2] += '-labels'
        if new:
            tmp[-2] += '-new'
        fname = '.'.join(tmp)
        labels = self.model.predictData(self.data.getPredictData())
        with open(fname, 'w') as csvfile:
                wrt = csv.writer(csvfile)
                for i in labels:
                    wrt.writerow([i])
    
    
    def getAlgorithm(self):
        return self.model.getFinal()


    def getParameters(self):
        params = {}
        for i in self.model.getSteps():
            params[i[0]] = i[1].get_params()
        return params


#-----------------------------------------------------------------------------#