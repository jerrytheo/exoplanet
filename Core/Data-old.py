
# Imports
# =======

import numpy as np
from random import shuffle
import csv
import logging


# Clustering/Prediction Data Class
# ===================== ==== =====

class ClusData:

    '''
    A container for the data set.
    Used for clustering
             predictions

    Data Members
    ------------
    datatable        -- Array form of dataset

    Methods
    -------
    __init__()       -- Reads data from specified file, stores in dataset.
                        Calls splitDataset()
    convert()        -- Converts the data read from a file into an array.
    getFitData()     -- Returns the data to fit model.
    getPredictData() -- Returns the data to predict accuracy of model (same as
                        getFitData() for unlabelled data).
    isNone()         -- Returns True if datatable is None.
    '''

    def __init__(self, dataFile=None, headers=False):
        '''
        Reads data from a specified file and converts it into numpy styled
        arrays.

        Parameters
        ----------
        dataFile - Path to file with data.
        headers  - Whether headers present in file.
        '''
        self.datatable = []
        self.headers = None
        self.dataFile = dataFile

        try:
            datafile = open(dataFile)
            try:
                dialect = csv.Sniffer().sniff(datafile.read(1024), delim)
                datafile.seek(0)
                table = csv.reader(datafile, dialect)
            except Exception as err:
                table = csv.reader(datafile, delimiter=delim)
                logging.error('Data:Sniff Failed')
                logging.error('Data:' + str(err))

            for row in table:
                self.datatable.append(row)

            if headers:
                self.headers = self.datatable[0]
                self.datatable = self.datatable[1:]

            self.convert()

            if self.datatable.size == 0:
                raise ValueError('data file empty')

        except Exception as err:
            self.datatable = None
            logging.error('Data:Upload data Failed')
            logging.error('Data:' + str(err))

        finally:
            datafile.close()

    def convert(self):
        '''
        Converts the data read from the file to a numpy array of type float64.
        Converts categorial data into integral data.
        '''
        temp = []
        for row in range(0, len(self.datatable)):
            for val in range(0, len(self.datatable[row])):
                try:
                    self.datatable[row][val] = float(self.datatable[row][val])
                except ValueError as err:
                    if self.datatable[row][val] not in temp:
                        temp.append(self.datatable[row][val])
                    self.datatable[row][val] = temp.index(
                                                    self.datatable[row][val])
        self.datatable = np.array(self.datatable)

    def getFitData(self, *args):
        '''
        Returns the data to fit.
        '''
        return [self.datatable]

    def getPredictData(self, *args):
        '''
        Returns the data to predict.
        '''
        return self.datatable

    def isNone(self):
        '''
        Returns True if datatable is None.
        '''
        if self.datatable is None:
            return True
        return False

PredictData = ClusData


# Classification Data Class
# ============== ==== =====

