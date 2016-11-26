
# Imports
# =======

import numpy as np
from random import shuffle
import csv
import logging


# Clustering/Prediction Data Class
# ===================== ==== =====

class Data:

    def __init__(self, data_filepath):
        self._pre_data = []
        self._headers_present = False
        try:
            data_file = open(data_filepath)
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

    def check(self):
        if self._pre_data is None:
            return False
