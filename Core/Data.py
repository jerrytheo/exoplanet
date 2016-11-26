
# Imports
# =======

import numpy as np
from random import shuffle
import csv
import logging


# Data Class
# ==========

class Data:

    def __init__(self, data_filepath):
        self._filepath = data_filepath
        self._pre_data = []
        self._headers_present = False
        try:
            data_file = open(self._filepath)
            csvreader = csv.reader(data_file, delimiter=',')
            for row in csvreader:
                self._pre_data.append(row)
            rows = len(self._pre_data)
            cols = max([len(row) for row in self._pre_data])
            self.size = (rows, cols)
            self.headers = ['Attribute {0}'.format(i+1) for i in range(cols)]
        except Exception as err:
            self._pre_data = None
            logging.error('Data:Upload Failed')
            logging.error('Data:' + str(err))
        else:
            data_file.close()

    def enableHeaders(self):
        if self._headers_present is not True:
            self.headers = self._pre_data[0]
            self._pre_data = self._pre_data[1:]
            self._headers_present = True

    def disableHeaders(self):
        if self._headers_present is True:
            self._pre_data = [self.headers, *self._pre_data]
            self.headers = ['Attribute {0}'.format(i+1)
                            for i in range(self.size[1])]
            self._headers_present = False

    def process(self, ltype, set_sizes=None, label_col=None):
        shuffle(self._pre_data)
        self._ltype = ltype
        if ltype == 'Clustering':
            self.post_data = self.convert()
        else:
            set_sizes = round(self.size[0] * (set_sizes / 100))
            labels, label_names = self.extractLabels(label_col, ltype)
            data = self.convert()

            class DataSet:
                data = None
                labels = None

            tr_data = DataSet()
            tr_data.data = data[:set_sizes]
            tr_data.labels = labels[:set_sizes]
            te_data = DataSet()
            te_data.data = data[set_sizes:]
            te_data.labels = labels[set_sizes:]

            self.post_data = {
                'Training': tr_data,
                'Testing': te_data
            }
            if ltype == 'Classification':
                self.post_data['Labels'] = label_names

    def convert(self):
        '''
        Converts the data read from the file to a numpy array of type float64.
        Converts categorial data into integral data.
        '''
        temp = []
        for row in range(0, len(self._pre_data)):
            for val in range(0, len(self._pre_data[row])):
                try:
                    self._pre_data[row][val] = float(self._pre_data[row][val])
                except ValueError as err:
                    if self._pre_data[row][val] not in temp:
                        temp.append(self._pre_data[row][val])
                    self._pre_data[row][val] = temp.index(
                                                    self._pre_data[row][val])
        return np.array(self._pre_data)

    def extractLabels(self, label_col, ltype):
        labels = []
        for row_num, row in enumerate(self._pre_data):
            labels.append(row[label_col])
            row = [val for i, val in enumerate(row) if i != label_col]
            self._pre_data[row_num] = row

        if ltype == 'Classification':
            uniq_labels = list(set(labels))
            labels = [uniq_labels.index(val) for val in labels]
        else:
            uniq_labels = None

        labels = np.array(labels, dtype=np.float)
        return labels, uniq_labels

    def check(self):
        if self._pre_data is None:
            return False
