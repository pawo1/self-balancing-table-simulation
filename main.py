import numpy as np

import controller
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, RadioButtonGroup, Toggle
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure


""" widgets """
tp_input = Slider(title="Sampling", value=0.010, start=0.005, end=1.000, step=0.005, format='0.000')
t_sim_input = TextInput(title="Simulation time", value=str(100))

# - Simulation 1
# --- Table
sim1_starting_x_pos_input = Slider(title="X position", value=25.0, start=-100, end=100, step=0.5, format='0.0')
sim1_starting_y_pos_input = Slider(title="Y position", value=-75.0, start=-100, end=100, step=0.5, format='0.0')

sim1_starting_x_spd_input = Slider(title="X velocity", value=-1, start=-30, end=30, step=0.5, format='0.0')
sim1_starting_y_spd_input = Slider(title="Y velocity", value=2, start=-30, end=30, step=0.5, format='0.0')

sim1_starting_x_ang_input = Slider(title="X angle", value=2.0, start=-90, end=90, step=0.5, format='0.0')
sim1_starting_y_ang_input = Slider(title="Y angle", value=-1.5, start=-90, end=90, step=0.5, format='0.0')

sim1_desired_x_pos_input = Slider(title="Desired X position", value=0, start=-100, end=100, step=0.5, format='0.0')
sim1_desired_y_pos_input = Slider(title="Desired Y position", value=0, start=-100, end=100, step=0.5, format='0.0')

# --- PID
sim1_pid_type_input = RadioButtonGroup(labels=["Positional", "Incremental"], active=1)
sim1_kp_input = Slider(title="Amplification", value=0.025, start=0.005, end=1.00, step=0.005, format='0.000')
sim1_ti_input = Slider(title="Integral action time factor", value=0.015, start=0.005, end=1.00, step=0.005, format='0.000')
sim1_td_input = Slider(title="Derivative action time factor", value=0.050, start=0.005, end=1.00, step=0.005, format='0.000')
sim1_servo_min_range_input = Slider(title="Servo minimal range", value=-15, start=-90, end=-1, step=1)
sim1_servo_max_range_input = Slider(title="Servo maximal range", value=15, start=1, end=90, step=1)


# --- Disturbances
sim1_dist_toggle = Toggle(label="Toggle disturbance", button_type='default')

sim1_x_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)
sim1_y_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)

sim1_x_dist_time_input = Slider(title="Disturbance duration", value=360, start=0, end=14400, step=1)
sim1_y_dist_time_input = Slider(title="Disturbance duration", value=180, start=0, end=14400, step=1)

sim1_x_dist_lvl_input = Slider(title="Level", value=-1, start=-15, end=15, step=1)
sim1_y_dist_lvl_input = Slider(title="Level", value=2, start=-15, end=15, step=1)

sim1_x_dist_freq_input = Slider(title="Frequency", value=0.100, start=0.001, end=10, step=0.005, format='0.000')
sim1_y_dist_freq_input = Slider(title="Frequency", value=0.125, start=0.001, end=10, step=0.005, format='0.000')


""" initial simulation """
initial_simulation = controller.Controller(tp=tp_input.value, t_sim=int(t_sim_input.value), kp=sim1_kp_input.value, ti=sim1_ti_input.value, td=sim1_td_input.value, pos_x=sim1_starting_x_pos_input.value, pos_y=sim1_starting_y_pos_input.value)
initial_simulation.run()
x = np.linspace(0, int(t_sim_input.value), int(int(t_sim_input.value) / tp_input.value))


""" data sources """
source_xy_pos = ColumnDataSource(data=dict(x=initial_simulation._table.get_pos_x_list(), y=initial_simulation._table.get_pos_y_list()))
source_x_pos = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_pos_x_list()))
source_y_pos = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_pos_y_list()))
source_x_spd = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_speed_x_list()))
source_y_spd = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_speed_y_list()))
source_x_ang = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_angle_x_list()))
source_y_ang = ColumnDataSource(data=dict(x=x, y=initial_simulation._table.get_angle_y_list()))


