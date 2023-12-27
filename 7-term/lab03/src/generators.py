from twist_generator import TwistGenerator
from math import log
def get_koeff(numbers):
    differences = [abs(numbers[i + 1] - numbers[i]) for i in range(len(numbers) - 1)]
    max_difference = max(differences)

    if max_difference == 0:
        ratios = [1] * len(differences)
    else:
        ratios = [difference / max_difference for difference in differences]
    koeff = sum(ratios) / len(ratios)

    entropy = get_entropy(numbers)

    result = ((1 - entropy) + koeff) / 2
    # print(f'Entropy: {entropy}')
    print(f'Koeff: {koeff}')

    return result

def get_entropy(numbers):
    count = len(numbers)
    if count == 0 or count == 1:
        return 0

    hist = dict()
    for el in numbers:
        if el not in hist.keys():
            hist.update({el: 1})
        else:
            hist[el] += 1

    koeff = 0
    for el in hist.keys():
        p = hist[el] / count
        koeff -= p * log(p, count)


    return koeff

gen1digit = TwistGenerator()
gen1digit.SetW(4)
gen1digit.start(2)

gen2digit = TwistGenerator()
gen2digit.SetW(7)
gen2digit.start(2)

gen3digit = TwistGenerator()
gen3digit.SetW(10)
gen3digit.start(2)


class AlgorithmGenerator:
    def get_sequence(self, digits_number, elements_number):
        sequence = []
        gen = gen1digit
        if digits_number == 1:
            gen = gen1digit
        elif digits_number == 2:
            gen = gen2digit
        elif digits_number == 3:
            gen = gen3digit

        maximum = 10**digits_number

        while elements_number:
            next = gen.Next()
            if next < maximum:
                sequence.append(next)
            else:
                sequence.append(next % maximum)
            elements_number -= 1

        return sequence

class TableGenerator:
    def __init__(self, file_path):
        self.table = open(file_path, 'r')

    def read_s(self, digits, total):
        s = []
        divider = pow(10, digits)
        while total:
            item = self.table.read(6)
            if item == '':
                self.table.seek(0)
                item = self.table.read(6)
            item = int(item[:5])
            while item:
                if total:
                    random = item % divider

                    if len(str(random)) == digits:
                        s.append(random)
                        total -= 1

                    item //= 10
                else:
                    return s

        return s

    def __del__(self):
        self.table.close()