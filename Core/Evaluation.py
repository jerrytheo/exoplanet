
# Imports
# =======

# From Packages
# ---- --------
from sklearn.metrics import roc_curve, confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import logging

# Backend Elements
# ------- --------
from . import Data
from .ModelBuild import Model


#-----------------------------------------------------------------------------#

# Visual Evaluation of Model
# ====== ========== == =====


class VisEval:

    def __init__(self, algotype, model, data, test):
        if algotype == 'Classification':
            confMatrix = self.buildConfusion(model, data.getPredictData(test))
            rocCurves = self.plotROC(model, data, test)
            accuracy = self.getAccuracy(model, data.getPredictData(test), algotype)
            self.Visuals = {
                'Confusion Matrix' : confMatrix,
                'ROC Curves' : rocCurves,
                'Labels' : data.labelList,
                'Accuracy' : accuracy
            }
        
        
        elif algotype == 'Regression':
            regrLines = self.plotRegr(model, data.getPredictData(test))
            accuracy = self.getAccuracy(model, data.getPredictData(test), algotype)
            self.Visuals = {
                'Regr Line' : regrLines,
                'Accuracy' : accuracy
            }
            
        
        elif algotype == 'Clustering':
            pcoPlot = self.plotPara(model, data.getPredictData())
            if data.headers is not None:
                heads = data.headers
            else:
                heads = []
                n_samp, n_feat = pcoPlot[0].shape
                for i in range(n_feat):
                    heads.append('Feature ' + str(i+1))
            self.Visuals = {
                'Para Co-ordinates' : pcoPlot,
                'Headers' : heads
            }


    def buildConfusion(self, model, data):
        X = data[0]
        y_true = data[1]
        y_pred = model.predictData(X)
        try:
            C = confusion_matrix(y_true, y_pred)
        except Exception as err:
            logging.error('Evaluation:Confusion Matrix:' + str(err))
            C = None
        
        return C
        
    
    def plotROC(self, model, data, test):
        train_data = data.getFitData()
        ovr_clf = OneVsRestClassifier(model.model)
        ovr_clf.fit(*train_data)
        
        X, y_true = data.getPredictData(test)
                
        y_pred = ovr_clf.predict_proba(X)
        labels = data.labelList
        
        rocVals = {}
        
        try:
            for i in range(0, y_pred.shape[1]):
                fpr, tpr, thr = roc_curve(y_true, y_pred[:,i], pos_label=i)
                rocVals[labels[i]] = (fpr, tpr)
        except Exception as err:
            logging.error('Evaluation:ROC Curve:' + str(err))
            rocVals = None
        
        return rocVals
        
    
    def getAccuracy(self, model, data, algotype):
        if algotype == 'Classification':
            X = data[0]
            y_true = data[1]
            y_pred = model.predictData(X)
            correct = 0
            for i in range(len(y_true)):
                if y_true[i] == y_pred[i]:
                    correct += 1
            return correct/len(y_true)
        elif algotype == 'Regression':
            X = data[0]
            y = data[1]
            return model.model.score(X, y)


    def plotRegr(self, model, data):
        X = data[0]
        y_true = data[1]
        y_pred = model.predictData(X)
        y = [y_true, y_pred]
        return (X, y)


    def plotPara(self, model, data):
        y = model.predictData(data)
        return (data, y)


#-----------------------------------------------------------------------------#
