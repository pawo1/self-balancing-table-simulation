from dataclasses import dataclass
from setters_dict import setters
import table
import servo
import regulator
import sensor


@dataclass
class Controller:
    _tp: float = 0.01
    _t_sim: float = 60
    _step: int = 0

    def __post_init__(self):

        self.simulation_range = int(self._t_sim / self._tp)

        # init default simulation objects
        self.table = table.Table()
        self._sensor_x = sensor.Sensor()
        self._sensor_y = sensor.Sensor()
        self._pid_x = regulator.Regulator()
        self._pid_y = regulator.Regulator()
        self._servo_x = servo.Servo()
        self._servo_y = servo.Servo()

        # make sure that PID has first value in error list (required by the algorithm at first step)
        self.init_error_list()

    def run(self):
        for i in range(1, self.simulation_range):
            self._step += 1
            self.run_step()

    def run_step(self):

        pos_x = self.table.x.pos[-1]
        pos_y = self.table.y.pos[-1]

        error_x = self._sensor_x.error(pos_x)
        error_y = self._sensor_y.error(pos_y)

        self._pid_x.add_error(error_x)
        self._pid_y.add_error(error_y)

        voltage_x = self._pid_x.run_pid()
        voltage_y = self._pid_y.run_pid()

        angle_x = self._servo_x.rotate(voltage_x)
        angle_y = self._servo_y.rotate(voltage_y)

        self.table.simulate_position(angle_x, angle_y)

    def reset_simulation(self):
        self.table.reset()
        self._pid_x.reset()
        self._pid_y.reset()
        self.init_error_list()

    def init_error_list(self):
        pos_x = self.table.x.pos[-1]
        pos_y = self.table.y.pos[-1]
        error_x = self._sensor_x.error(pos_x)
        error_y = self._sensor_y.error(pos_y)

        self._pid_x.add_error(error_x)
        self._pid_y.add_error(error_y)

    def set_property(self, prop: str, value):

        self.set_property_axis(prop, 'x', value)
        self.set_property_axis(prop, 'y', value)

    def set_property_axis(self, prop: str, axis_name: str, value):

        if axis_name == 'x':
            suffix = '_x'
            if hasattr(self.table.x, prop):
                getattr(self.table.x, prop)(value)
        else:
            suffix = '_y'
            if hasattr(self.table.y, prop):
                getattr(self.table.y, prop)(value)

        if prop in setters:
            for obj_name in setters[prop]:
                obj = getattr(self, obj_name+suffix)
                method = getattr(obj, prop)
                method(value)

        self.reset_simulation()
