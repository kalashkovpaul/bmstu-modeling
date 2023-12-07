from random import random

class Generator:
    def __init__(self, a, b):
        self.a, self.b = a, b

    def get_time_interval(self):
        return self.a + (self.b - self.a) * random()