class Regulator:
    # servo voltage range of work[V]
    _u_min = -10.0
    _u_max = 10.0
    _u_last = 0
    # amplification
    _kp = 0.015
    # sampling time [s]
    _tp = 0.1
    # integration time
    _ti = 0.05
    # derivative time
    _td = 0.25
    # algorithm type 0 - positional, 1 - incremental
    _pid_type = 0

    def __init__(self, u_min=-10.0, u_max=10.0, kp=0.25, tp=0.1, ti=0.05, td=0.25, pid_type=1):
        self._u_min = float(u_min)
        self._u_max = float(u_max)
        self._kp = float(kp)
        self._tp = float(tp)
        self._ti = float(ti)
        self._td = float(td)
        self._pid_type = pid_type
        # error list
        self.error = []
        # sum of errors
        self.sum_err = 0

    # add error to regulator memory
    def add_error(self, val):
        self.error.append(val)

    # run PID regulator
    def run_pid(self):

        if self._pid_type == 0:
            return self.pid_positional()
        else:
            return self.pid_incremental()

    # positional algorithm
    def pid_positional(self):

        self.sum_err += self.error[-1]

        val = self._kp * (self.error[-1] + ((self._tp / self._ti) * self.sum_err) + ((self._td / self._tp) *
                                                                                    (self.error[-1] - self.error[-2])))
        print(val)
        # limit voltage to servo range of work
        return min(max(self._u_min, val), self._u_max)

    # incremental algorithm
    def pid_incremental(self):
        delta_e = (self.error[-1] - self.error[-2])
        val = self._kp * (delta_e + ((self._tp / self._ti) * self.error[-1]) + ((self._td / self._tp) *
                                                                                delta_e * delta_e))

        u = self._u_last + val
        # limit voltage to servo range of work
        self._u_last = min(max(self._u_min, u), self._u_max)

        return self._u_last
