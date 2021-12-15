import math
import noise_generator as ng


class Dimension:
    noise_gen: ng.NoiseGenerator

    def __init__(self, pos_init=0, speed_init=0.0, angle_init=0, g=9.81, noise_frequency=0, noise_period=0,
                 noise_level=0, noise_type=0, tp=0):

        # list of object position
        self._pos = [float(pos_init)]
        # list of object speed
        self._speed = [float(speed_init)]
        # list of table angle in this dimension
        self._angle = [float(angle_init)]
        # gravitational acceleration
        self._g = float(g)

        # init noise generator object
        self.noise_gen = ng.NoiseGenerator(noise_frequency, noise_period, noise_level, noise_type, tp)

    def simulate(self, angle):
        angle += self.noise_gen.noise(len(self._pos) - 1)
       # TODO limit
       # angle = max(min(80, angle), -80)
        actual_speed = self._g * math.sin(math.radians(angle))
        actual_pos = self._pos[-1] + self._speed[-1] + actual_speed

        self._speed.append(actual_speed)
        self._pos.append(actual_pos)
        self._angle.append(angle)

        return actual_pos

    def get_pos(self, n=-1):
        return self._pos[n]

    def get_pos_list(self):
        return self._pos

    def get_speed(self, n=-1):
        return self._speed[n]

    def get_speed_list(self):
        return self._speed

    def get_angle(self, n=-1):
        return self._angle[n]

    def get_angle_list(self):
        return self._angle
