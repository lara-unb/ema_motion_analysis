""" Defines DataMonitor class
"""

from multiprocessing import Process, Queue, TimeoutError
from multiprocessing.connection import Connection
from queue import Empty
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

class ExitDataMonitorException(Exception):
    pass
class DataMonitor(object):
    """ DataMonitor class encapsulate threads logic to plot data in a non-block
    way.

    """

    def __init__(self, data = None, channels = [{}], size_of_graph=1000):
        """ Constructs a DataMonitor instance.
        
        Args: 
            data:
            channels: list with channels dictionaryies that should contain keys:
            title, color, y_label, x_label, width and y_limit (optional)
            size_of_graph: int that represents the size of graph
        
        """
        # data handling
        self._data = data
        self.data_vector = []

        # Initialize graph vectors
        self.channels = []
        index = 0
        for channel in channels:
            aux_channel = {
                'data': [0]*size_of_graph,
                'index':index,
            }
            for key in channel.keys():
                aux_channel[key] = channel[key]
            self.channels.append(aux_channel)
            index+=1
        self.t = [0]*size_of_graph

        # Initialize timer
        self.start_time = time.time()

        # animation handling
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
        raise ExitDataMonitorException("Left data monitor.")
    def start(self):
        """ Starts the QtCore.QTimer() as subprocess (non-blocking, 
        queue communication) 
        
        """
        self._data_queue = Queue()
        self._show_process = Process(name='animate', 
                                    target=self.show, 
                                    args=(self._data_queue,))
        self._show_process.start()

    def stop(self):
        """ Stop a potentially running QtCore.QTimer() as subprocess 
        
        """
        if self._show_process is not None:
            self.__exit__(None, None, None)

    def show(self, data_queue: Connection):
        """ Creates the QtCore.QTimer() and creates the plot (blocking) 
        
        """
        # Set _data_queue and app atributes
        self._data_queue = data_queue
        self.app = QtGui.QApplication([])

        # Define background and foreground colors
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.win = pg.GraphicsWindow()

        
        # Create plots automatically
        for channel in self.channels:
            channel['plot'] = self.win.addPlot(colspan=2)
            self.win.nextRow()

        # Add title or labels color and width - https://linuxhint.com/use-pyqtgraph/
        for channel in self.channels:
            channel['plot'].setTitle(channel['title'])
            channel['plot'].setLabel('left', channel['y_label'])
            channel['plot'].setLabel('bottom', channel['x_label'])
            if('y_limit' in channel):
                channel['plot'].setYRange(channel['y_limit'][0], 
                                         channel['y_limit'][1], 
                                         padding=0)
            
            pen = pg.mkPen(channel['color'], 
                          width=channel['width'], 
                          style=QtCore.Qt.SolidLine)
            channel['curve'] = channel['plot'].plot(pen = pen)

        graph_update_ms = 1
        timer = QtCore.QTimer()
        timer.timeout.connect(self.animate)
        timer.start(graph_update_ms)   
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
            which is then received by the qt plot animation.
        
        """

        self._data_queue.put(value)

    def animate(self):
        """ The update method of qt plot animation 
        
        """
        data = self.data
        if data is not None:
            self.data_vector.append(data)

        if data is None:
            return

        # Set data for each plot
        for channel in self.channels:
            channel['data'][0:-1] = channel['data'][1:]
            channel['data'][-1] = data['data'][channel['index']]

        self.t[0:-1] = self.t[1:]
        self.t[-1] = data['time']

        for channel in self.channels:
            channel['curve'].setData(self.t, channel['data'])

        self.app.processEvents()  


# Run this function to understand this module usage
if __name__ == '__main__':
    # Define amount of channels and it's caracteristics
    channels = [
        {
            'title': "Angle 1", 
            'color': 'cyan', 
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2,
        }, 
        {
            'title': 'Angle2', 
            'color': 'pink',
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 2
        },
        {
            'title': 'Angle3', 
            'color': 'blue',
            'y_label': 'Angle(deg)', 
            'x_label': "Time(s)", 
            "width": 4
        }
    ]
    with DataMonitor(channels=channels) as dm:
        startTime = time.time()
        for i in range(20):
            # update data monitored
            dm.data = {
                "data": (2*np.random.rand(), np.random.rand(), np.random.rand()),
                "time": time.time() - startTime
            }
            time.sleep(1)

        