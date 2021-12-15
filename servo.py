class Servo:
    # servo angle range of work [degrees]
    _alpha_min = -30.0
    _alpha_max = 30.0
    # servo voltage range of work [Volt]
    _voltage_min = -10.0
    _voltage_max = 10.0

    def __init__(self, alpha_min=-30.0, alpha_max=30.0, voltage_min=-10.0, voltage_max=10.0):
        self._alpha_min = alpha_min
        self._alpha_max = alpha_max
        self._voltage_min = voltage_min
        self._voltage_max = voltage_max

    # calculate angle based on signal voltage and rotate servo
    # TODO: rotation = ax + b , ax only now
    def rotate(self, signal):
        return ( (self._alpha_max - self._alpha_min) / (self._voltage_max - self._voltage_min) ) * signal
