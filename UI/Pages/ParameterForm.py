'''
ExoPlanet Parameter Form
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

import json
from os import path
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MultiInput, ComboBox


# Parameters UI
# ========== ==

class ParameterForm(ExoBase):

    '''
    Page used to set the parameters of the selected algorithm.
    Generated from the parameter details stored in JSON files.
    '''

    def __init__(self, parent, algorithm, learning_type, default=None):
        self._inputs = {
            'int': self.intInput,
            'float': self.floatInput,
            'combo': self.comboInput,
            'multi': self.multiInput
        }
        super().__init__(parent)

        self._elements = {}
        self._defaults = {}
        self._metadata = {}

        self.setupForm(algorithm, learning_type, default)
        self.initiateDefaultState()

    def initiateDefaultState(self):
        '''
        Initialise the AlgoFile page.
            1. Sets layout for AlgoFile.
            2. Checks the conditions criteria for each parameter and disables
               the corresponding widgets.
        '''
        for parameter in self._elements:
            info = self._metadata[parameter]
            if not isinstance(info, dict):
                continue
            if 'conditions' in info:
                if info['type'] == 'combo':
                    index = self._elements[parameter][1].currentIndex()
                    val = info['opts'][index]
                    for chk in info['conditions'][val]:
                        if not chk[1]:
                            lab, ele = self._elements[chk[0]]
                            lab.setVisible(False)
                            ele.setVisible(False)
                elif info['type'] == 'int' or info['type'] == 'float':
                    x = self._elements[parameter][1].text()
                    if info['type'] == 'int':
                        x = int(x)
                    else:
                        round(float(x), 6)
                    for chk in info['conditions']:
                        if eval(chk):
                            for parameter in info['conditions'][chk]:
                                lab, ele = self._elements[parameter[0]]
                                if not parameter[1]:
                                    lab.setVisible(False)
                                    ele.setVisible(False)

    def setupForm(self, algorithm, learning_type, default):
        '''
        Creates the layout to set the parameters of the algorithm.
        1. Builds a layout for each algorithm as follows:
            1. Read the JSON file corresponding to the algorithm type.
            2. Select the parameters corresponding to the algorithm from the
               JSON object.
            3. Build the layout for the parameters using createAlgoLayout.
        2. Creates a start button to initialise training.
        '''
        fpath = '{0}.json'.format(learning_type)
        fpath = path.join('Info', 'Parameters', fpath)
        with open(fpath) as jfile:
            self._metadata = json.load(jfile)[learning_type][algorithm]
            if default is not None:
                self.setDefaults(default, algorithm)
        layout = self.createWidgetLayout()
        self.setLayout(layout)

    def createWidgetLayout(self):
        '''
        Creates the layout for the parameters of each algorithm.
            1. If the parameter details is a dict, builds the necessary
               widget(s) to change its value.
            2. Otherwise, stores the value of the parameter as a default value.
        '''
        # Generating Elements
        formPara = QtGui.QFormLayout()

        parameters = list(self._metadata.keys())
        parameters.sort()
        parameters_noncombo = []
        parameters_combo = []
        for parameter in parameters:
            if not isinstance(self._metadata[parameter], dict):
                continue
            if self._metadata[parameter]['type'] in ('combo', 'multi'):
                parameters_combo.append(parameter)
            else:
                parameters_noncombo.append(parameter)
        del parameters

        parameters = [*parameters_combo, *parameters_noncombo]
        for parameter in parameters:
            ele_meta = self._metadata[parameter]
            if isinstance(ele_meta, dict):
                self._elements[parameter] = self.getElement(parameter, ele_meta)
                formPara.addRow(*self._elements[parameter])
            else:
                defaults[parameter] = ele_meta

        formPara.setLabelAlignment(QtCore.Qt.AlignRight)
        formPara.setVerticalSpacing(15)
        formPara.setHorizontalSpacing(25)
        return formPara

    def getElement(self, para, info):
        '''
        Creates the appropriate widget to read parameter value.
        '''
        ele = self._inputs[info['type']](info)
        lab = QtGui.QLabel(info['title'])
        lab.setStatusTip(info['hint'])
        ele.setStatusTip(info['hint'])
        lab.setObjectName('FormLabel')
        return (lab, ele)

    def intInput(self, info):
        '''
        Creates the widget to read integer values and sets a validator to
        ensure valid input.
        '''
        input_valid = QtGui.QIntValidator()
        if 'min' in info:
            input_valid.setBottom(info['min'])
        if 'max' in info:
            input_valid.setTop(info['max'])
        edit = QtGui.QLineEdit(self)
        edit.setValidator(input_valid)
        edit.setText(str(info['default']))
        edit.editingFinished.connect(self.changeUI)
        return edit

    def floatInput(self, info):
        '''
        Creates the widget to read floating point values and sets a validator
        to ensure valid input.
        '''
        input_valid = QtGui.QDoubleValidator()
        input_valid.setDecimals(6)
        if 'fmin' in info:
            input_valid.setBottom(info['fmin'])
        if 'fmax' in info:
            input_valid.setTop(info['fmax'])
        edit = QtGui.QLineEdit(self)
        edit.setValidator(input_valid)
        edit.setText(str(info['default']))
        edit.editingFinished.connect(self.changeUI)
        return edit

    def comboInput(self, info):
        '''
        Creates the widget to select a value from a list of values.
        '''
        comb = ComboBox()
        comb.addItems(info['opts'])
        comb.currentIndexChanged[int].connect(self.changeUI)
        try:
            ind = info['vals'].index(info['default'])
            comb.setCurrentIndex(ind)
        except:
            pass
        return comb

    def multiInput(self, info):
        '''
        Creates the widget to select an object from a list and then may or may
        not allow an additional integer or floating point value.
        '''
        if 'int' in info['types']:
            intIP = True
        else:
            intIP = False
        if 'float' in info['types']:
            floatIP = True
        else:
            floatIP = False
        mulInp = MultiInput(self, intIP, floatIP, **info)
        return mulInp

    def changeUI(self):
        '''
        A change in a parameter's values triggers this function.
        Checks for the conditions section of the parameter details and disables
        widgets for which the conditions fail.
        '''
        sender = self.sender()
        flag = False
        for parameter in self._elements:
            lab, ele = self._elements[parameter]
            if ele is sender:
                flag = True
                break
        info = self._metadata[parameter]
        if 'conditions' not in info:
            return
        elements = self._elements
        if info['type'] == 'combo':
            index = sender.currentIndex()
            val = info['opts'][index]
            for chk in info['conditions'][val]:
                lab, ele = elements[chk[0]]
                if not chk[1]:
                    lab.setVisible(False)
                    ele.setVisible(False)
                else:
                    lab.setVisible(True)
                    ele.setVisible(True)

        elif info['type'] == 'int' or info['type'] == 'float':
            x = self.sender().text()
            x = int(x) if info['type'] == 'int' else round(float(x), 6)
            for chk in info['conditions']:
                if eval(chk):
                    for para in info['conditions'][chk]:
                        lab, ele = elements[para[0]]
                        if not para[1]:
                            lab.setVisible(False)
                            ele.setVisible(False)
                        else:
                            lab.setVisible(True)
                            ele.setVisible(True)

    def getParameters(self):
        '''
        For every algorithm, stores the value of every parameter in a dict and
        returns the dict.
            1. If the parameter type is combo,
                Get the index of value selected, and store the corresponding
                sklearn string.
            2. If the parameter type is int or float,
                1. Get the value from QLineEdit and validate it using the set
                   validator.
                2. If valid, store, otherwise raise ValueError
            3. If the parameter type is multi,
                Get its value and store.
        '''
        parameters = self._defaults
        for parameter in self._elements:
            ele = self._elements[parameter][1]

            if self._metadata[parameter]['type'] == 'int':
                val = ele.text()
                if val in self._metadata[parameter]:
                    val = self._metadata[parameter][val]
                else:
                    state = ele.validator().validate(val, 0)[0]
                    if state != 2:
                        raise ValueError
                    val = int(val)

            elif self._metadata[parameter]['type'] == 'float':
                val = ele.text()
                if val in self._metadata[parameter]:
                    val = self._metadata[parameter][val]
                else:
                    state = ele.validator().validate(val, 0)[0]
                    if state != 2:
                        raise ValueError
                    val = float(val)

            elif self._metadata[parameter]['type'] == 'combo':
                val = ele.currentIndex()
                val = self._metadata[parameter]['vals'][val]

            elif self._metadata[parameter]['type'] == 'multi':
                val = ele.getValue()
            parameters[parameter] = val

        return parameters

    def setDefaults(self, default):
        '''
        Set default values for each parameter.
        '''
        for parameter in self._metadata:
            if isinstance(self._metadata[parameter], dict):
                meta = self._metadata[parameter]
                for key in meta:
                    try:
                        if meta['type'] == 'int':
                            val = int(key)
                        elif meta['type'] == 'float':
                            val = float(key)
                    except ValueError:
                        pass
                    else:
                        if default[parameter] == meta[key]:
                            default[parameter] = val
                self._metadata[parameter]['default'] = default[parameter]

