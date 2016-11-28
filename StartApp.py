
# Imports
# =======


import sys
import os
from PyQt4 import QtGui
from UI.ExoPlanet import ExoPlanet


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
    startLogs()
    app = QtGui.QApplication(sys.argv)
    setDefaults(app)
    exo = ExoPlanet()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
