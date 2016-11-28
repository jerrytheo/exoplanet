'''
ExoPlanet Canvas Base Class
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

from os import path
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure
import matplotlib


# Base Canvas
# ==== ======

class ExoCanvas(FigureCanvas):

    '''
    Base class to build graphs and plots.
    '''

    def __init__(self, parent, dpi):
        self.fig = Figure(dpi=dpi, facecolor='white', edgecolor='white')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        matplotlib.rcParams.update({
            'font.size': 12,
        })
        self.setObjectName('Canvas')

    def initFigure(self, x, y, title=None, color='black'):
        '''
        Initialise figure by plotting the initial state of the graph.
        '''

        self.axes.plot(x, y, color=color)
        if title is not None:
            self.fig.suptitle(title)

    def save(self, dname, figname):
        '''
        Save the current instance of the graph.
        '''
        fname = path.join(dname, figname+'.png')
        self.fig.savefig(fname, dpi=200, format='png')
