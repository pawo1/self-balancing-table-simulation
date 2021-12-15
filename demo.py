import controller

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')


# czas symulacji - parametr wejściowy [s]
t_sim = 10  #float(input())
t_p = 0.01

k_p = 0.025
t_i = 0.5
t_d = 0.25

pos_x = 0.003
pos_y = 0.000


Sim1 = controller.Controller(tp=t_p, t_sim=t_sim, kp=k_p, ti=t_i, td=t_d, pos_x=pos_x, pos_y=pos_y)

Sim1.run()

print(Sim1._x_pid.error)

fig = plt.figure('Position X')
ax = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
ax.plot(x, Sim1._table.get_pos_x_list())
#ax.plot(x, t.get_list_x_angle())

fig = plt.figure('Angle is X Dimension')
cx = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
#cx.plot(x, t.get_list_y())
cx.plot(x, Sim1._table.get_angle_x_list())

fig2 = plt.figure('Object movement')
bx = plt.axes()
bx.plot(Sim1._table.get_pos_x_list(), Sim1._table.get_pos_y_list())
plt.show()

