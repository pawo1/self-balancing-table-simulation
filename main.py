from functools import partial

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, RadioButtonGroup, Toggle, Select
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.models.widgets import Tabs, Panel, Div
from bokeh.plotting import figure

from backend import controller
from default_values import values, SI_base

# TODO: add Favicon, and title poster on main page
# TODO: fix widgets formats

Sim1 = controller.Controller()
Sim2 = controller.Controller()

""" --- resources for dynamic access to document elements --- """
simulation_names = ['Simulation 1', 'Simulation 2']
lines = ['xy', 'x_pos', 'y_pos', 'x_vel', 'y_vel', 'x_ang', 'y_ang']
conversion = ['set_asked_value', 'set_pos_init', 'set_speed_init']
accelerations = {"Sun (273.95)": 273.95, "Mercury (3.7)": 3.7, "Venus (8.9)": 8.9, "Earth (9.81)": 9.81,
                 "Moon (1.62)": 1.62, "Mars (3.7)": 3.7,
                 "Jupiter (23.1)": 23.1, "Saturn (9.0)": 9.0, "Uranus (8.7)": 8.7,
                 "Neptune (11.0)": 11.0}
simulation_dict = {"Simulation 1": Sim1, "Simulation 2": Sim2}

""" --- initial simulation --- """
for simulation_name, sim_prop in values.items():
    for key, value in sim_prop.items():
        if simulation_name == "Global":
            for _, sim in simulation_dict.items():
                sim.set_property(key, value)
        elif type(value) is dict:
            for axis_prop, axis_value in value.items():
                simulation_dict[simulation_name].set_property_axis(axis_prop, key, axis_value)
        elif key == "set_acceleration":
            simulation_dict[simulation_name].set_property(key, accelerations[value])
        else:
            simulation_dict[simulation_name].set_property(key, value)

Sim1.run()
Sim2.run()

# lin-space for plot lines
x = np.linspace(0, int(values["Global"]["set_simulation_time"]),
                int(int(values["Global"]["set_simulation_time"]) / values["Global"]["set_tp"]))

""" --- data sources --- """
sim1_source_xy_pos = ColumnDataSource(data=dict(x=[element / SI_base for element in Sim1.table.x.pos],
                                                y=[element / SI_base for element in Sim1.table.y.pos]))
sim1_source_x_pos = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim1.table.x.pos]))
sim1_source_y_pos = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim1.table.y.pos]))
sim1_source_x_vel = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim1.table.x.speed]))
sim1_source_y_vel = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim1.table.y.speed]))
sim1_source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.x.angle))
sim1_source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim1.table.y.angle))

sim2_source_xy_pos = ColumnDataSource(data=dict(x=[element / SI_base for element in Sim2.table.x.pos],
                                                y=[element / SI_base for element in Sim2.table.y.pos]))
sim2_source_x_pos = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim2.table.x.pos]))
sim2_source_y_pos = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim2.table.y.pos]))
sim2_source_x_vel = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim2.table.x.speed]))
sim2_source_y_vel = ColumnDataSource(data=dict(x=x, y=[element / SI_base for element in Sim2.table.y.speed]))
sim2_source_x_ang = ColumnDataSource(data=dict(x=x, y=Sim2.table.x.angle))
sim2_source_y_ang = ColumnDataSource(data=dict(x=x, y=Sim2.table.y.angle))

""" --- callbacks --- """


def tp_update(attr, old, new):
    """ simulation sampling callback """
    for _tab in simulation_names:
        for dim_call in ['x', 'y']:
            model = curdoc().get_model_by_name(_tab + '_noise_freq_' + dim_call)
            model.update(end=1 / new)
            model.update(step=values["Global"]["set_tp"])
            if model.value > 1 / new:
                model.update(value=1 / new)
                simulation_dict[_tab].set_property_axis('set_noise_frequency', dim_call, 1 / new)
            model = curdoc().get_model_by_name(_tab + '_noise_time_' + dim_call)
            model.update(start=new)
            if model.value < new:
                model.update(value=new)
                simulation_dict[_tab].set_property_axis('set_noise_period', dim_call, new)

    Sim1.set_property('set_tp', new)
    Sim2.set_property('set_tp', new)
    Sim1.run()
    Sim2.run()
    update_plots()


