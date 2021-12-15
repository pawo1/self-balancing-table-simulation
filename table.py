import dimension


class Table:
    _x: dimension.Dimension
    _y: dimension.Dimension

    def __init__(self, pos_x=0.7, pos_y=0.3, speed_x=0.0, speed_y=0.0, angle_x=0.0, angle_y=0.0, g=9.81):
        self._x = dimension.Dimension(pos_x, speed_x, angle_x, g)
        self._y = dimension.Dimension(pos_y, speed_y, angle_y, g)

    def simulate(self, angle_x, angle_y):
        pos_x = self._x.simulate(angle_x)
        pos_y = self._y.simulate(angle_y)

        return pos_x, pos_y

    def get_pos_x_list(self):
        return self._x.get_pos_list()

    def get_pos_x(self, n=-1):
        return self._x.get_pos(n)

    def get_pos_y_list(self):
        return self._y.get_pos_list()

    def get_pos_y(self, n=-1):
        return self._y.get_pos(n)

    def get_angle_x_list(self):
        return self._x.get_angle_list()

    def get_angle_x(self, n=-1):
        return self._x.get_angle(n)

    def get_angle_y_list(self):
        return self._y.get_angle_list()

    def get_angle_y(self, n=-1):
        return self._y.get_angle(n)

    def get_speed_x_list(self):
        return self._x.get_speed_list()

    def get_speed_x(self, n=-1):
        return self._x.get_speed(n)

    def get_speed_y_list(self):
        return self._y.get_speed_list()

    def get_speed_y(self, n=-1):
        return self._y.get_speed(n)
