import math


class NoiseGenerator:
    _noise_type = 0
    _noise_period = 0
    _noise_frequency = 0
    _noise_level = 0
    _tp = 0

    def __init__(self, noise_frequency=0.0, noise_period=0.0, noise_level=0.0, noise_type=0, t_p=0.01):
        self._noise_type = noise_type
        self._noise_period = noise_period
        self._noise_level = noise_level
        self._noise_frequency = noise_frequency
        self._tp = t_p

    def noise(self, n):
        if self._noise_period < n or self._noise_period == 0:
            return 0

        if self._noise_type == 0:
            return self.impulse_noise(n)

        if self._noise_type == 1:
            return self.sinusoidal_noise(n)

    def impulse_noise(self, n):
        if (n % ((1 / self._noise_frequency) / self._tp)) == 0:
            return self._noise_level
        else:
            return 0

    def sinusoidal_noise(self, n):
        return self._noise_level * math.sin(2 * math.pi * (self._noise_frequency / self._tp) * n)
