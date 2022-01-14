import math
import noise_generator as ng


class Dimension:
    noise_gen: ng.NoiseGenerator
    _pos_init: float = 0.0
    _speed_init: float = 0.0
    _angle_init: float = 0.0
    _g: float = 9.81
    _angle_min: float = -30.0
    _angle_max: float = 30.0
    _tp: float = 0.01

    def __init__(self, pos_init: float = 0.0, speed_init: float = 0.0, angle_init: float = 0.0, g: float = 9.81,
                 tp: float = 0.01):
        # initial values are kept in memory for reset purposes
        self._pos_init = pos_init
        self._speed_init = speed_init
        self._angle_init = angle_init

        self._g = g
        self._tp = tp
        self._pos = [self._pos_init]
        self._speed = [self._speed_init]
        self._angle = [self._angle_init]

    def init_noise_generator(self, noise_frequency: float = 0, noise_period: float = 0,
                             noise_level: float = 0, noise_type: int = 0, tp: float = 0.01):
        # init noise generator object
        self.noise_gen = ng.NoiseGenerator(noise_frequency, noise_period, noise_level, noise_type, tp)

    def reset(self):
        self._pos = [self._pos_init]
        self._speed = [self._speed_init]
        self._angle = [self._angle_init]

    def simulate_position(self, angle):
        angle += self.noise_gen.noise(len(self._pos) - 1)
        angle = max(min(self._angle_max, angle), self._angle_min)
        actual_speed = self._speed[-1] + self._g * math.sin(math.radians(angle)) * self._tp
        actual_pos = self._pos[-1] + actual_speed

        self._speed.append(actual_speed)
        self._pos.append(actual_pos)
        self._angle.append(angle)

        return actual_pos

    @property
    def pos(self):
        return self._pos

    @property
    def speed(self):
        return self._speed

    @property
    def angle(self):
        return self._angle

    def set_pos_init(self, pos_init: float):
        print(pos_init)
        self._pos_init = pos_init

    def set_speed_init(self, speed_init: float):
        self._speed_init = speed_init

    def set_angle_init(self, angle_init: float):
        self._angle_init = angle_init

    def set_acceleration(self, g: float):
        self._g = g

    def set_angle_min(self, angle_min: float):
        self._angle_min = angle_min

    def set_angle_max(self, angle_max: float):
        self._angle_max = angle_max

    def set_noise_frequency(self, noise_frequency: float):
        self.noise_gen.set_noise_frequency(noise_frequency)

    def set_noise_period(self, noise_period: float):
        self.noise_gen.set_noise_period(noise_period)

    def set_noise_level(self, noise_level: float):
        self.noise_gen.set_noise_level(noise_level)

    def set_noise_type(self, noise_type: int):
        self.noise_gen.set_noise_type(noise_type)

    def set_noise_active(self, noise_active: bool):
        self.noise_gen.set_noise_active(noise_active)

    def set_tp(self, tp: float):
        self._tp = tp
        self.noise_gen.set_tp(tp)
