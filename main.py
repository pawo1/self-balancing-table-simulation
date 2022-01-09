import numpy as np
import controller
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, RadioButtonGroup, Toggle, Select
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure
from functools import partial

# TODO: delegate controller to backend folder
# TODO: add Favicon, and title poster on main page

""" --- resources for dynamic access to document elements --- """
lines = ['xy', 'x_pos', 'y_pos', 'x_vel', 'y_vel', 'x_ang', 'y_ang']
conversion = ['set_asked_value', 'set_pos_init', 'set_speed_init']
accelerations = {"Sun (273.95)": 273.95, "Mercury (3.7)": 3.7, "Venus (8.9)": 8.9, "Earth (9.81)": 9.81,
                 "Moon (1.62)": 1.62, "Mars (3.7)": 3.7,
                 "Jupiter (23.1)": 23.1, "Saturn (9.0)": 9.0, "Uranus (8.7)": 8.7,
                 "Neptune (11.0)": 11.0}

""" --- initial simulation --- """
# TODO: initial simulation values should be the same values displaying by the widgets
Sim1 = controller.Controller()
Sim1.run()
Sim2 = controller.Controller()
Sim2.run()
x = np.linspace(0, int(60), int(int(60) / 0.01))

""" --- data sources --- """
sim1_source_xy_pos = ColumnDataSource(data=dict(x=[element * 100 for element in Sim1.table.x.pos],
                                                y=[element * 100 for element in Sim1.table.y.pos]))
sim1_source_x_pos = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim1.table.x.pos]))
sim1_source_y_pos = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim1.table.y.pos]))
sim1_source_x_vel = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim1.table.x.speed]))
sim1_source_y_vel = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim1.table.y.speed]))
sim1_source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.angle))
sim1_source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.angle))

sim2_source_xy_pos = ColumnDataSource(data=dict(x=[element * 100 for element in Sim2.table.x.pos],
                                                y=[element * 100 for element in Sim2.table.y.pos]))
sim2_source_x_pos = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim2.table.x.pos]))
sim2_source_y_pos = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim2.table.y.pos]))
sim2_source_x_vel = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim2.table.x.speed]))
sim2_source_y_vel = ColumnDataSource(data=dict(x=x, y=[element * 100 for element in Sim2.table.y.speed]))
sim2_source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim2.table.x.angle))
sim2_source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim2.table.y.angle))

""" --- callbacks --- """


def tp_update(attr, old, new):
    """ simulation sampling callback """
    callback_global(attr, old, new, name='set_tp')


def t_sim_update(attr, old, new):
    """ simulation time callback """
    callback_global(attr, old, int(new), name='set_simulation_time')


def sim_update(attr, old, new, simulation):
    """ simulation toggle callback """
    for name in lines:
        line = curdoc().get_model_by_name(name + '_' + simulation)
        line.visible = new
    update_plots()


def voltage_update(attr, old, new, simulation):
    """ servo voltage callback """

# we don't use standard callback for min and max values to update plots only once
    if simulation == "Simulation 1":
        Sim1.set_property('set_voltage_min', new[0])
        Sim1.set_property('set_voltage_max', new[1])
        Sim1.run()
    elif simulation == "Simulation 2":
        Sim2.set_property('set_voltage_min', new[0])
        Sim2.set_property('set_voltage_max', new[1])
        Sim2.run()
    update_plots()


def callback_g_acc(attr, old, new, simulation):
    callback(attr, accelerations[old], accelerations[new], 'set_acceleration', simulation)


def callback_global(attr, old, new, name):
    """ callback updating global parameters for both simulations """
    callback(attr, old, new, name, "Simulation 1")
    callback(attr, old, new, name, "Simulation 2")


