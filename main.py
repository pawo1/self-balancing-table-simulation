from math import sqrt
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure


file = open("data", "r")
file = file.readlines()
y = list(map(float, file))
x = [i for i in range(len(y))]
source = ColumnDataSource(data=dict(x=x, y=y))


""" plots """
plot_xy = figure(title="XY", tools="pan,reset,save,wheel_zoom", x_range=[-100, 100], y_range=[-100, 100])
plot_xy.sizing_mode = 'stretch_both'
plot_xy.line('x', 'y', source=ColumnDataSource(data=dict(x=[i for i in range(-100, 100)], y=[i for i in range(-100, 100)])))

plot_x_axis = figure(title="X axis", tools="pan,reset,save,wheel_zoom")
plot_x_axis.sizing_mode = 'stretch_both'
plot_x_axis.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

plot_y_axis = figure(title="Y axis", tools="pan,reset,save,wheel_zoom")
plot_y_axis.sizing_mode = 'stretch_both'
plot_y_axis.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


""" widgets """
slider_1 = Slider(title="Slider 1", value=5.0, start=0.0, end=10.0, step=0.5)
slider_2 = Slider(title="Slider 2", value=5.0, start=0.0, end=10.0, step=0.5)
slider_3 = Slider(title="Slider 3", value=5.0, start=0.0, end=10.0, step=0.5)
range_slider_1 = RangeSlider(title="Range slider 1", value=(0, 10), start=0, end=100, step=1)
text_input_1 = TextInput(title="Text input 1", value=str(12.5))
text_input_2 = TextInput(title="Text input 2", value=str(14.0))
text_input_3 = TextInput(title="Text input 3", value=str(1.5))


curdoc().add_root(row(
    column(slider_1, slider_2, slider_3, range_slider_1, row(text_input_1, text_input_2, text_input_3)),
    column(plot_xy, row(plot_x_axis, plot_y_axis), sizing_mode='stretch_both'),
    sizing_mode='stretch_both'))
curdoc().title = "Self-balancing table simulation mockup"
