import controller

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')


# czas symulacji - parametr wejściowy [s]
t_sim = 60  #float(input())
t_p = 0.01

k_p = 0.025
t_i = 0.5
t_d = 0.25

pos_x = 0.003
pos_y = 0.007


Sim1 = controller.Controller()

Sim1.set_property_axis('set_pos_init', 'x', 50)
Sim1.set_property_axis('set_pos_init', 'y', 30)
Sim1.set_property_axis('set_noise_period', 'x', 600)
Sim1.set_property_axis('set_noise_frequency', 'x', 0.5)
Sim1.set_property_axis('set_noise_level', 'x', 6)
Sim1.set_property_axis('set_noise_type', 'x', 1)


Sim2 = controller.Controller()

Sim2.set_property_axis('set_pos_init', 'x', 25)
Sim2.set_property_axis('set_pos_init', 'y', 15)
Sim2.set_property('set_acceleration', 19.3)

Sim1.run()
Sim2.run()

#print(Sim1._x_pid.error)

fig = plt.figure('Position X')
ax = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
ax.plot(x, Sim1.table.x.pos)
ax.plot(x, Sim2.table.x.pos)

fig = plt.figure('Angle is X Dimension')
cx = plt.axes()
x = np.linspace(0, t_sim, int(t_sim / t_p))
#cx.plot(x, t.get_list_y())
cx.plot(x, Sim1.table.x.angle)

fig2 = plt.figure('Object movement')
bx = plt.axes()
bx.plot(Sim1.table.x.pos, Sim1.table.y.pos)
plt.show()