def callback_axis(attr, old, new, name, axis, simulation):
    """ axis callback for specific simulation passed as argument """

    if name in conversion:
        new = float(new/100) # conversion from [m] to [cm]

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
    x = np.linspace(0, int(t_sim_input.value), int(int(t_sim_input.value) / tp_input.value))

    """ --- data sources --- """
    if sim1_toggle.active is True:
        sim1_source_xy_pos.data = dict(x=[element * 100 for element in Sim1.table.x.pos],
                                       y=[element * 100 for element in Sim1.table.y.pos])
        sim1_source_x_pos.data = dict(x=x, y=[element * 100 for element in Sim1.table.x.pos])
        sim1_source_y_pos.data = dict(x=x, y=[element * 100 for element in Sim1.table.y.pos])
        sim1_source_x_vel.data = dict(x=x, y=[element * 100 for element in Sim1.table.x.speed])
        sim1_source_y_vel.data = dict(x=x, y=[element * 100 for element in Sim1.table.y.speed])
        sim1_source_x_ang.data = dict(x=x, y=Sim1.table.x.angle)
        sim1_source_y_ang.data = dict(x=x, y=Sim1.table.y.angle)

    if sim2_toggle.active is True:
        sim2_source_xy_pos.data = dict(x=[element * 100 for element in Sim2.table.x.pos],
                                       y=[element * 100 for element in Sim2.table.y.pos])
        sim2_source_x_pos.data = dict(x=x, y=[element * 100 for element in Sim2.table.x.pos])
        sim2_source_y_pos.data = dict(x=x, y=[element * 100 for element in Sim2.table.y.pos])
        sim2_source_x_vel.data = dict(x=x, y=[element * 100 for element in Sim2.table.x.speed])
        sim2_source_y_vel.data = dict(x=x, y=[element * 100 for element in Sim2.table.y.speed])
        sim2_source_x_ang.data = dict(x=x, y=Sim2.table.x.angle)
        sim2_source_y_ang.data = dict(x=x, y=Sim2.table.y.angle)


""" --- widgets --- """
# TODO: widgets range should be connected to each other and update on change of different input
#  (i.e. max sim_dist_time_input value on t_sim_input)
tp_input = Slider(title="Sampling [s]", value=0.010, start=0.005, end=1.000, step=0.005, format='0.000', id='tp_input')
t_sim_input = TextInput(title="Simulation time [s]", value=str(60), id='tp_sim_input')
sim1_toggle = Toggle(label="Toggle simulation 1", active=True)
sim2_toggle = Toggle(label="Toggle simulation 2")

tp_input.on_change('value_throttled', partial(callback_global, name='set_tp'))
t_sim_input.on_change('value', t_sim_update)
sim1_toggle.on_change('active', partial(sim_update, simulation='simulation_1'))
sim2_toggle.on_change('active', partial(sim_update, simulation='simulation_2'))

