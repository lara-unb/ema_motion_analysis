from multiprocessing import Process, Queue, TimeoutError
from multiprocessing.connection import Connection
from queue import Empty
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
class DataMonitor(object):
    """ Data Monitoring of externally manipulated data
        The data-monitor runs matplotlib in an extra multiprocessing.Process.
        For a clean subprocess handling it is recommended to use DataMonitor in the with environment:
        > with DataMonitor(channels=..., ...) as dm:
        >     while True:
        >         dm.data = <update data from external source>
        >         <do something else>
    """

    def __init__(self, data = None):
        """ Constructs a DataMonitor instance
        """
        # data handling
        self._data = data
        self.data_vector = []

        # Initialize graph vectors
        size_of_graph = 1000
        self.curve1_plot = [0]*size_of_graph
        self.curve2_plot = [0]*size_of_graph
        self.t = [0]*size_of_graph

        # Initialize timer
        self.start_time = time.time()


        # animation handling
        self._func_animation = None
        self.update_rate = 0.1

        # multiprocess handling
        self._show_process = None
        self._data_queue = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit real time data monitor.")
        if self._show_process is not None:
            if exc_type is not None:
                try:
                    self._show_process.terminate()
                except:
                    pass

            self._show_process.join()
            self._show_process = None

        if self._data_queue is not None:
            while not self._data_queue.empty():
                try:
                    self._data_queue.get(timeout=0.001)
                except (TimeoutError, Empty):
                    pass

            self._data_queue.close()
            self._data_queue = None

    def start(self):
        """ Starts the matplotlib FuncAnimation as subprocess (non-blocking, queue communication) """
        self._data_queue = Queue()
        self._show_process = Process(name='animate', target=self.show, args=(self._data_queue, ))
        self._show_process.start()

    def stop(self):
        """ Stop a potentially running matplotlib FuncAnimation as subprocess """
        if self._show_process is not None:
            self.__exit__(None, None, None)

    def show(self, data_queue: Connection):
        """ Creates the matplotlib FuncAnimation and creates the plot (blocking) """
        # 
        self._data_queue = data_queue
        self.app = QtGui.QApplication([])

        # Define background and foreground colors
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.win = pg.GraphicsWindow()

        self.p1 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.win.nextRow()

        # https://pyqtgraph.readthedocs.io/en/latest/introduction.html
        # https://linuxhint.com/use-pyqtgraph/
        # Add title or labels
        self.p1.setTitle("Angle 1")
        self.p2.setTitle("Angle 2")
        self.p1.setLabel('left', "Angles(deg)")
        self.p2.setLabel('left', "Angles(deg)")
        self.p1.setLabel('bottom', "Time(s)")
        self.p2.setLabel('bottom', "Time(s)")
        # self.p1.showGrid(x=True, y=True)
              
        # Define ploting line styles
        pen1 =pg.mkPen('cyan', width=2, style=QtCore.Qt.DashLine, label="angle 1")
        pen2 =pg.mkPen('pink', width=2, style=QtCore.Qt.DashLine)
        self.curve1 = self.p1.plot(pen=pen1, labels='Angle 1' )
        self.curve2 = self.p2.plot(pen=pen2, title='Angle 2')

        graphUpdateSpeedMs = 1
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.animate)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()

    @property
    def data(self):
        """ Data property (getter) which tries to read from a
            multiprocessing queue and returns the current data array
            on default.
        """
        try:
            if self._data is not None:
                data = self._data
                self._data = None

            else:
                data = self._data_queue.get(timeout=self.update_rate)

        except (TimeoutError, Empty):
            data = None

        return data

    @data.setter
    def data(self, value):
        """ Puts data to the multiprocessing data queue
            which is then received by the function animation.
        """

        self._data_queue.put(value)

    def animate(self):
        """ The update method of the matplotlib function animation """
        data = self.data
        if data is not None:
            self.data_vector.append(data)

        if data is None:
            return

        self.curve1_plot[0:-1] = self.curve1_plot[1:]
        self.curve1_plot[-1] = data
        self.curve2_plot[0:-1] = self.curve2_plot[1:]
        self.curve2_plot[-1] = -data

        self.t[0:-1] = self.t[1:]
        self.t[-1] = time.time() - self.start_time

        self.curve1.setData(self.t, self.curve1_plot)
        self.curve2.setData(self.t, self.curve2_plot)
        self.app.processEvents()  


if __name__ == '__main__':
    with DataMonitor() as dm:
        for i in range(20):
            dm.data = np.random.rand()
            time.sleep(0.5);

        