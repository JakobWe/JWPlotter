from jw_plotter.PlotImplementations import Modes
import jw_plotter.pyqt_liveplotter_creatorconnector


__client = pyqt_liveplotter_creatorconnector.pyqt_liveplotter_creatorconnector(
    "Mein zwei live")


update_plot = __client.update_plot
create_plot = __client.create_plot
start_run = __client.start_run
clear_plot = __client.clear_plot
exit = __client.exit
Modes = Modes

__all__ = ["update_plot", "create_plot",
           "clear_plot", "exit", "start_run", "Modes"]