def t_sim_update(attr, old, new):
    """ simulation time callback """

    for _tab in simulation_names:
        for dim_call in ['x', 'y']:
            model = curdoc().get_model_by_name(_tab + '_noise_freq_' + dim_call)
            model.update(start=float(1 / float(new)))
            if model.value > float(1 / float(new)):
                model.update(value=float(1 / float(new)))
                simulation_dict[_tab].set_property_axis('set_noise_frequency', dim_call, float(1 / float(new)))
            model = curdoc().get_model_by_name(_tab + '_noise_time_' + dim_call)
            model.update(end=int(new))
            if model.value < int(new):
                model.update(value=int(new))
                simulation_dict[_tab].set_property_axis('set_noise_period', dim_call, int(new))

    Sim1.set_property('set_simulation_time', int(new))
    Sim2.set_property('set_simulation_time', int(new))
    Sim1.run()
    Sim2.run()
    update_plots()


def change_angle_min(attr, old, new, simulation):
    for dim_call in ['x', 'y']:
        model = curdoc().get_model_by_name(simulation + '_dist_lvl_' + dim_call)
        model.update(start=new)
        if model.value < new:
            model.trigger('value', model.value, new)


def change_angle_max(attr, old, new, simulation):
    for dim_call in ['x', 'y']:
        model = curdoc().get_model_by_name(simulation + '_dist_lvl_' + dim_call)
        model.update(end=new)
        if model.value > new:
            model.trigger('value', model.value, new)


def sim_update(attr, old, new, simulation):
    """ simulation toggle callback """

    for name in lines:
        line = curdoc().get_model_by_name(name + '_' + simulation)
        line.visible = new

    update_range()
    update_plots()


def voltage_update(attr, old, new, simulation):
    """ servo voltage callback """

    # we don't use standard callback for min and max values to update plots only once
    simulation_dict[simulation].set_property('set_voltage_min', new[0])
    simulation_dict[simulation].set_property('set_voltage_max', new[1])
    simulation_dict[simulation].run()


def callback_g_acc(attr, old, new, simulation):
    callback(attr, accelerations[old], accelerations[new], 'set_acceleration', simulation)


def callback_global(attr, old, new, name):
    """ callback updating global parameters for both simulations """
    for sim_name_call in simulation_names:
        callback(attr, old, new, name, sim_name_call)


def callback_axis(attr, old, new, name, axis, simulation):
    """ axis callback for specific simulation passed as argument """

    if name in conversion:
        new = float(new * SI_base)  # conversion from [m] to [cm]

    simulation_dict[simulation].set_property_axis(name, axis, new)
    simulation_dict[simulation].run()

    update_plots()


def callback(attr, old, new, name, simulation):
    """ main callback function """

    simulation_dict[simulation].set_property(name, new)
    simulation_dict[simulation].run()

    update_plots()


def update_plots():
    """ callback updating plots """
    # TODO: real time plot stream

    global x
    x = np.linspace(0, int(t_sim_input.value), int(int(t_sim_input.value) / tp_input.value))

    """ --- data sources --- """
    #    if sim1_toggle.active is True:
    sim1_source_xy_pos.data = dict(x=[element / SI_base for element in Sim1.table.x.pos],
                                   y=[element / SI_base for element in Sim1.table.y.pos])
    sim1_source_x_pos.data = dict(x=x, y=[element / SI_base for element in Sim1.table.x.pos])
    sim1_source_y_pos.data = dict(x=x, y=[element / SI_base for element in Sim1.table.y.pos])
    sim1_source_x_vel.data = dict(x=x, y=[element / SI_base for element in Sim1.table.x.speed])
    sim1_source_y_vel.data = dict(x=x, y=[element / SI_base for element in Sim1.table.y.speed])
    sim1_source_x_ang.data = dict(x=x, y=Sim1.table.x.angle)
    sim1_source_y_ang.data = dict(x=x, y=Sim1.table.y.angle)

    #    if sim2_toggle.active is True:
    sim2_source_xy_pos.data = dict(x=[element / SI_base for element in Sim2.table.x.pos],
                                   y=[element / SI_base for element in Sim2.table.y.pos])
    sim2_source_x_pos.data = dict(x=x, y=[element / SI_base for element in Sim2.table.x.pos])
    sim2_source_y_pos.data = dict(x=x, y=[element / SI_base for element in Sim2.table.y.pos])
    sim2_source_x_vel.data = dict(x=x, y=[element / SI_base for element in Sim2.table.x.speed])
    sim2_source_y_vel.data = dict(x=x, y=[element / SI_base for element in Sim2.table.y.speed])
    sim2_source_x_ang.data = dict(x=x, y=Sim2.table.x.angle)
    sim2_source_y_ang.data = dict(x=x, y=Sim2.table.y.angle)