class ClassData(ClusData):

    '''
    Inherited from Data.
    A container for the training, validation and testing sets.
    Used for classification (discrete labels)
             regression     (continuous labels)

    Data Members
    ------------
    train          -- Array of training tuples
    valid          -- Array of validation tuples
    test           -- Array of testing tuples
    train_labels   -- Array of training tuple labels
    valid_labels   -- Array of validation tuple labels
    test_labels    -- Array of testing tuple labels

    Methods
    -------
    __init__()       -- Reads data and labels from the files.
                        Calls super() to initiate parent.
                        Calls splitLabels()
    splitDataset()   -- Splits the dataset into different sets for training,
                        validation and testing.
    splitLabels()    -- Splits the labels into different sets for training,
                        validation and testing.
    getFitData()     -- Returns the data to fit model.
    getPredictData() -- Returns the data to predict accuracy of model.
    '''

    def __init__(self, dataFile=None, labelsFile=None,
                 fractions=[0.7, 0.2, 0.1], headers=False, delim=','):
        '''
        Reads data set from file1 and it's corresponding class labels from
        file2. Converts the data from each file into numpy arrays for
        classification (or regression).

        Parameters
        ----------
        dataFile  -- File to read data set from. (String)
        labsFile  -- File to read corresponding class labels from. (String)
        fractions -- Fractional sizes of train, valid and test set. (List of 
                     floating point numbers)
        headers   -- True if headers present in csv file. (Boolean)
        '''
        super().__init__(dataFile, headers)
        self.labels = []
        self.labelsFile = labelsFile
        self.delim = delim
        try:
            labelfile = open(labelsFile)
            try:
                dialect = csv.Sniffer().sniff(labelfile.read(4096), delim)
                labelfile.seek(0)
                table = csv.reader(labelfile, dialect)
            except Exception as err:
                table = csv.reader(labelfile, delimiter=delim)
                logging.info('Data:Sniff Failed')
                logging.info('Data:' + str(err) )

            labelfile.seek(0)
            label = csv.reader(labelfile, delimiter=delim)
            for row in label:
                self.labels.append(row)
            if headers:
                self.labels = self.labels[1:]
            if (len(self.labels) != len(self.datatable)):
                raise ValueError('inequal observations and labels')

            order = [i for i in range(len(self.datatable))]
            shuffle(order)
            self.splitDataset(fractions, order)
            self.splitLabels(fractions, order)

        except ValueError as err:
            self.labels = None
            self.datatable = None
            logging.error('ClassData:Labels upload failed.')
            logging.error('ClassData:' + str(err))

        finally:
            labelfile.close()

    def splitDataset(self, sizes, order):
        '''
        Splits the data read from the file into training, validation and
        testing sets.

        Parameters
        ----------
        sizes -- Fractional size of train, valid and test sets.
        '''
        self.datatable = [self.datatable[i] for i in order]
        self.convert()
        # Split the dataset into training, validation and test sets
        nrowst = round(self.datatable.shape[0] * sizes[0])
        self.train = self.datatable[:nrowst]

        nrowsv = nrowst + round(self.datatable.shape[0] * sizes[1])
        self.valid = self.datatable[nrowst:nrowsv]

        nrowst = self.datatable.shape[0] - nrowsv
        self.test = self.datatable[-nrowst:]

    def splitLabels(self, sizes, order):
        '''
        Splits the labels corresponding to the data set from the file into
        training, validation and testing labels sets. Categorizes labels.

        Parameters
        ----------
        sizes    -- Fractional sizes of train, valid and test sets.
        '''
        self.labels = [self.labels[i] for i in order]
        temp = []
        for i in range(0, len(self.labels)):
            if self.labels[i] not in temp:
                temp.append(self.labels[i])
            self.labels[i] = temp.index(self.labels[i])
        self.labelList = []
        for i in temp:
            for j in i:
                if j is not '':
                    self.labelList.append(j)
                    break

        self.labels = np.array(self.labels)

        nrowst = round(self.labels.shape[0] * sizes[0])
        self.train_labels = self.labels[:nrowst]

        nrowsv = nrowst + round(self.labels.shape[0] * sizes[1])
        self.valid_labels = self.labels[nrowst:nrowsv]

        nrowst = self.datatable.shape[0] - nrowsv
        self.test_labels = self.labels[-nrowst:]

    def getFitData(self):
        '''
        Returns the data to fit (Training data).
        '''
        return (self.train, self.train_labels)

    def getPredictData(self, test=False):
        '''
        Returns data to predict classlabels of (Testing or Validation data).

        Parameters
        ----------
        test -- If True, return test dataset.
                If False, return validation dataset.
        '''
        if test == 'both':
            data = np.concatenate([self.test, self.valid])
            labs = np.concatenate([self.test_labels, self.valid_labels])
            return(data, labs)
        elif test is True:
            return (self.test, self.test_labels)
        elif test is not False:
            return (self.valid, self.valid_labels)

    def getLabels(self):
        labs = []
        for i in self.labels:
            labs.append(self.labelList[i])
        return labs


# Regression Data Class
# ========== ==== =====

class RegrData(ClassData):

    def splitLabels(self, sizes, order):
        '''
        Splits the labels corresponding to the data set from the file into
        training, validation and testing labels sets. Does not categorize
        labels, instead converts to array.

        Parameters
        ----------
        sizes    -- Fractional sizes of train, valid and test sets.
        '''

        self.labels = [self.labels[i] for i in order]
        try:
            self.labels = np.array(self.labels, dtype=np.float64)
        except Exception as err:
            logging.error('RegrClass: Invalid input labels')
            logging.error('RegrClass: ' + str(err))

        nrowst = round(self.labels.shape[0] * sizes[0])
        self.train_labels = self.labels[:nrowst]

        nrowsv = nrowst + round(self.labels.shape[0] * sizes[1])
        self.valid_labels = self.labels[nrowst:nrowsv]

        nrowst = self.datatable.shape[0] - nrowsv
        self.test_labels = self.labels[-nrowst:]

    def getLabels(self):
        '''
        Return the labels of the dataset.
        '''
        return self.labels
