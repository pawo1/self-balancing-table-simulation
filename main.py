import numpy as np
import controller
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, RadioButtonGroup, Toggle, Select
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure
from functools import partial

# TODO: do something with those global vars, maybe read values from widgets?
t_sim = 60
tp = 0.01


""" --- initial simulation --- """
# TODO: initial simulation values should be the same values displaying by the widgets
Sim1 = controller.Controller()
Sim1.run()
Sim2 = controller.Controller()
Sim2.run()
x = np.linspace(0, int(t_sim), int(int(t_sim) / tp))


""" --- data sources --- """
source_xy_pos = ColumnDataSource(data=dict(x=Sim1.table.x.pos, y=Sim1.table.y.pos))
source_x_pos = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_pos = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))
source_x_vel = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_vel = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))
source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.pos))
source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.pos))


""" --- callbacks --- """


def tp_update(attr, old, new):
    """ simulation sampling callback """
    global tp
    tp = new
    callback_global(attr, old, new, name='set_tp')


def t_sim_update(attr, old, new):
    """ simulation time callback """
    global t_sim
    t_sim = int(new)
    callback_global(attr, old, int(new), name='set_simulation_time')


def voltage_update(attr, old, new, simulation):
    """ servo voltage callback """
    callback(attr, old, new[0], 'set_voltage_min', simulation)
    callback(attr, old, new[1], 'set_voltage_max', simulation)


def callback_global(attr, old, new, name):
    """ callback updating global parameters for both simulations """
    callback(attr, old, new, name, "Simulation 1")
    callback(attr, old, new, name, "Simulation 2")


def callback_axis(attr, old, new, name, axis, simulation):
    """ axis callback for specific simulation passed as argument """
    if simulation == "Simulation 1":
        Sim1.set_property_axis(name, axis, new)
        Sim1.run()
    elif simulation == "Simulation 2":
        Sim2.set_property_axis(name, axis, new)
        Sim2.run()
    update_plots()


def callback(attr, old, new, name, simulation):
    """ main callback function """
    if simulation == "Simulation 1":
        Sim1.set_property(name, new)
        Sim1.run()
    elif simulation == "Simulation 2":
        Sim2.set_property(name, new)
        Sim2.run()
    update_plots()


def update_plots():
    """ callback updating plots """
    # TODO: real time plot stream
    global x
    x = np.linspace(0, int(t_sim), int(int(t_sim) / tp))

    """ --- data sources --- """
    source_xy_pos.data = dict(x=Sim1.table.x.pos, y=Sim1.table.y.pos)
    source_x_pos.data = dict(x=x, y=Sim1.table.x.pos)
    source_y_pos.data = dict(x=x, y=Sim1.table.y.pos)
    source_x_vel.data = dict(x=x, y=Sim1.table.x.speed)
    source_y_vel.data = dict(x=x, y=Sim1.table.y.speed)
    source_x_ang.data = dict(x=x, y=Sim1.table.x.angle)
    source_y_ang.data = dict(x=x, y=Sim1.table.y.angle)


""" --- widgets --- """
# TODO: widgets range should be connected to each other and update on change of different input
#  (i.e. max sim_dist_time_input value on t_sim_input)
tp_input = Slider(title="Sampling", value=0.010, start=0.005, end=1.000, step=0.005, format='0.000')
t_sim_input = TextInput(title="Simulation time", value=str(100))
sim2_toggle = Toggle(label="Toggle simulation 2", button_type='default')

tp_input.on_change('value_throttled', tp_update)
t_sim_input.on_change('value', t_sim_update)

