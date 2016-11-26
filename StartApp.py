
# Imports
# =======


import sys
import os
from datetime import date, datetime
import logging
from PyQt4 import QtGui
from UI.ExoPlanet import ExoPlanet


# Logging Init.
# ======= ====


def startLogs():
    logdir = os.getcwd()
    logdir = os.path.join(logdir, 'logs')
    if not os.path.isdir(logdir):
        os.mkdir(logdir)
    dt = str(date.today()).split('-')
    dt.reverse()
    dt[2] = dt[2].split('0')[1]
    dt = ''.join(dt)

    logfile = '-'.join(('Exo', dt)) + '.log'
    logfile = os.path.join(logdir, logfile)
    logging.basicConfig(filename=logfile, format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    tm = datetime.now().strftime('%H:%M:%S')
    logging.info('StartApp:Starting application at ' + tm)


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
