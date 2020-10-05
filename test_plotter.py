import plotter

with plotter.start_run(plotting=True):

    update_plt1 = plotter.create_plot(
        "plot1", mode=plotter.Modes.APPEND, xlabel="my_x_label", ylabel="my_y_label")
    # und dann
    plotter.update_plot("plot1", 0)
    plotter.update_plot("plot1", 1)
    plotter.update_plot("plot1", 2)
    # oder
    update_plt1(0)
    update_plt1(1)
    update_plt1(2)

    # bzw.
    update_plt2 = plotter.create_plot("plot2", mode=plotter.Modes.REPLACE)
    # und dann
    plotter.update_plot("plot2", [0, 1, 2])
    # oder
    update_plt2([0, 1, 2])

    plotter.clear_plot("plot1")

    plotter.update_plot("plot1", 3)
    plotter.update_plot("plot1", 4)
    plotter.update_plot("plot1", 5)

    while 1:
        pass
