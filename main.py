import numpy as np

import controller
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, RadioButtonGroup, Toggle
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from functools import partial

t_sim = 60
tp = 0.01

""" initial simulation """
Sim1 = controller.Controller()
Sim1.run()
Sim2 = controller.Controller()
Sim2.run()
x = np.linspace(0, int(60), int(int(60) / 0.01))

""" data sources """
source_xy_pos = ColumnDataSource(data=dict(x=Sim1.table.x.pos, y=Sim1.table.y.pos))
source_x_pos = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_pos = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))
source_x_spd = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_spd = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))
source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))


def tp_update(attr, old, new):
    global tp
    tp = new
    callback_global(attr, old, new, name='set_tp')


def t_sim_update(attr, old, new):
    global t_sim
    t_sim = int(new)
    callback_global(attr, old, int(new), name='set_simulation_time')


def callback_global(attr, old, new, name):
    callback(attr, old, new, name, "Simulation 1")
    callback(attr, old, new, name, "Simulation 2")


def callback_axis(attr, old, new, name, axis, simulation):
    if simulation == "Simulation 1":
        Sim1.set_property_axis(name, axis, new)
        Sim1.run()
    elif simulation == "Simulation 2":
        Sim2.set_property_axis(name, axis, new)
        Sim2.run()
    update_plots()


def callback(attr, old, new, name, simulation):
    if simulation == "Simulation 1":
        Sim1.set_property(name, new)
        Sim1.run()
    elif simulation == "Simulation 2":
        Sim2.set_property(name, new)
        Sim2.run()
    update_plots()


def update_plots():

    global x
    x = np.linspace(0, int(t_sim), int(int(t_sim) / tp))

    print(len(x), len(Sim1.table.x.pos), len(Sim1.table.y.pos), len(Sim1.table.y.pos),
          len(Sim1.table.x.speed), len(Sim1.table.y.speed), len(Sim1.table.x.angle), len(Sim1.table.y.angle))

    """ data sources """
    source_xy_pos.data=dict(x=Sim1.table.x.pos, y=Sim1.table.y.pos)
    source_x_pos.data=dict(x=x, y=Sim1.table.x.pos)
    source_y_pos.data=dict(x=x, y=Sim1.table.y.pos)
    source_x_spd.data=dict(x=x, y=Sim1.table.x.speed)
    source_y_spd.data=dict(x=x, y=Sim1.table.y.speed)
    source_x_ang.data=dict(x=x, y=Sim1.table.x.angle)
    source_y_ang.data=dict(x=x, y=Sim1.table.y.angle)

""" widgets """
tp_input = Slider(title="Sampling", value=0.010, start=0.005, end=1.000, step=0.005, format='0.000')
t_sim_input = TextInput(title="Simulation time", value=str(100))

tp_input.on_change('value_throttled', tp_update)
t_sim_input.on_change('value', t_sim_update)

