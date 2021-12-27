from dataclasses import dataclass


@dataclass
class Sensor:
    _asked_value: float = 0.0

    # calculate error
    def error(self, value):
        return self._asked_value - value

    def set_asked_value(self, asked_value: float):
        self._asked_value = asked_value
