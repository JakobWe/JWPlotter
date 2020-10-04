from enum import Enum


class AppendPlot:
    def __init__(self, canvas, title, ylabel, xlabel):
        plot = canvas.addPlot(title=title)
        plot.setLabel("left", ylabel)
        plot.setLabel("bottom", xlabel)
        plot.showGrid(x=True, y=True, alpha=0.8)
        self.plot = plot.plot(pen='b')
        self.values = []

    def update_plot(self, message):
        _, title, value = message
        self.values.append(value)
        self.plot.setData(self.values)

    def clear_plot(self):
        print("i am called!11")
        self.values = []
        self.plot.setData(self.values)
        # self.plot.clear()


class ReplacePlot:
    def __init__(self, canvas, title, ylabel, xlabel):
        plot = canvas.addPlot(title=title)
        plot.setLabel("left", ylabel)
        plot.setLabel("bottom", xlabel)
        plot.showGrid(x=True, y=True, alpha=0.8)
        self.plot = plot.plot(pen='r')

    def update_plot(self, message):
        _, title, values = message
        self.plot.setData(values)

    def clear_plot(self):
        print("i am called!")
        self.plot.setData([1])


class Modes(Enum):
    APPEND = AppendPlot
    REPLACE = ReplacePlot
