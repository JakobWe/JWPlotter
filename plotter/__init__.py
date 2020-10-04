from plotter.pyqtgraph_live_plotter import PyQtLivePlotterCreatorConnector
from plotter.PlotImplementations import Modes


__client = PyQtLivePlotterCreatorConnector("Mein eins live")


update_plot = __client.update_plot
create_plot = __client.create_plot
start_run = __client.start_run
clear_plot = __client.clear_plot
exit = __client.exit
Modes = Modes

__all__ = ["update_plot", "create_plot",
           "clear_plot", "exit", "start_run", "Modes"]
