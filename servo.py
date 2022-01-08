from dataclasses import dataclass


@dataclass
class Servo:
    # servo angle range of work [degrees]
    _angle_min: float = -30.0
    _angle_max: float = 30.0
    # servo voltage range of work [Volt]
    _voltage_min: float = -10.0
    _voltage_max: float = 10.0

    # calculate angle based on signal voltage and rotate servo
    # using range conversion formula
    def rotate(self, signal):
        voltage_range = self._voltage_max - self._voltage_min
        if voltage_range == 0:
            return self._angle_min

        angle_range = self._angle_max - self._angle_min

        angle_signal = (((signal - self._voltage_min) * angle_range) / voltage_range) + self._angle_min

        return min(max(angle_signal, self._angle_min), self._angle_max)

    def set_angle_min(self, angle_min: float):
        self._angle_min = angle_min

    def set_angle_max(self, angle_max: float):
        self._angle_max = angle_max

    def set_voltage_min(self, voltage_min: float):
        self._voltage_min = voltage_min

    def set_voltage_max(self, voltage_max: float):
        self._voltage_max = voltage_max
