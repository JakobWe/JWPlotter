import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Pipe, Queue
import threading
import pyqtgraph.exporters
from enum import Enum
from plotter.PlotImplementations import Modes


class PyQtLivePlotter(QtGui.QMainWindow):
    def __init__(self, title, pqueue, parent=None):
        super(PyQtLivePlotter, self).__init__(parent)

        pg.setConfigOptions(antialias=True)

        self.pqueue = pqueue

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)

        self.label.setText(title)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.await_pipe)
        self.timer.setInterval(1000)
        self.timer.start()

        self.columns = 3

        self.plots = {}

        self.decoder = {
            "exit": self.exit,
            "save_plot": self.save_fig,
            "single_datapoint": self._new_update,
            "create_plot": self._register_new_plot,
            "clear_plot": self._clear_plot,
        }

    def _register_new_plot(self, data_array):
        _, title, mode, kwargs = data_array
        self.plots[title] = mode.value(self.canvas, title, kwargs)

        if len(self.plots) % self.columns == 0:
            self.canvas.nextRow()

    def _new_update(self, message):
        self.plots[message[1]].update_plot(message)

        pg.QtGui.QApplication.processEvents()

    def await_pipe(self):
        while self.pqueue.qsize() > 0:
            data = self.pqueue.get()
            self.decoder[data[0]](data)

    def await_pipe_old(self):
        try:
            while self.pqueue.qsize() > 0:
                data = self.pqueue.get()
                self.decoder[data[0]](data)
        except:
            self.timer.stop()
            self.timer.deleteLater()
            self.exit(None)

    def _clear_plot(self, message):
        self.plots[message[1]].clear_plot()

    def exit(self, data):
        sys.exit()

    def save_fig(self, data):
        exporter = pg.exporters.ImageExporter(self.plots)
        # set export parameters if needed
        # (note this also affects height parameter)
        exporter.parameters()['width'] = 100
        # save to file
        exporter.export('results/result.png')
