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
            "create_plot": self._register_new_plot
        }

    def _register_new_plot(self, data_array, xlabel="xachse", ylabel="yachse"):
        _, title, mode = data_array
        self.plots[title] = mode.value(self.canvas, title, ylabel, xlabel)

        if len(self.plots) % self.columns == 0:
            self.canvas.nextRow()

    def _new_update(self, message):
        self.plots[message[1]].update_plot(message)

        pg.QtGui.QApplication.processEvents()

    def await_pipe(self):
        try:
            while self.pqueue.qsize() > 0:
                data = self.pqueue.get()
                self.decoder[data[0]](data)
        except:
            print("I'm done")
            self.timer.stop()
            self.timer.deleteLater()
            self.exit(None)

    def exit(self, data):
        sys.exit()

    def save_fig(self, data):
        exporter = pg.exporters.ImageExporter()
        # set export parameters if needed
        # (note this also affects height parameter)
        exporter.parameters()['width'] = 100
        # save to file
        exporter.export('results/result.png')


class PyQtLivePlotterCreatorConnector:
    def __init__(self, title):
        self.title = title
        self.parent_conn = None
        self.pqueue = None
        self.plotting = False

    def create_pyqt_liveplotter(self, title):
        app = QtGui.QApplication(sys.argv)
        thisapp = PyQtLivePlotter(title, self.pqueue)
        thisapp.show()
        app.exec_()

    def update_plot(self, plot_num, values):
        if self.plotting:
            self.pqueue.put(tuple(["single_datapoint", plot_num, values]))

    def create_plot(self, title, mode=Modes.REPLACE):
        if self.plotting:
            self.pqueue.put(tuple(["create_plot", title, mode]))

            def update_function(values):
                return self.update_plot(title, values)
            return update_function

        def update_function(_):
            pass
        return update_function

    def save_fig(self):
        if self.plotting:
            self.pqueue.put(tuple(["save_fig", None]))

    def exit(self):
        if self.plotting:
            self.pqueue.put(tuple(["exit", None]))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    def __enter__(self):
        pass

    def start_run(self, plotting):
        self.plotting = plotting
        if plotting:
            print("plotting!")
            self.parent_conn, child_conn = Pipe()
            self.pqueue = Queue()
            process = Process(
                target=self.create_pyqt_liveplotter, args=(self.title,))
            process.start()
        else:
            print("not plotting!")

        return self
