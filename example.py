from math import sqrt

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure


def regulator(_fluid_level, _tank_cross_section, _min_level, _max_level, _sampling, _regulator_amp, _inflow_factor_min,
              _inflow_factor_max, _outflow_factor, _integral_action_time, _derivative_action_time, fluid_level_array,
              error_array, inflow_array, signal_array):
    """ PID regulator algorithm """

    # Step 1: Calculate regulation error.
    error = _fluid_level - fluid_level_array[-1]
    error_array.append(error)

    # Step 2: Calculate value of steering signal.
    signal = _regulator_amp * (error_array[-1] + (_sampling / _integral_action_time) * sum(error_array) + (
                (_derivative_action_time / _sampling) * (error_array[-2] - error_array[-1])))
    signal_array.append(signal)

    # Step 3: Calculate value of inflow intensity.
    inflow = (_inflow_factor_max - _inflow_factor_min) / (_max_level - _min_level) * signal_array[-1]
    inflow_array.append(inflow)

    # Step 4: Calculate fluid level.
    current_fluid_level = float(
        1 / _tank_cross_section * ((-_outflow_factor) * sqrt(fluid_level_array[-1]) + inflow_array[-1]) * _sampling +
        fluid_level_array[-1])
    if current_fluid_level > _max_level:
        current_fluid_level = _max_level
    elif current_fluid_level < _min_level:
        current_fluid_level = _min_level
    fluid_level_array.append(current_fluid_level)

    return current_fluid_level


""" widgets """
fluid_level_slider = Slider(title="Desired fluid level", value=5.0, start=0.0, end=10.0, step=0.5)
level_range_slider = RangeSlider(title="Tank min/max size", value=(0, 10), start=0, end=100, step=1)
tank_cross_section_text_input = TextInput(title="Tank Cross section area", value=str(1.5))
simulation_time_text_input = TextInput(title="Simulation time", value=str(3600 * 4))

sampling_slider = Slider(title="Sampling", value=0.10, start=0.05, end=1.0, step=0.05)
regulator_amp_slider = Slider(title="Amplification", value=0.015, start=0.005, end=1.00, step=0.005, format='0.000')
inflow_factor_range_slider = RangeSlider(title="Inflow factors", value=(0.00, 0.05), start=0.00, end=1.00, step=0.005,
                                         format='0.000')
outflow_factor_slider = Slider(title="Outflow factor", value=0.035, start=0.005, end=1.00, step=0.005, format='0.000')
integral_action_time_text_input = TextInput(title="Integral action time factor", value=str(0.05))
derivative_action_time_text_input = TextInput(title="Derivative action time factor", value=str(0.25))

""" plot settings """
plot = figure(title="Fluid Tank simulation",
              tools="pan,reset,save,wheel_zoom",
              x_range=[0, 3600 * 4], y_range=[0, 10], height=500, width=1200)
plot.sizing_mode = 'scale_width'

""" load default plot """
file = open("data", "r")
file = file.readlines()
y = list(map(float, file))
x = [i for i in range(len(y))]
source = ColumnDataSource(data=dict(x=x, y=y))
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


def update_data(attrname, old, new):
    """ update callback """

    # load widgets data
    fluid_level = fluid_level_slider.value  # m
    min_level = level_range_slider.value[0]  # m
    max_level = level_range_slider.value[1]  # m
    tank_cross_section = float(tank_cross_section_text_input.value)  # m^2
    simulation_time = simulation_time_text_input.value  # s

    sampling = sampling_slider.value  # s
    regulator_amp = regulator_amp_slider.value
    inflow_factor_min = inflow_factor_range_slider.value[0]  # m^3/s
    inflow_factor_max = inflow_factor_range_slider.value[1]  # m^3/s
    outflow_factor = outflow_factor_slider.value  # m^3/s

    integral_action_time = float(integral_action_time_text_input.value)
    derivative_action_time = float(derivative_action_time_text_input.value)

    # generate regulator arrays
    x_axis = []
    y_axis = []
    fluid_level_array = [float(min_level)]
    error_array = [float(fluid_level)]
    inflow_array = []
    signal_array = []

    # main simulation loop
    for n in range(0, int(simulation_time)):
        x_axis.append(n)
        y_axis.append(
            regulator(fluid_level, tank_cross_section, min_level, max_level, sampling, regulator_amp, inflow_factor_min,
                      inflow_factor_max, outflow_factor, integral_action_time, derivative_action_time,
                      fluid_level_array, error_array, inflow_array, signal_array))

    # update plot
    source.data = dict(x=x_axis, y=y_axis)

    # update sliders and grid range
    plot.y_range.start = min_level
    plot.y_range.end = max_level
    fluid_level_slider.start = min_level
    fluid_level_slider.end = max_level
    plot.x_range.end = int(simulation_time)


# column 1
fluid_level_slider.on_change('value_throttled', update_data)
level_range_slider.on_change('value_throttled', update_data)
tank_cross_section_text_input.on_change('value', update_data)
simulation_time_text_input.on_change('value', update_data)

# column 2
sampling_slider.on_change('value_throttled', update_data)
regulator_amp_slider.on_change('value_throttled', update_data)
inflow_factor_range_slider.on_change('value_throttled', update_data)
outflow_factor_slider.on_change('value_throttled', update_data)

# column 3
integral_action_time_text_input.on_change('value', update_data)
derivative_action_time_text_input.on_change('value', update_data)

inputs_1 = column(fluid_level_slider, level_range_slider, tank_cross_section_text_input, simulation_time_text_input,
                  sizing_mode='scale_width')
inputs_2 = column(sampling_slider, regulator_amp_slider, inflow_factor_range_slider, outflow_factor_slider,
                  sizing_mode='scale_width')
inputs_3 = column(integral_action_time_text_input, derivative_action_time_text_input, sizing_mode='scale_width')
curdoc().add_root(column(plot, row(inputs_1, inputs_2, inputs_3), sizing_mode='scale_width'))
curdoc().title = "PID regulator example"
