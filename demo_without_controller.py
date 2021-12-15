import table
import servo
import regulator
import sensor

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')


# czas symulacji - parametr wejściowy [s]
t_sim = 10  #float(input())
t_p = 0.01

k_p = 0.25
t_i = 0.015
t_d = 0.05

pos_x = 7.0
pos_y = 7.000


t = table.Table(pos_x=pos_x, pos_y=pos_y, speed_x=0, speed_y=0, angle_x=0, angle_y=0)
servo = servo.Servo(alpha_min=-30.0, alpha_max=30.0, voltage_min=-10.0, voltage_max=10.0)
x_pid = regulator.Regulator(u_min=-10.0, u_max=10.0, kp=k_p, tp=t_p, ti=t_i, td=t_d, pid_type=0)
y_pid = regulator.Regulator(u_min=-10.0, u_max=10.0, kp=k_p, tp=t_p, ti=t_i, td=t_d, pid_type=0)
sensor_x = sensor.Sensor(0)
sensor_y = sensor.Sensor(0)

x_pid.add_error(sensor_x.error(t.get_pos_x()))
y_pid.add_error(sensor_y.error(t.get_pos_y()))

for i in range(1, int(t_sim / t_p)):
    # read error from sensor and add it to regulator memory
    x_pid.add_error(sensor_x.error(t.get_pos_x()))
    y_pid.add_error(sensor_y.error(t.get_pos_y()))
    # calculate signal Voltage for servo
    u_x = x_pid.run_pid()
    u_y = y_pid.run_pid()
    # rotate servo and simulate next step on table
    t.simulate(servo.rotate(u_x), servo.rotate(u_y))


fig = plt.figure('Position X')
ax = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
ax.plot(x, t.get_pos_x_list())
#ax.plot(x, t.get_list_x_angle())

fig = plt.figure('Angle is X Dimension')
cx = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
#cx.plot(x, t.get_list_y())
cx.plot(x, t.get_angle_x_list())

fig2 = plt.figure('Object movement')
bx = plt.axes()
bx.plot(t.get_pos_x_list(), t.get_pos_y_list())
plt.show()