sim_tabs = []
for tab in ["Simulation 1", "Simulation 2"]:
    sim_dist_toggle = Toggle(label="Toggle noise", button_type='default')
    sim_dist_toggle.on_change('active', partial(callback, name='set_noise_active', simulation=tab))
    dists = []
    tabl = []
    for dimension in ['x', 'y']:
        """ disturbances widgets """
        sim_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=0)
        sim_dist_time_input = Slider(title="Disturbance duration", value=360, start=0, end=14400, step=1)
        sim_dist_lvl_input = Slider(title="Level", value=-1, start=-15, end=15, step=1)
        sim_dist_freq_input = Slider(title="Frequency", value=0.100, start=0.001, end=10, step=0.005, format='0.000')

        dists.append(Panel(child=layout(
            column(sim_dist_type_input, sim_dist_time_input, sim_dist_lvl_input, sim_dist_freq_input,
                   sizing_mode='stretch_width'), sizing_mode='stretch_both'), title=dimension.upper() + " disturbance"))

        sim_dist_type_input.on_change('active', partial(callback_axis, name='set_noise_type', axis=dimension,
                                                        simulation=tab))
        sim_dist_time_input.on_change('value_throttled', partial(callback_axis, name='set_noise_period', axis=dimension,
                                                                 simulation=tab))
        sim_dist_lvl_input.on_change('value_throttled', partial(callback_axis, name='set_noise_level', axis=dimension,
                                                                simulation=tab))
        sim_dist_freq_input.on_change('value_throttled', partial(callback_axis, name='set_noise_frequency',
                                                                 axis=dimension, simulation=tab))
        """ table widgets """
        g_acc_input = Select(title="Gravitational acceleration [m/s^2]", value="Earth (9.81)",
                             options=["Sun (273.95)", "Mercury (3.7)", "Venus (8.9)",
                                      "Earth (9.81)", "Moon (1.62)", "Mars (3.7)",
                                      "Jupiter (23.1)", "Saturn (9.0)", "Uranus (8.7)",
                                      "Neptune (11.0)"])
        sim_starting_pos_input = Slider(title=dimension.upper() + " position [cm]", value=25.0, start=-100, end=100,
                                        step=0.5,
                                        format='0.0')
        sim_starting_vel_input = Slider(title=dimension.upper() + " velocity [m/s]", value=-1, start=-30, end=30, step=0.5,
                                        format='0.0')
        sim_starting_ang_input = Slider(title=dimension.upper() + " angle [degree]", value=2.0, start=-90, end=90, step=0.5,
                                        format='0.0')
        sim_desired_pos_input = Slider(title="Desired " + dimension.upper() + " position [cm]", value=0, start=-100, end=100,
                                       step=0.5, format='0.0')

        tabl.append(column(sim_starting_pos_input, sim_starting_vel_input, sim_starting_ang_input,
                           sim_desired_pos_input, sizing_mode='stretch_width'))

        g_acc_input.on_change('value', partial(callback_g_acc, simulation=tab))

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

    sim_pid_type_input.on_change('active', partial(callback, name='set_pid_type', simulation=tab))
    sim_kp_input.on_change('value_throttled', partial(callback, name='set_kp', simulation=tab))
    sim_ti_input.on_change('value_throttled', partial(callback, name='set_ti', simulation=tab))
    sim_td_input.on_change('value_throttled', partial(callback, name='set_td', simulation=tab))
    sim_servo_min_range_input.on_change('value_throttled', partial(callback, name='set_angle_min', simulation=tab))
    sim_servo_max_range_input.on_change('value_throttled', partial(callback, name='set_angle_max', simulation=tab))
    sim_servo_voltage_input.on_change('value_throttled', partial(voltage_update, simulation=tab))

    """ --- tabs --- """
    table_tab = Panel(child=layout(column(g_acc_input, row(tabl)), sizing_mode='stretch_both'), title="Table")

    pid_tab = Panel(child=layout(column(sim_pid_type_input, sim_kp_input, sim_ti_input, sim_td_input,
                                        sizing_mode='stretch_width'), sizing_mode='stretch_both'), title="PID")
    servo_tab = Panel(child=layout(column(row(sim_servo_min_range_input, sim_servo_max_range_input,
                                              sizing_mode='stretch_width'), sim_servo_voltage_input,
                                          sizing_mode='stretch_width'), sizing_mode='stretch_width'), title="Servo")
    noise_tab = Panel(child=layout(column(sim_dist_toggle, Tabs(tabs=dists), sizing_mode='stretch_width'),
                                   sizing_mode='stretch_width'), title="Noise")

    sim_tab = Panel(child=layout(Tabs(tabs=[table_tab, pid_tab, servo_tab, noise_tab]), sizing_mode='stretch_both'),
                    title=tab)

    sim_tabs.append(sim_tab)
tabs = Tabs(tabs=sim_tabs)

""" --- plots --- """
""" XY position """
xy_pos_plot = figure(title="Position on Table (x, y)[cm x cm]", tools="pan,reset,save,wheel_zoom", x_range=[-100, 100],
                     y_range=[-100, 100])