sim_tabs = []
for tab in ["Simulation 1", "Simulation 2"]:
    # TODO: connect sim2_toggle button
    sim_dist_toggle = Toggle(label="Toggle noise", button_type='default')
    dists = []
    for dimension in ['x', 'y']:
        """ disturbances widgets """
        sim_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)
        sim_dist_time_input = Slider(title="Disturbance duration", value=360, start=0, end=14400, step=1)
        sim_dist_lvl_input = Slider(title="Level", value=-1, start=-15, end=15, step=1)
        sim_dist_freq_input = Slider(title="Frequency", value=0.100, start=0.001, end=10, step=0.005, format='0.000')

        dists.append(Panel(child=layout(
            column(sim_dist_type_input, sim_dist_time_input, sim_dist_lvl_input, sim_dist_freq_input,
                   sizing_mode='stretch_width'), sizing_mode='stretch_both'), title=dimension.upper() + " disturbance"))

        # TODO: connect sim_dist_toggle button
        sim_dist_type_input.on_change('active', partial(callback_axis, name='set_noise_type', axis=dimension,
                                                        simulation=tab))
        sim_dist_time_input.on_change('value_throttled', partial(callback_axis, name='set_noise_period', axis=dimension,
                                                                 simulation=tab))
        sim_dist_lvl_input.on_change('value_throttled', partial(callback_axis, name='set_noise_level', axis=dimension,
                                                                simulation=tab))
        sim_dist_freq_input.on_change('value_throttled', partial(callback_axis, name='set_noise_frequency',
                                                                 axis=dimension, simulation=tab))

    tabl = []
    for dimension in ['x', 'y']:
        """ table widgets """
        g_acc_input = Select(title="Gravitational acceleration", value="Earth", options=["Sun", "Mercury", "Venus",
                                                                                         "Earth", "Moon", "Mars",
                                                                                         "Jupiter", "Saturn", "Uranus",
                                                                                         "Neptune"])
        sim_starting_pos_input = Slider(title=dimension.upper() + " position", value=25.0, start=-100, end=100,
                                        step=0.5,
                                        format='0.0')
        sim_starting_vel_input = Slider(title=dimension.upper() + " velocity", value=-1, start=-30, end=30, step=0.5,
                                        format='0.0')
        sim_starting_ang_input = Slider(title=dimension.upper() + " angle", value=2.0, start=-90, end=90, step=0.5,
                                        format='0.0')
        sim_desired_pos_input = Slider(title="Desired " + dimension.upper() + " position", value=0, start=-100, end=100,
                                       step=0.5, format='0.0')

        tabl.append(column(sim_starting_pos_input, sim_starting_vel_input, sim_starting_ang_input,
                           sim_desired_pos_input, sizing_mode='stretch_width'))

        # TODO: connect g_acc_input select list
        sim_starting_pos_input.on_change('value_throttled', partial(callback_axis, name='set_pos_init',
                                                                    axis=dimension, simulation=tab))
        sim_starting_vel_input.on_change('value_throttled', partial(callback_axis, name='set_speed_init',
                                                                    axis=dimension, simulation=tab))
        sim_starting_ang_input.on_change('value_throttled', partial(callback_axis, name='set_angle_init',
                                                                    axis=dimension, simulation=tab))
        sim_desired_pos_input.on_change('value_throttled', partial(callback_axis, name='set_asked_value',
                                                                   axis=dimension, simulation=tab))

    """ PID widgets """
    sim_pid_type_input = RadioButtonGroup(labels=["Positional", "Incremental"], active=1)
    sim_kp_input = Slider(title="Amplification", value=0.025, start=0.005, end=1.00, step=0.005, format='0.000')
    sim_ti_input = Slider(title="Integral action time factor", value=0.015, start=0.005, end=1.00, step=0.005,
                          format='0.000')
    sim_td_input = Slider(title="Derivative action time factor", value=0.050, start=0.005, end=1.00, step=0.005,
                          format='0.000')
    sim_servo_min_range_input = Slider(title="Servo minimal range", value=-15, start=-90, end=-1, step=1)
    sim_servo_max_range_input = Slider(title="Servo maximal range", value=15, start=1, end=90, step=1)

    sim_servo_voltage_input = RangeSlider(title="Servo voltage", value=(-100, 100), start=-200, end=200, step=1)

    # TODO: connect sim_pid_type_input button
    sim_kp_input.on_change('value_throttled', partial(callback, name='set_kp', simulation=tab))
    sim_ti_input.on_change('value_throttled', partial(callback, name='set_ti', simulation=tab))
    sim_td_input.on_change('value_throttled', partial(callback, name='set_td', simulation=tab))
    sim_servo_min_range_input.on_change('value_throttled', partial(callback, name='set_angle_min', simulation=tab))
    sim_servo_max_range_input.on_change('value_throttled', partial(callback, name='set_angle_max', simulation=tab))
    sim_servo_voltage_input.on_change('value_throttled', partial(voltage_update, simulation=tab))

    """ --- tabs --- """
    table_tab = Panel(child=layout(column( g_acc_input, row(tabl)), sizing_mode='stretch_both'), title="Table")

    pid_tab = Panel(child=layout(column(sim_pid_type_input, sim_kp_input, sim_ti_input, sim_td_input,
                                        sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="PID")
    servo_tab = Panel(child=layout(column(row(sim_servo_min_range_input, sim_servo_max_range_input,
                                              sizing_mode='stretch_width'), sim_servo_voltage_input,
                                          sizing_mode='stretch_width'), sizing_mode='stretch_width'), title="Servo")
    noise_tab = Panel(child=layout(column(sim_dist_toggle, Tabs(tabs=dists), sizing_mode='stretch_width'), sizing_mode='stretch_width'), title="Noise")

    sim_tab = Panel(child=layout(Tabs(tabs=[table_tab, pid_tab, servo_tab, noise_tab]), sizing_mode='stretch_both'),
                    title=tab)

    sim_tabs.append(sim_tab)
tabs = Tabs(tabs=sim_tabs)


""" --- plots --- """
# TODO: add simulation 2 lines to existing plots
""" XY position """
xy_pos_plot = figure(title="table_position(x,y)", tools="pan,reset,save,wheel_zoom", x_range=[-100, 100],
                     y_range=[-100, 100])
xy_pos_plot.sizing_mode = 'stretch_both'
xy_pos_plot.line('x', 'y', source=source_xy_pos)

""" position """
x_pos_plot = figure(title="pos_x(t)", tools="pan,reset,save,wheel_zoom")
x_pos_plot.sizing_mode = 'stretch_both'
x_pos_plot.line('x', 'y', source=source_x_pos, line_width=3, line_alpha=0.6)

y_pos_plot = figure(title="pos_y(t)", tools="pan,reset,save,wheel_zoom")
y_pos_plot.sizing_mode = 'stretch_both'
y_pos_plot.line('x', 'y', source=source_y_pos, line_width=3, line_alpha=0.6)

""" velocity """
x_vel_plot = figure(title="speed_x(t)", tools="pan,reset,save,wheel_zoom")
x_vel_plot.sizing_mode = 'stretch_both'
x_vel_plot.line('x', 'y', source=source_x_vel, line_width=3, line_alpha=0.6)

y_vel_plot = figure(title="speed_y(t)", tools="pan,reset,save,wheel_zoom")
y_vel_plot.sizing_mode = 'stretch_both'
y_vel_plot.line('x', 'y', source=source_y_vel, line_width=3, line_alpha=0.6)

""" angle """
x_ang_plot = figure(title="angle_x(t)", tools="pan,reset,save,wheel_zoom")
x_ang_plot.sizing_mode = 'stretch_both'
x_ang_plot.line('x', 'y', source=source_x_ang, line_width=3, line_alpha=0.6)

y_ang_plot = figure(title="angle_y(t)", tools="pan,reset,save,wheel_zoom")
y_ang_plot.sizing_mode = 'stretch_both'
y_ang_plot.line('x', 'y', source=source_y_ang, line_width=3, line_alpha=0.6)

curdoc().add_root(
    row(column(row(tp_input, t_sim_input, sizing_mode='stretch_width'), sim2_toggle, tabs, sizing_mode='stretch_width'),
        column(xy_pos_plot, row(column(x_pos_plot, x_vel_plot, x_ang_plot), column(y_pos_plot, y_vel_plot, y_ang_plot),
                                sizing_mode='stretch_both'), sizing_mode='stretch_both'), sizing_mode='stretch_both'))
curdoc().title = "Self-balancing table simulation"