def update_range():
    plots = {"x_pos": x_pos_plot, "y_pos": y_pos_plot, "x_vel": x_vel_plot, "y_vel": y_vel_plot, "x_ang": x_ang_plot,
             "y_ang": y_ang_plot}

    for name in lines:
        if name == "xy":  # main table plot has fixed -100;100 ranges
            continue

        renderers = []

        for sim_name_call in simulation_names:
            if curdoc().get_model_by_name("toggle_" + sim_name_call.lower().replace(' ', '_')).active is True:
                renderers.append(curdoc().get_model_by_name(name + "_" + sim_name_call.lower().replace(' ', '_')))

        plots[name].y_range.update(renderers=renderers)


""" --- widgets --- """
tp_input = Slider(title="Sampling [s]", value=values["Global"]["set_tp"], start=0.005, end=1.000, step=0.005,
                  format='0.000', id='tp_input')
t_sim_input = TextInput(title="Simulation time [s]", value=str(values["Global"]["set_simulation_time"]),
                        id='tp_sim_input')


toggle = []
for sim_name in simulation_names:
    sim_toggle = Toggle(label="Toggle " + sim_name.lower(), active=values[sim_name]["toggle"],
                        name="toggle_" + sim_name.lower().replace(' ', '_'))
    sim_toggle.on_change('active', partial(sim_update, simulation=sim_name.lower().replace(' ', '_')))
    toggle.append(sim_toggle)

tp_input.on_change('value_throttled', tp_update)
t_sim_input.on_change('value', t_sim_update)