""" plots """
# --- XY position
xy_pos_plot = figure(title="table_position(x,y)", tools="pan,reset,save,wheel_zoom", x_range=[-100, 100], y_range=[-100, 100])
xy_pos_plot.sizing_mode = 'stretch_both'
xy_pos_plot.line('x', 'y', source=source_xy_pos)

# --- position
x_pos_plot = figure(title="pos_x(t)", tools="pan,reset,save,wheel_zoom")
x_pos_plot.sizing_mode = 'stretch_both'
x_pos_plot.line('x', 'y', source=source_x_pos, line_width=3, line_alpha=0.6)

y_pos_plot = figure(title="pos_y(t)", tools="pan,reset,save,wheel_zoom")
y_pos_plot.sizing_mode = 'stretch_both'
y_pos_plot.line('x', 'y', source=source_y_pos, line_width=3, line_alpha=0.6)

# --- Speed
x_spd_plot = figure(title="speed_x(t)", tools="pan,reset,save,wheel_zoom")
x_spd_plot.sizing_mode = 'stretch_both'
x_spd_plot.line('x', 'y', source=source_x_spd, line_width=3, line_alpha=0.6)

y_spd_plot = figure(title="speed_y(t)", tools="pan,reset,save,wheel_zoom")
y_spd_plot.sizing_mode = 'stretch_both'
y_spd_plot.line('x', 'y', source=source_y_spd, line_width=3, line_alpha=0.6)

# --- Angle
x_ang_plot = figure(title="angle_x(t)", tools="pan,reset,save,wheel_zoom")
x_ang_plot.sizing_mode = 'stretch_both'
x_ang_plot.line('x', 'y', source=source_x_ang, line_width=3, line_alpha=0.6)

y_ang_plot = figure(title="angle_y(t)", tools="pan,reset,save,wheel_zoom")
y_ang_plot.sizing_mode = 'stretch_both'
y_ang_plot.line('x', 'y', source=source_y_ang, line_width=3, line_alpha=0.6)


def update_data(attrname, old, new):
    """ update callback """

    # global variables
    tp = tp_input.value
    t_sim = int(t_sim_input.value)

    # - Simulation 1
    # --- Table
    sim1_starting_pos = (sim1_starting_x_pos_input.value, sim1_starting_y_pos_input.value)
    sim1_starting_spd = (sim1_starting_x_spd_input.value, sim1_starting_y_spd_input.value)
    sim1_starting_ang = (sim1_starting_x_ang_input.value, sim1_starting_y_ang_input.value)
    sim1_desired_pos = (sim1_desired_x_pos_input.value, sim1_desired_y_pos_input.value)
    # --- PID
    # sim1_pid_type = sim1_pid_type_input.value
    sim1_kp = sim1_kp_input.value
    sim1_ti = sim1_ti_input.value
    sim1_td = sim1_td_input.value
    sim1_servo_min_range = sim1_servo_min_range_input.value
    sim1_servo_max_range = sim1_servo_max_range_input.value

    simulation_1 = controller.Controller(tp=tp, t_sim=t_sim, kp=sim1_kp, ti=sim1_ti, td=sim1_td, pos_x=sim1_starting_pos[0], pos_y=sim1_starting_pos[1])
    simulation_1.run()

    # update plots
    source_xy_pos.data = dict(x=simulation_1._table.get_pos_x_list(), y=simulation_1._table.get_pos_y_list())

    axis = np.linspace(0, t_sim, int(t_sim / tp))
    source_x_pos.data = dict(x=axis, y=simulation_1._table.get_pos_x_list())
    source_y_pos.data = dict(x=axis, y=simulation_1._table.get_pos_y_list())

    source_x_spd.data = dict(x=axis, y=simulation_1._table.get_speed_x_list())
    source_y_spd.data = dict(x=axis, y=simulation_1._table.get_speed_y_list())

    source_x_ang.data = dict(x=axis, y=simulation_1._table.get_angle_x_list())
    source_y_ang.data = dict(x=axis, y=simulation_1._table.get_angle_y_list())


    # update sliders and grid range
    sim1_x_dist_time_input.end = int(t_sim)
    sim1_y_dist_time_input.end = int(t_sim)

    sim1_x_dist_lvl_input.start = sim1_servo_min_range
    sim1_x_dist_lvl_input.end = sim1_servo_max_range
    sim1_y_dist_lvl_input.start = sim1_servo_min_range
    sim1_y_dist_lvl_input.end = sim1_servo_max_range

    sim1_x_dist_freq_input.start = float(1 / float(t_sim))
    sim1_x_dist_freq_input.end = float(1 / float(tp))
    sim1_y_dist_freq_input.start = float(1 / float(t_sim))
    sim1_y_dist_freq_input.end = float(1 / float(tp))