xy_pos_plot.sizing_mode = 'stretch_both'
xy_pos_plot.line('x', 'y', source=sim1_source_xy_pos, name='xy_simulation_1')
xy_pos_plot.line('x', 'y', source=sim2_source_xy_pos, name='xy_simulation_2', color="orange")

""" position """
x_pos_plot = figure(title="pos_x(t)", tools="pan,reset,save,wheel_zoom")
x_pos_plot.sizing_mode = 'stretch_both'
x_pos_plot.line('x', 'y', source=sim1_source_x_pos, line_width=3, line_alpha=0.6, name='x_pos_simulation_1')
x_pos_plot.line('x', 'y', source=sim2_source_x_pos, line_width=3, line_alpha=0.6, name='x_pos_simulation_2',
                color="orange")

y_pos_plot = figure(title="pos_y(t)", tools="pan,reset,save,wheel_zoom")
y_pos_plot.sizing_mode = 'stretch_both'
y_pos_plot.line('x', 'y', source=sim1_source_y_pos, line_width=3, line_alpha=0.6, name='y_pos_simulation_1')
y_pos_plot.line('x', 'y', source=sim2_source_y_pos, line_width=3, line_alpha=0.6, name='y_pos_simulation_2',
                color="orange")

""" velocity """
x_vel_plot = figure(title="speed_x(t)", tools="pan,reset,save,wheel_zoom")
x_vel_plot.sizing_mode = 'stretch_both'
x_vel_plot.line('x', 'y', source=sim1_source_x_vel, line_width=3, line_alpha=0.6, name='x_vel_simulation_1')
x_vel_plot.line('x', 'y', source=sim2_source_x_vel, line_width=3, line_alpha=0.6, name='x_vel_simulation_2',
                color="orange")

y_vel_plot = figure(title="speed_y(t)", tools="pan,reset,save,wheel_zoom")
y_vel_plot.sizing_mode = 'stretch_both'
y_vel_plot.line('x', 'y', source=sim1_source_y_vel, line_width=3, line_alpha=0.6, name='y_vel_simulation_1')
y_vel_plot.line('x', 'y', source=sim2_source_y_vel, line_width=3, line_alpha=0.6, name='y_vel_simulation_2',
                color="orange")

""" angle """
x_ang_plot = figure(title="angle_x(t)", tools="pan,reset,save,wheel_zoom")
x_ang_plot.sizing_mode = 'stretch_both'
x_ang_plot.line('x', 'y', source=sim1_source_x_ang, line_width=3, line_alpha=0.6, name='x_ang_simulation_1')
x_ang_plot.line('x', 'y', source=sim2_source_x_ang, line_width=3, line_alpha=0.6, name='x_ang_simulation_2',
                color="orange")

y_ang_plot = figure(title="angle_y(t)", tools="pan,reset,save,wheel_zoom")
y_ang_plot.sizing_mode = 'stretch_both'
y_ang_plot.line('x', 'y', source=sim1_source_y_ang, line_width=3, line_alpha=0.6, name='y_ang_simulation_1')
y_ang_plot.line('x', 'y', source=sim2_source_y_ang, line_width=3, line_alpha=0.6, name='y_ang_simulation_2',
                color="orange")

curdoc().add_root(
    row(column(
        row(tp_input, t_sim_input, sizing_mode='stretch_width'),
        row(sim1_toggle, sim2_toggle, sizing_mode='stretch_width'), tabs, sizing_mode='stretch_width'),
        column(xy_pos_plot, row(column(x_pos_plot, x_vel_plot, x_ang_plot),
                                column(y_pos_plot, y_vel_plot, y_ang_plot), sizing_mode='stretch_both'),
               sizing_mode='stretch_both'),
        sizing_mode='stretch_both'))

curdoc().title = "Self-balancing table simulation"
update_plots()
