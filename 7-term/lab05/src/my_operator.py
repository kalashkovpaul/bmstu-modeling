from time_generator import TimeGenerator

class Operator:
    def __init__(self, time_value, time_limit, computer):
        self.time_generator = TimeGenerator(time_value - time_limit, time_value + time_limit)
        self.computer = computer
        self.max_time = time_value + time_limit
        self.time_next = 0
        self.free = True

    def generate_time(self, prev_time):
        self.time_next = prev_time + self.time_generator.get_interval()

    def is_free(self):
        return self.free

    def set_free(self):
        self.free = True

    def set_busy(self):
        self.free = False

    def get_computer(self):
        return self.computer
