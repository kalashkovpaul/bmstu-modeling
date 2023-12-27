from random import random
from math import log

class Handler:
    def __init__(self, k, lambd):
        self.k, self.lambd = k, lambd
        self.free = True

    def get_time_interval(self):
        random_sum = sum([log(1 - random()) for _ in range(self.k)])
        chance =  -1 / (self.k * self.lambd) * random_sum
        print(chance)
        return chance