import math
from dataclasses import dataclass


@dataclass
class NoiseGenerator:
    _noise_frequency: float = 0
    _noise_period: float = 0
    _noise_level: float = 0
    _noise_type: int = 0
    _tp: float = 0.01
    _noise_active: bool = False

    def noise(self, n):
        if self._noise_active is False or int(self._noise_period / self._tp) < n or self._noise_period == 0 \
                or self._noise_frequency == 0:
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
        val = self._noise_level * math.sin(2 * math.pi * self._noise_frequency * (n * self._tp))
        return val

    def set_noise_frequency(self, noise_frequency: float):
        self._noise_frequency = noise_frequency

    def set_noise_period(self, noise_period: float):
        self._noise_period = noise_period

    def set_noise_level(self, noise_level: float):
        self._noise_level = noise_level

    def set_noise_type(self, noise_type: int):
        self._noise_type = noise_type

    def set_noise_active(self, noise_active: bool):
        self._noise_active = noise_active

    def set_tp(self, tp: float):
        self._tp = tp