for elem in [tp_input, sim1_starting_x_pos_input, sim1_starting_y_pos_input, sim1_starting_x_spd_input, sim1_starting_y_spd_input, sim1_starting_x_ang_input, sim1_starting_y_ang_input, sim1_desired_x_pos_input, sim1_desired_y_pos_input, sim1_kp_input, sim1_ti_input, sim1_td_input, sim1_servo_min_range_input, sim1_servo_max_range_input]:
    elem.on_change('value_throttled', update_data)

for elem in [t_sim_input]:
    elem.on_change('value', update_data)

""" tabs """
sim1_pid = Panel(child=layout(column(sim1_pid_type_input, sim1_kp_input, sim1_ti_input, sim1_td_input, row(sim1_servo_min_range_input, sim1_servo_max_range_input, sizing_mode='stretch_width'), sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="PID")
sim1_table = Panel(child=layout(column(row(sim1_starting_x_pos_input, sim1_starting_y_pos_input, sizing_mode='stretch_width'), sizing_mode='stretch_width'), row(sim1_starting_x_spd_input, sim1_starting_y_spd_input, sizing_mode='stretch_width'), row(sim1_starting_x_ang_input, sim1_starting_y_ang_input, sizing_mode='stretch_width'), column(sim1_desired_x_pos_input, sim1_desired_y_pos_input, sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="Table")
sim1_tabs = Tabs(tabs=[sim1_table, sim1_pid])

sim1_x_dist = Panel(child=layout(column(sim1_x_dist_type_input, sim1_x_dist_time_input, sim1_x_dist_lvl_input, sim1_x_dist_freq_input, sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="X disturbance")
sim1_y_dist = Panel(child=layout(column(sim1_y_dist_type_input, sim1_y_dist_time_input, sim1_y_dist_lvl_input, sim1_y_dist_freq_input, sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="Y disturbance")
sim1_dist_tabs = Tabs(tabs=[sim1_x_dist, sim1_y_dist])

sim1_tab = Panel(child=layout(column(sim1_tabs, sim1_dist_toggle, sim1_dist_tabs), sizing_mode='stretch_both'), title="Simulation 1")

#
# SIMULATION 2 CODE GOES HERE
#

sim2_tab = Panel(child=layout(row(), sizing_mode='stretch_both'), title="Simulation 2")

sim_tabs = Tabs(tabs=[sim1_tab, sim2_tab])

curdoc().add_root(row(column(row(tp_input, t_sim_input, sizing_mode='stretch_width'), sim_tabs, sizing_mode='stretch_width'), column(xy_pos_plot, row(column(x_pos_plot, x_spd_plot, x_ang_plot), column(y_pos_plot, y_spd_plot, y_ang_plot), sizing_mode='stretch_both'), sizing_mode='stretch_both'), sizing_mode='stretch_both'))
curdoc().title = "Self-balancing table simulation mockup"
