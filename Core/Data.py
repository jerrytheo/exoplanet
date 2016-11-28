'''
ExoPlanet Data
Copyright (C) 2016  Abhijit J. Theophilus, Mohinish L. Reddy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# Imports
# =======

import csv
import logging
import numpy as np
from os import path
from random import shuffle
from copy import deepcopy


# Required Information
# ====================

class _DataSet:
    data = None
    labels = None


# Data Class
# ==========

class Data:

    def __init__(self, data_filepath):
        self._filepath = data_filepath
        self.filedir = path.split(self._filepath)[0]
        self.filename = path.split(self._filepath)[1]
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
        data = deepcopy(self._pre_data)
        shuffle(data)
        self._ltype = ltype
        if ltype == 'Clustering':
            self.post_data = self.convert(data)
        else:
            set_sizes = round(self.size[0] * (set_sizes / 100))
            labels, label_names = self.extractLabels(data, label_col, ltype)
            data = self.convert(data)

            tr_data = _DataSet()
            tr_data.data = data[:set_sizes]
            tr_data.labels = labels[:set_sizes]
            te_data = _DataSet()
            te_data.data = data[set_sizes:]
            te_data.labels = labels[set_sizes:]

            self.post_data = {
                'Training': tr_data,
                'Testing': te_data
            }
            if ltype == 'Classification':
                self.post_data['Labels'] = label_names

    def convert(self, data):
        '''
        Converts the data read from the file to a numpy array of type float64.
        Converts categorial data into integral data.
        '''
        temp = []
        for row in range(0, len(data)):
            for val in range(0, len(data[row])):
                try:
                    data[row][val] = float(data[row][val])
                except ValueError as err:
                    if data[row][val] not in temp:
                        temp.append(data[row][val])
                    data[row][val] = temp.index(
                                                    data[row][val])
        return np.array(data)

    def extractLabels(self, data, label_col, ltype):
        labels = []
        for row_num, row in enumerate(data):
            labels.append(row[label_col])
            row = [val for i, val in enumerate(row) if i != label_col]
            data[row_num] = row

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
