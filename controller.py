import table
import servo
import regulator
import sensor


class Controller:
    _table: table.Table
    _x_sensor: sensor.Sensor
    _y_sensor: sensor.Sensor
    _x_pid: regulator.Regulator
    _y_pid: regulator.Regulator
    _x_servo: servo.Servo
    _y_servo: servo.Servo
    _tp = 0.01
    _t_sim = 60

    def __init__(self, tp=0.01, t_sim=60, kp=0.25, ti=0.05, td=0.005, pos_x=0.0, pos_y=0.0):

        self._tp = tp
        self._t_sim = t_sim

        # init simulation objects
        self._table = table.Table(pos_x=pos_x, pos_y=pos_y)
        self._x_sensor = sensor.Sensor()
        self._y_sensor = sensor.Sensor()
        self._x_pid = regulator.Regulator(tp=tp, kp=kp, ti=ti, td=td)
        self._y_pid = regulator.Regulator(tp=tp, kp=kp, ti=ti, td=td)
        self._x_servo = servo.Servo()
        self._y_servo = servo.Servo()

    def run(self):
        self._x_pid.add_error(self._x_sensor.error(self._table.get_pos_x()))
        self._y_pid.add_error(self._y_sensor.error(self._table.get_pos_y()))

        for i in range(1, int(self._t_sim / self._tp)):
            # read error from sensor and add it to regulator memory
            self._x_pid.add_error(self._x_sensor.error(self._table.get_pos_x()))
            self._y_pid.add_error(self._y_sensor.error(self._table.get_pos_y()))
            # calculate signal Voltage for servo
            u_x = self._x_pid.run_pid()
            u_y = self._y_pid.run_pid()
            # rotate servo and simulate next step on table
            self._table.simulate(self._x_servo.rotate(u_x), self._y_servo.rotate(u_y))
