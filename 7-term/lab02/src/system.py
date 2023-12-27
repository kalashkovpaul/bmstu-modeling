from numpy import linalg, transpose, arange
from scipy.integrate import odeint
import matplotlib.pyplot as plt

min_number_states = 1
max_number_states = 10

max_time = 20
time_delta = 0.01
eps = 0.5e-10

class System:
    def __init__(self, number_states):
        self.intensity_matrix = []
        self.number_states = number_states

    def get_limit_probabilities(self):
        coeffs = self.__get_kolmogorov_koeffs()
        coeffs[0] = [1] * self.number_states
        free_numbers = [0] * self.number_states
        free_numbers[0] = 1

        return linalg.solve(coeffs, free_numbers)

    def get_time_to_stable(self, probs):
        time = arange(0, max_time, time_delta)

        start_probabilities = [0] * self.number_states
        start_probabilities[0] = 1

        coeffs = self.__get_kolmogorov_koeffs()

        integrated_probabilities = transpose(odeint(self.__get_derivatives,
                start_probabilities,
                time, args=(coeffs,)))

        stabilization_time = []

        for state in range(self.number_states):
            probabilities = integrated_probabilities[state]

            for i, probability in enumerate(probabilities):
                if abs(probs[state] - probability) < eps:
                    stabilization_time.append(time[i])
                    break

                if i == len(probabilities) - 1:
                    stabilization_time.append(0)

        return stabilization_time

    def __get_kolmogorov_koeffs(self):
        factors = []

        for state in range(self.number_states):
            factors.append([0] * self.number_states)
            for i in range(self.number_states):
                if i != state:
                    factors[state][i] = self.intensity_matrix[i][state]
                    factors[state][state] -= self.intensity_matrix[state][i]

        return factors

    def __get_derivatives(self, probabilities, time, factors):
        derivatives = [0] * self.number_states

        for state in range(self.number_states):
            for i, probability in enumerate(probabilities):
                derivatives[state] += factors[state][i] * probability

        return derivatives