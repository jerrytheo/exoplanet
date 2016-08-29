
# Imports
# =======


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from os import path


#-----------------------------------------------------------------------------#

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
        
        
#-----------------------------------------------------------------------------#
