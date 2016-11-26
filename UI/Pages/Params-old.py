
# Imports
# =======


import sys
import json
import logging
from os import path
from PyQt4 import QtGui, QtCore
from ..Base import ExoBase, MultiInput, MaterialShadow


# Parameters UI
# ========== ==

class ParameterForm(ExoBase):

    '''
    Page used to set the parameters of the selected algorithm.
    Generated from the parameter details stored in JSON files.
    '''

    def __init__(self, parent, algorithm, learning_type, params=None):
        self.inputs = {
            'int': self.intInput,
            'float': self.floatInput,
            'combo': self.comboInput,
            'multi': self.multiInput
        }
        super().__init__(parent)
        self._elements = {}
        self._defaults = {}
        self._param_details = {}

        self.setupForm(algorithm_type, algorithm, params)
        self.initiateDefaultState()

    def makeConnections(self, layout):
        '''
        Initialise the AlgoFile page.
            1. Sets layout for AlgoFile.
            2. Connects the clicked signals for startButton and backButton.
            3. Checks the conditions criteria for each parameter and disables
               the corresponding widgets.
        '''
        super().initUI(layout)
        for algo in self._param_details:
            elements = self._elements[algo]

            for para in elements:
                info = self._param_details[algo][para]
                if not isinstance(info, dict):
                    continue

                if 'conditions' in info:
                    if info['type'] == 'combo':
                        index = elements[para][1].currentIndex()
                        val = info['opts'][index]

                        for chk in info['conditions'][val]:
                            if not chk[1]:
                                lab, ele = elements[chk[0]]
                                lab.setVisible(False)
                                ele.setVisible(False)

                    elif info['type'] == 'int' or info['type'] == 'float':
                        x = elements[para][1].text()

                        if info['type'] == 'int':
                            x = int(x)
                        else:
                            round(float(x), 6)

                        for chk in info['conditions']:

                            if eval(chk):

                                for para in info['conditions'][chk]:
                                    lab, ele = elements[para[0]]
                                    if not para[1]:
                                        lab.setVisible(False)
                                        ele.setVisible(False)

    def createLayout(self, algo, algotype, params):
        '''
        Creates the layout to set the parameters of the algorithm.
        1. Builds a layout for each algorithm as follows:
            1. Read the JSON file corresponding to the algorithm type.
            2. Select the parameters corresponding to the algorithm from the
               JSON object.
            3. Build the layout for the parameters using createAlgoLayout.
        2. Creates a start button to initialise training.
        '''
        # Labels, Back button
        # Create individual layouts
        for i, val in enumerate(algo):
            fname = files[algotype[i]]
            fname = path.join('Info', 'Parameters', fname)
            with open(fname) as jfile:
                param_details = json.load(jfile)
                param_details = param_details[algotype[i]][val]
                self._param_details[val] = param_details
                if params is not None:
                    self.setDefaults(params[val], val)

            layout = self.createAlgoLayout(val)
            cards.append(self.createCard(val, layout))
        
        vbox = self.createCardLayout(*cards)
        vbox = self.vboxCreate(40, hboxStart, 40, hboxBtm, vbox=vbox)
        return vbox


    def createAlgoLayout(self, algo):
        '''
        Creates the layout for the parameters of each algorithm.
            1. If the parameter details is a dict, builds the necessary
               widget(s) to change its value.
            2. Otherwise, stores the value of the parameter as a default value.
        '''

        # Generating Elements
        elements = {}
        formPara = QtGui.QFormLayout()
        defaults = {}

        self._elements[algo] = elements

        params = list(self._param_details[algo].keys())
        params.sort()
        params_noncombo = []
        params_combo = []
        for para in params:
            if not isinstance(self._param_details[algo][para], dict): continue
            if self._param_details[algo][para]['type'] in ('combo', 'multi'):
                params_combo.append(para)
            else: params_noncombo.append(para)
        del params
        params = [*params_combo, *params_noncombo]

        for para in params:
            ele_info = self._param_details[algo][para]
            if isinstance(ele_info, dict):
                elements[para] = self.getElement(para, ele_info)
                formPara.addRow(*elements[para])
            else:
                defaults[para] = ele_info
        
        self._defaults[algo] = defaults
        formPara.setLabelAlignment(QtCore.Qt.AlignRight)
        formPara.setVerticalSpacing(15)
        formPara.setHorizontalSpacing(25)
        hboxPara = self.hcenter(formPara)

        return hboxPara

    
    def getElement(self, para, info):
        '''
        Creates the appropriate widget to read parameter value.
        '''
        
        ele = self.inputs[info['type']](info)
        
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
        comb = QtGui.QComboBox()
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
        else: intIP = False
        if 'float' in info['types']:
            floatIP = True
        else: floatIP = False
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
        for algo in self._elements:
            for para in self._elements[algo]:
                lab, ele = self._elements[algo][para]
                if ele is sender:
                    flag = True
                    break
            if flag:
                break
        
        info = self._param_details[algo][para]
        if 'conditions' not in info: return
        elements = self._elements[algo]
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


    def getVal(self):
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

        param_list = {}
        for algo in self._elements:
            algo_param = self._defaults[algo]
            for parameter in self._elements[algo]:
                ele = self._elements[algo][parameter][1]
                
                if self._param_details[algo][parameter]['type'] == 'int':
                    val = ele.text()
                    if val in self._param_details[algo][parameter]:
                        val = self._param_details[algo][parameter][val]
                    else:
                        state = ele.validator().validate(val, 0)[0]
                        if state != 2:
                            raise ValueError
                        val = int(val)

                elif self._param_details[algo][parameter]['type'] == 'float':
                    val = ele.text()
                    if val in self._param_details[algo][parameter]:
                        val = self._param_details[algo][parameter][val]
                    else:
                        state = ele.validator().validate(val, 0)[0]
                        if state != 2:
                            raise ValueError
                        val = float(val)

                elif self._param_details[algo][parameter]['type'] == 'combo':
                    val = ele.currentIndex()
                    val = self._param_details[algo][parameter]['vals'][val]
                
                elif self._param_details[algo][parameter]['type'] == 'multi':
                    val = ele.getValue()

                algo_param[parameter] = val

            param_list[algo] = algo_param

        return param_list


    def setDefaults(self, params, algo):
        '''
        Set default values for each parameter.
        '''
        for para in self._param_details[algo]:
            if isinstance(self._param_details[algo][para], dict):
                info = self._param_details[algo][para]
                for key in info:
                    try:
                        if info['type'] == 'int':
                            val = int(key)
                        elif info['type'] == 'float':
                            val = float(key)
                    except ValueError:
                        pass
                    else:
                        if params[para] == info[key]:
                            params[para] = val
                self._param_details[algo][para]['default'] = params[para]



#-----------------------------------------------------------------------------#