class Sensor:
    _asked_value = 0.0

    def __init__(self, value=0.0):
        self._asked_value = value

    # calculate error
    def error(self, value):
        return self._asked_value - value
