from time_generator import TimeGenerator

class ClientGenerator:
    def __init__(self, time_value, time_limit, operators, number):
        self.generator = TimeGenerator(time_value - time_limit, time_value + time_limit)
        self.operators = sorted(operators, key= lambda operator: operator.max_time)
        self.time_next = 0
        self.number = number

    def generate_client(self, time_prev):
        self.time_next = time_prev + self.generator.get_interval()

    def choose_operator(self):
        for operator in self.operators:
            if operator.is_free():
                return operator
        return None
