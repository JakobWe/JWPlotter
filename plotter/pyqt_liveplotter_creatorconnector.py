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
from plotter.pyqt_live_plotter import PyQtLivePlotter


class pyqt_liveplotter_creatorconnector:
    def __init__(self, title):
        self.title = title
        self.pqueue = None
        self.plotting = True

    def create_pyqt_liveplotter(self, title):
        app = QtGui.QApplication(sys.argv)
        thisapp = PyQtLivePlotter(title, self.pqueue)
        thisapp.show()
        app.exec_()

    def update_plot(self, plot_num, values):
        if self.plotting:
            self.pqueue.put(tuple(["single_datapoint", plot_num, values]))

    def create_plot(self, title, mode=Modes.REPLACE, **kwargs):
        if self.plotting:
            self.pqueue.put(tuple(["create_plot", title, mode, kwargs]))

            def update_function(values):
                return self.update_plot(title, values)
            return update_function

        def empty_update_function(_):
            pass
        return empty_update_function

    def save_fig(self):
        if self.plotting:
            self.pqueue.put(tuple(["save_fig", None]))

    def exit(self):
        if self.plotting:
            self.pqueue.put(tuple(["exit", None]))

    def clear_plot(self, title):
        if self.plotting:
            self.pqueue.put(tuple(["clear_plot", title]))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    def __enter__(self):
        pass

    def start_run(self, plotting):
        self.plotting = plotting
        if plotting:
            self.pqueue = Queue()
            process = Process(
                target=self.create_pyqt_liveplotter, args=(self.title,))
            process.start()

        return self
