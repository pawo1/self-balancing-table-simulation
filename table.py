import dimension


class Table:
    x: dimension.Dimension
    y: dimension.Dimension

    def __init__(self, pos_x: float = 0.0, pos_y: float = 0.0, speed_x: float = 0.0,
                 speed_y: float = 0.0, angle_x: float = 0.0, angle_y: float = 0.0,
                 g: float = 9.81):
        self.x = dimension.Dimension(pos_x, speed_x, angle_x, g)
        self.y = dimension.Dimension(pos_y, speed_y, angle_y, g)
        self.x.init_noise_generator()
        self.y.init_noise_generator()

    def reset(self):
        self.x.reset()
        self.y.reset()

    def simulate_position(self, angle_x, angle_y):
        pos_x = self.x.simulate_position(angle_x)
        pos_y = self.y.simulate_position(angle_y)

        return pos_x, pos_y