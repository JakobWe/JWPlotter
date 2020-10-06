from enum import Enum
from abc import ABC, abstractmethod


class AbstractPlot(ABC):
    def __init__(self, canvas, title, kwargs):
        xlabel = kwargs.pop('xlabel', 'x-axis')
        ylabel = kwargs.pop('ylabel', 'y-axis')

        plot = canvas.addPlot(title=title)

        plot.showGrid(x=True, y=True, alpha=0.8)
        plot.setLabel("left", ylabel)
        plot.setLabel("bottom", xlabel)
        self.plot = plot.plot(pen='b')

    @abstractmethod
    def update_plot(self):
        pass

    @abstractmethod
    def clear_plot(self):
        pass

    def set_plot_color(self, color):
        self.plot.setPen(color)


class AppendPlot(AbstractPlot):
    def __init__(self, canvas, title, kwargs):
        super().__init__(canvas, title, kwargs)

        self.values = []

    def update_plot(self, message):
        _, _, value = message
        self.values.append(value)
        self.plot.setData(self.values)

    def clear_plot(self):
        self.values = []
        self.plot.setData(self.values)


class ReplacePlot(AbstractPlot):
    def __init__(self, canvas, title, kwargs):
        super().__init__(canvas, title, kwargs)
        super().set_plot_color('r')

    def update_plot(self, message):
        _, _, values = message
        self.plot.setData(values)

    def clear_plot(self):
        self.values = []
        self.plot.setData(self.values)


class Modes(Enum):
    APPEND = AppendPlot
    REPLACE = ReplacePlot