sim_tabs = []
for tab in ["Simulation 1", "Simulation 2"]:
    sim_dist_toggle = Toggle(label="Toggle noise", button_type='default', active=values[tab]["set_noise_active"])
    sim_dist_toggle.on_change('active', partial(callback, name='set_noise_active', simulation=tab))
    dists = []
    tabl = []
    for dimension in ['x', 'y']:
        """ disturbances widgets """
        sim_dist_type_input = RadioButtonGroup(labels=["Pulse", "Sin"], active=values[tab][dimension]["set_noise_type"])

        sim_dist_time_input = Slider(title="Disturbance duration", value=values[tab][dimension]["set_noise_period"],
                                     start=values["Global"]["set_tp"], end=int(values["Global"]["set_simulation_time"]),
                                     step=values["Global"]["set_tp"], name=tab + '_noise_time_' + dimension)

        sim_dist_lvl_input = Slider(title="Level", value=values[tab][dimension]["set_noise_level"],
                                    start=values[tab]["set_angle_min"],
                                    end=values[tab]["set_angle_max"],
                                    step=1, name=tab + '_dist_lvl_' + dimension)

        sim_dist_freq_input = Slider(title="Frequency", value=values[tab][dimension]["set_noise_frequency"],
                                     start=float(1 / float(values["Global"]["set_simulation_time"])),
                                     end=1 / values["Global"]["set_tp"], step=values["Global"]["set_tp"],
                                     format='0.000', name=tab + '_noise_freq_' + dimension)

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
        g_acc_input = Select(title="Gravitational acceleration [m/s^2]", value=values[tab]["set_acceleration"],
                             options=["Sun (273.95)", "Mercury (3.7)", "Venus (8.9)",
                                      "Earth (9.81)", "Moon (1.62)", "Mars (3.7)",
                                      "Jupiter (23.1)", "Saturn (9.0)", "Uranus (8.7)",
                                      "Neptune (11.0)"])
        sim_starting_pos_input = Slider(title=dimension.upper() + " position [cm]",
                                        value=values[tab][dimension]["set_pos_init"] / SI_base, start=-100, end=100,
                                        step=0.5, format='0.0')
        sim_starting_vel_input = Slider(title=dimension.upper() + " velocity [m/s]",
                                        value=values[tab][dimension]["set_speed_init"] / SI_base, start=-30, end=30,
                                        step=0.5, format='0.0')
        #        present PID algorithm doesn't care about starting angle, setting this is pointless
        #        sim_starting_ang_input = Slider(title=dimension.upper() + " angle [degree]", value=2.0, start=-90,
        #                                        end=90, step=0.5, format='0.0')
        sim_desired_pos_input = Slider(title="Desired " + dimension.upper() + " position [cm]",
                                       value=values[tab][dimension]["set_asked_value"] / SI_base, start=-100,
                                       end=100, step=0.5, format='0.0')

        tabl.append(column(sim_starting_pos_input, sim_starting_vel_input, sim_desired_pos_input,
                           sizing_mode='stretch_width'))

        g_acc_input.on_change('value', partial(callback_g_acc, simulation=tab))

        sim_starting_pos_input.on_change('value_throttled', partial(callback_axis, name='set_pos_init',
                                                                    axis=dimension, simulation=tab))
        sim_starting_vel_input.on_change('value_throttled', partial(callback_axis, name='set_speed_init',
                                                                    axis=dimension, simulation=tab))
        #        sim_starting_ang_input.on_change('value_throttled', partial(callback_axis, name='set_angle_init',
        #                                                                    axis=dimension, simulation=tab))
        sim_desired_pos_input.on_change('value_throttled', partial(callback_axis, name='set_asked_value',
                                                                   axis=dimension, simulation=tab))

    """ PID widgets """
    sim_pid_type_input = RadioButtonGroup(labels=["Positional", "Incremental"], active=values[tab]["set_pid_type"])
    sim_kp_input = Slider(title="Amplification", value=values[tab]["set_kp"], start=0.005, end=1.00, step=0.005,
                          format='0.000')
    sim_ti_input = Slider(title="Integral action time factor", value=values[tab]["set_ti"], start=0.005, end=1.00,
                          step=0.005, format='0.000')
    sim_td_input = Slider(title="Derivative action time factor", value=values[tab]["set_td"], start=0.005, end=1.00,
                          step=0.005, format='0.000')
    sim_servo_min_range_input = Slider(title="Servo minimal range", value=values[tab]["set_angle_min"], start=-90,
                                       end=-1, step=1)
    sim_servo_max_range_input = Slider(title="Servo maximal range", value=values[tab]["set_angle_max"], start=1, end=90,
                                       step=1)

    sim_servo_voltage_input = RangeSlider(title="Servo voltage", value=(values[tab]["set_voltage_min"],
                                                                        values[tab]["set_voltage_max"]),
                                          start=-50, end=50, step=1)

    sim_pid_type_input.on_change('active', partial(callback, name='set_pid_type', simulation=tab))
    sim_kp_input.on_change('value_throttled', partial(callback, name='set_kp', simulation=tab))
    sim_ti_input.on_change('value_throttled', partial(callback, name='set_ti', simulation=tab))
    sim_td_input.on_change('value_throttled', partial(callback, name='set_td', simulation=tab))
    sim_servo_min_range_input.on_change('value_throttled', partial(callback, name='set_angle_min', simulation=tab),
                                        partial(change_angle_min, simulation=tab))
    sim_servo_max_range_input.on_change('value_throttled', partial(callback, name='set_angle_max', simulation=tab),
                                        partial(change_angle_max, simulation=tab))
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
xy_pos_plot.line('x', 'y', source=sim1_source_xy_pos, legend_label='Simulation 1', name='xy_simulation_1')
xy_pos_plot.line('x', 'y', source=sim2_source_xy_pos, legend_label='Simulation 2', name='xy_simulation_2',
                 color="orange")
