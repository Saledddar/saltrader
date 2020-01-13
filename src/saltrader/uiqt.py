from    matplotlib.backends.backend_qt5agg  import  FigureCanvasQTAgg       as FigureCanvas
from    matplotlib.backends.backend_qt5agg  import  NavigationToolbar2QT    as NavigationToolbar
from    PyQt5.QtWidgets                     import  QApplication, QMainWindow   ,QMenu      ,QVBoxLayout    ,\
                                                    QSizePolicy , QMessageBox   ,QWidget    ,QPushButton    ,\
                                                    QGroupBox   , QGridLayout   ,QHBoxLayout,QCheckBox      ,\
                                                    QComboBox   , QListWidget   ,QLineEdit  ,QLabel         ,\
                                                    QScrollArea , QTabWidget    ,QCalendarWidget
from    PyQt5.QtGui                         import  QIcon
from    PyQt5                               import  QtWidgets   , QtGui         , QtCore
from    matplotlib.figure                   import  Figure
from    pandas.plotting                     import  register_matplotlib_converters
from    mpl_finance                         import  candlestick2_ohlc

from    collections                         import  OrderedDict
from    .project                            import  Project

import  matplotlib.pyplot                   as      plt
import  pandas                              as      pd 
import  saltools.autoreload                 as      sta
import  saltools.logging                    as      stl

import  sys

class WidgetPlot(QWidget        ):
    def __init__(
        self    , 
        *args   , 
        **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
class PlotCanvas(FigureCanvas   ):

    def __init__(
        self            , 
        parent  = None  , 
        width   = 5     , 
        height  = 4     , 
        dpi     = 100   ):
        fig = Figure(
            figsize = (width, height)   , 
            dpi     = dpi               )
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
                self                    ,
                QSizePolicy.Expanding   ,
                QSizePolicy.Expanding   )
        FigureCanvas.updateGeometry(self)

        

    def plot_htf(
            self                ,
            df                  ,
            supply_start        , 
            supply_end          , 
            demand_start        , 
            demand_end          ,
            parts               ):
        self.axes.clear()
        plot_htf(
            df                  ,
            supply_start        , 
            supply_end          , 
            demand_start        , 
            demand_end          ,
            parts               ,
            self.axes           )
        self.draw()
    def plot_itf(self,  dfi):
        self.axes.clear()
        plot_itf(dfi, self.axes)
        self.draw()
    def plot_ltf(
        self    ,  
        dfl     ,
        d_zones ,
        s_zones ):
        self.axes.clear()
        plot_ltf(dfl, d_zones, s_zones, self.axes)
        self.draw()

class App(QWidget):
    def __init__(
        self    ,
        project ):
        super().__init__()
        self.title  = 'GUI'
        self.left   = 100
        self.top    = 100
        self.width  = 640
        self.height = 480
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.project    = project
        self._create_layout()

        self.show()
    
    def _create_layout(
        self    ):
        pass


def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

if __name__ == '__main__':
    main()