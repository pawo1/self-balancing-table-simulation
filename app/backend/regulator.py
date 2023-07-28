from dataclasses import dataclass, field


@dataclass
class Regulator:
    # servo voltage range of work[V]
    _voltage_min: float = -10.0
    _voltage_max: float = 10.0
    _voltage_last: float = 0
    # amplification
    _kp: float = 0.015
    # sampling time [s]
    _tp: float = 0.01
    # integration time
    _ti: float = 0.05
    # derivative time
    _td: float = 0.25
    # algorithm type 0 - positional, 1 - incremental
    _pid_type: int = 0
    _sum_err: float = field(init=False, default=0)

    def __post_init__(self):
        self._error = []

    def reset(self):
        self._error.clear()
        self._sum_err = 0

    # add error to regulator memory
    def add_error(self, val):
        self._error.append(val)

    # run PID regulator
    def run_pid(self):

        if self._pid_type == 0:
            return self.pid_positional()
        else:
            return self.pid_incremental()

    def pid_positional(self):

        # latest error is always last element in list
        self._sum_err += self._error[-1]

        integral_value = (self._tp / self._ti) * self._sum_err
        derivative_value = (self._td / self._tp) * (self._error[-1] - self._error[-2])
        # calculate voltage value proportional to current error, integral and derivative part
        value = self._kp * (self._error[-1] + integral_value + derivative_value)

        # limit voltage to servo range of work
        limited_voltage = min(max(self._voltage_min, value), self._voltage_max)

        return limited_voltage

    def pid_incremental(self):

        # delta based on previous and current error
        delta_e = (self._error[-1] - self._error[-2])

        integral_value = (self._tp / self._ti) * self._error[-1]
        derivative_value = (self._td / self._tp) * delta_e * delta_e
        # calculate voltage value proportional to current error, integral and derivative part
        value = self._kp * (delta_e + integral_value + derivative_value)

        voltage = self._voltage_last + value
        # limit voltage to servo range of work
        self._voltage_last = min(max(self._voltage_min, voltage), self._voltage_max)

        return self._voltage_last

    def set_voltage_min(self, voltage_min: float):
        self._voltage_min = voltage_min

    def set_voltage_max(self, voltage_max: float):
        self._voltage_max = voltage_max

    def set_kp(self, kp: float):
        self._kp = kp

    def set_tp(self, tp: float):
        self._tp = tp

    def set_ti(self, ti: float):
        self._ti = ti

    def set_td(self, td: float):
        self._td = td

    def set_pid_type(self, pid_type: int):
        self._pid_type = pid_type