xy_pos_plot.legend.location = 'top_right'

""" position """
x_pos_plot = figure(title="Position X dimension [cm]", tools="pan,reset,save,wheel_zoom")
x_pos_plot.sizing_mode = 'stretch_both'
x_pos_plot.line('x', 'y', source=sim1_source_x_pos, line_width=3, line_alpha=0.6, name='x_pos_simulation_1')
x_pos_plot.line('x', 'y', source=sim2_source_x_pos, line_width=3, line_alpha=0.6, name='x_pos_simulation_2',
                color="orange")

y_pos_plot = figure(title="Position Y dimension [cm]", tools="pan,reset,save,wheel_zoom")
y_pos_plot.sizing_mode = 'stretch_both'
y_pos_plot.line('x', 'y', source=sim1_source_y_pos, line_width=3, line_alpha=0.6, name='y_pos_simulation_1')
y_pos_plot.line('x', 'y', source=sim2_source_y_pos, line_width=3, line_alpha=0.6, name='y_pos_simulation_2',
                color="orange")

""" velocity """
x_vel_plot = figure(title="Speed X dimension [cm/s]", tools="pan,reset,save,wheel_zoom")
x_vel_plot.sizing_mode = 'stretch_both'
x_vel_plot.line('x', 'y', source=sim1_source_x_vel, line_width=3, line_alpha=0.6, name='x_vel_simulation_1')
x_vel_plot.line('x', 'y', source=sim2_source_x_vel, line_width=3, line_alpha=0.6, name='x_vel_simulation_2',
                color="orange")

y_vel_plot = figure(title="Speed Y dimension [cm/s]", tools="pan,reset,save,wheel_zoom")
y_vel_plot.sizing_mode = 'stretch_both'
y_vel_plot.line('x', 'y', source=sim1_source_y_vel, line_width=3, line_alpha=0.6, name='y_vel_simulation_1')
y_vel_plot.line('x', 'y', source=sim2_source_y_vel, line_width=3, line_alpha=0.6, name='y_vel_simulation_2',
                color="orange")

""" angle """
x_ang_plot = figure(title="Angle X dimension [degree]", tools="pan,reset,save,wheel_zoom")
x_ang_plot.sizing_mode = 'stretch_both'
x_ang_plot.line('x', 'y', source=sim1_source_x_ang, line_width=3, line_alpha=0.6, name='x_ang_simulation_1')
x_ang_plot.line('x', 'y', source=sim2_source_x_ang, line_width=3, line_alpha=0.6, name='x_ang_simulation_2',
                color="orange")

y_ang_plot = figure(title="Angle Y dimension [degree]", tools="pan,reset,save,wheel_zoom")
y_ang_plot.sizing_mode = 'stretch_both'
y_ang_plot.line('x', 'y', source=sim1_source_y_ang, line_width=3, line_alpha=0.6, name='y_ang_simulation_1')
y_ang_plot.line('x', 'y', source=sim2_source_y_ang, line_width=3, line_alpha=0.6, name='y_ang_simulation_2',
                color="orange")

div_banner = Div(text="""<img src="self-balancing-table-simulation/static/SBTable.png" 
alt="SBTable banner" style="position:fixed; left:0; bottom:0">""", width=495, height=106)

curdoc().add_root(
    row(column(
        row(tp_input, t_sim_input, sizing_mode='stretch_width'),
        row(toggle, sizing_mode='stretch_width'), tabs, div_banner, sizing_mode='stretch_width'),
        column(xy_pos_plot, row(column(x_pos_plot, x_vel_plot, x_ang_plot),
                                column(y_pos_plot, y_vel_plot, y_ang_plot), sizing_mode='stretch_both'),
               sizing_mode='stretch_both'),
        sizing_mode='stretch_both'))

curdoc().title = "Self-balancing table simulation"
for dim in ["Simulation 1", "Simulation 2"]:
    sim_update('active', 0, values[dim]["toggle"], simulation=dim.lower().replace(' ', '_'))
update_range()
update_plots()
# TODO: dark theme templates with dynamic change button
# curdoc().theme = 'dark_minimal'
