'''
ExoPlanet Start Application
Copyright (C) 2016  Abhijit J. Theophilus

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


import sys
import os
from PyQt4 import QtGui
from UI import ExoPlanet


# Set Default Styles
# === ======= ======

def setDefaults(app):
    rootpath = os.getcwd()
    style_file = os.path.join('Info', 'Styles', 'AppStyles.qss')
    if os.path.isfile(style_file):
        with open(style_file) as stylePage:
            style = stylePage.read()
    try:
        app.setStyleSheet(style)
    except Exception as err:
        logging.error('StartApp:Error in applying styles.')
        logging.error('StartApp:' + str(err))
    appFont = app.font()
    appFont.setStyleStrategy(QtGui.QFont.PreferQuality)


# Main
# ====

def main():
    app = QtGui.QApplication(sys.argv)
    setDefaults(app)
    exo = ExoPlanet()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