temp_tabs = []
for tab in ["Simulation 1", "Simulation 2"]:
    # --- Table
    sim_starting_x_pos_input = Slider(title="X position", value=25.0, start=-100, end=100, step=0.5, format='0.0')
    sim_starting_y_pos_input = Slider(title="Y position", value=-75.0, start=-100, end=100, step=0.5, format='0.0')

    sim_starting_x_spd_input = Slider(title="X velocity", value=-1, start=-30, end=30, step=0.5, format='0.0')
    sim_starting_y_spd_input = Slider(title="Y velocity", value=2, start=-30, end=30, step=0.5, format='0.0')

    sim_starting_x_ang_input = Slider(title="X angle", value=2.0, start=-90, end=90, step=0.5, format='0.0')
    sim_starting_y_ang_input = Slider(title="Y angle", value=-1.5, start=-90, end=90, step=0.5, format='0.0')

    sim_desired_x_pos_input = Slider(title="Desired X position", value=0, start=-100, end=100, step=0.5, format='0.0')
    sim_desired_y_pos_input = Slider(title="Desired Y position", value=0, start=-100, end=100, step=0.5, format='0.0')

    # --- PID
    sim_pid_type_input = RadioButtonGroup(labels=["Positional", "Incremental"], active=1)
    sim_kp_input = Slider(title="Amplification", value=0.025, start=0.005, end=1.00, step=0.005, format='0.000')
    sim_ti_input = Slider(title="Integral action time factor", value=0.015, start=0.005, end=1.00, step=0.005,
                          format='0.000')
    sim_td_input = Slider(title="Derivative action time factor", value=0.050, start=0.005, end=1.00, step=0.005,
                          format='0.000')
    sim_servo_min_range_input = Slider(title="Servo minimal range", value=-15, start=-90, end=-1, step=1)
    sim_servo_max_range_input = Slider(title="Servo maximal range", value=15, start=1, end=90, step=1)

    # --- Disturbances
    sim_dist_toggle = Toggle(label="Toggle disturbance", button_type='default')

    sim_x_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)
    sim_y_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)

    sim_x_dist_time_input = Slider(title="Disturbance duration", value=360, start=0, end=14400, step=1)
    sim_y_dist_time_input = Slider(title="Disturbance duration", value=180, start=0, end=14400, step=1)

    sim_x_dist_lvl_input = Slider(title="Level", value=-1, start=-15, end=15, step=1)
    sim_y_dist_lvl_input = Slider(title="Level", value=2, start=-15, end=15, step=1)

    sim_x_dist_freq_input = Slider(title="Frequency", value=0.100, start=0.001, end=10, step=0.005, format='0.000')
    sim_y_dist_freq_input = Slider(title="Frequency", value=0.125, start=0.001, end=10, step=0.005, format='0.000')

    sim_kp_input.on_change('value_throttled', partial(callback, name='set_kp', simulation=tab))
    sim_ti_input.on_change('value_throttled', partial(callback, name='set_ti', simulation=tab))
    sim_td_input.on_change('value_throttled', partial(callback, name='set_td', simulation=tab))
    sim_servo_min_range_input.on_change('value_throttled', partial(callback, name='set_angle_min', simulation=tab))
    sim_servo_max_range_input.on_change('value_throttled', partial(callback, name='set_angle_max', simulation=tab))

    sim_starting_x_pos_input.on_change('value_throttled', partial(callback_axis, name='set_pos_init',
                                                                  axis='x', simulation=tab))
    sim_starting_y_pos_input.on_change('value_throttled', partial(callback_axis, name='set_pos_init',
                                                                  axis='y', simulation=tab))
    sim_starting_x_spd_input.on_change('value_throttled', partial(callback_axis, name='set_speed_init',
                                                                  axis='x', simulation=tab))
    sim_starting_y_spd_input.on_change('value_throttled', partial(callback_axis, name='set_speed_init',
                                                                  axis='y', simulation=tab))
    sim_starting_x_ang_input.on_change('value_throttled', partial(callback_axis, name='set_angle_init',
                                                                  axis='x', simulation=tab))
    sim_starting_y_ang_input.on_change('value_throttled', partial(callback_axis, name='set_angle_init',
                                                                  axis='y', simulation=tab))
    sim_desired_x_pos_input.on_change('value_throttled', partial(callback_axis, name='set_asked_value',
                                                                 axis='x', simulation=tab))
    sim_desired_y_pos_input.on_change('value_throttled', partial(callback_axis, name='set_asked_value',
                                                                 axis='y', simulation=tab))



    """ tabs """
    sim_pid = Panel(child=layout(column(sim_pid_type_input, sim_kp_input, sim_ti_input, sim_td_input,
                                        row(sim_servo_min_range_input, sim_servo_max_range_input,
                                            sizing_mode='stretch_width'), sizing_mode='stretch_width'),
                                 sizing_mode='stretch_both'), title="PID")
    sim_table = Panel(child=layout(
        column(row(sim_starting_x_pos_input, sim_starting_y_pos_input, sizing_mode='stretch_width'),
               sizing_mode='stretch_width'),
        row(sim_starting_x_spd_input, sim_starting_y_spd_input, sizing_mode='stretch_width'),
        row(sim_starting_x_ang_input, sim_starting_y_ang_input, sizing_mode='stretch_width'),
        column(sim_desired_x_pos_input, sim_desired_y_pos_input, sizing_mode='stretch_width'),
        sizing_mode='stretch_both'), title="Table")
    sim_tabs = Tabs(tabs=[sim_table, sim_pid])

    sim_x_dist = Panel(child=layout(
        column(sim_x_dist_type_input, sim_x_dist_time_input, sim_x_dist_lvl_input, sim_x_dist_freq_input,
               sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="X disturbance")
    sim_y_dist = Panel(child=layout(
        column(sim_y_dist_type_input, sim_y_dist_time_input, sim_y_dist_lvl_input, sim_y_dist_freq_input,
               sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="Y disturbance")
    sim_dist_tabs = Tabs(tabs=[sim_x_dist, sim_y_dist])

    sim_tab = Panel(child=layout(column(sim_tabs, sim_dist_toggle, sim_dist_tabs), sizing_mode='stretch_both'),
                    title=tab)

    temp_tabs.append(sim_tab)


sim_tabs = Tabs(tabs=temp_tabs)

# TODO: add multiple plotlines to existing plots



""" plots """
# --- XY position
xy_pos_plot = figure(title="table_position(x,y)", tools="pan,reset,save,wheel_zoom", x_range=[-100, 100],
                     y_range=[-100, 100])
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

curdoc().add_root(
    row(column(row(tp_input, t_sim_input, sizing_mode='stretch_width'), sim_tabs, sizing_mode='stretch_width'),
        column(xy_pos_plot, row(column(x_pos_plot, x_spd_plot, x_ang_plot), column(y_pos_plot, y_spd_plot, y_ang_plot),
                                sizing_mode='stretch_both'), sizing_mode='stretch_both'), sizing_mode='stretch_both'))
curdoc().title = "Self-balancing table simulation mockup"
