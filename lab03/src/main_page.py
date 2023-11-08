from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from generators import TableGenerator, AlgorithmGenerator, get_koeff

line_width = 125

calculate_button_width = 120
calculate_button_text = 'Вычислить'
generate_button_width = 200
generate_button_text = 'Сгенерировать'

manual_width = 125
generate_table_width = 357
table_height = 324
koeff_table_heidht = 54

koeff_title = 'Коэффициент'
error_message = 'Ошибка ввода'

file_path = 'number_table.txt'
count = 10


class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.__create_tables()

        self.table_generator = TableGenerator(file_path)
        self.algorithm_generator = AlgorithmGenerator()
        manual = self.__create_manual()
        table = self.__create_table()
        algorithm = self.__create_algorithm()
        self.__create_buttons(table, algorithm, manual)

    def __create_manual(self):
        manual = QVBoxLayout()
        manual_title = QLabel('Ручной ввод')
        manual_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual.addWidget(manual_title)
        manual.addWidget(self.manual_table)

        manual_koeff_title = QLabel(koeff_title + ':')
        manual_koeff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual.addWidget(manual_koeff_title)
        manual.addWidget(self.manual_koeff)

        manual_button = QPushButton(calculate_button_text)
        manual_button.clicked.connect(self.__get_manual_koeff)
        manual_button.setFixedWidth(calculate_button_width)
        manual.addWidget(manual_button)
        return manual

    def __create_table(self):
        table = QVBoxLayout()
        table_title = QLabel('Табличный способ')
        table_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table.addWidget(table_title)
        table.addWidget(self.tabular_table)
        tabular_koeff_title = QLabel(koeff_title + 'ы:')
        tabular_koeff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table.addWidget(tabular_koeff_title)
        table.addWidget(self.tabular_koeff)
        return table

    def __create_algorithm(self):
        algorithm = QVBoxLayout()
        algorithm_title = QLabel('Алгоритмический способ')
        algorithm_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        algorithm.addWidget(algorithm_title)
        algorithm.addWidget(self.algorithmic_table)
        algorithmic_koeff_title = QLabel(koeff_title + 'ы:')
        algorithmic_koeff_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        algorithm.addWidget(algorithmic_koeff_title)
        algorithm.addWidget(self.algorithmic_koeff)
        return algorithm

    def __create_buttons(self, table, algorithm, manual):
        generate_button = QPushButton(generate_button_text)
        generate_button.setFixedWidth(generate_button_width)
        generate_button.clicked.connect(self.__generate_numbers)

        solve_button = QPushButton(calculate_button_text)
        solve_button.setFixedWidth(calculate_button_width)
        solve_button.clicked.connect(self.__get_koeffs)
        buttons = QHBoxLayout()
        buttons.addWidget(generate_button)
        buttons.addWidget(solve_button)

        tables = QHBoxLayout()
        tables.addLayout(algorithm)
        tables.addLayout(table)

        generation_part = QVBoxLayout()
        generation_part.addLayout(tables)
        generation_part.addLayout(buttons)

        hbox = QHBoxLayout()
        hbox.addLayout(generation_part)
        hbox.addLayout(manual)

        self.setLayout(hbox)

    def __create_tables(self):
        self.manual_table = QTableWidget()
        self.manual_table.setFixedSize(manual_width, table_height)
        self.manual_table.setRowCount(10)
        self.manual_table.setColumnCount(1)

        self.manual_koeff = QTableWidget()
        self.manual_koeff.setFixedSize(manual_width, koeff_table_heidht)
        self.manual_koeff.setRowCount(1)
        self.manual_koeff.setColumnCount(1)

        self.tabular_table = QTableWidget()
        self.tabular_table.setFixedSize(generate_table_width, table_height)
        self.tabular_table.setColumnCount(3)

        self.tabular_koeff = QTableWidget()
        self.tabular_koeff.setFixedSize(generate_table_width, koeff_table_heidht)
        self.tabular_koeff.setRowCount(1)
        self.tabular_koeff.setColumnCount(3)

        self.algorithmic_table = QTableWidget()
        self.algorithmic_table.setFixedSize(generate_table_width, table_height)
        self.algorithmic_table.setColumnCount(3)

        self.algorithmic_koeff = QTableWidget()
        self.algorithmic_koeff.setFixedSize(generate_table_width,  koeff_table_heidht)
        self.algorithmic_koeff.setRowCount(1)
        self.algorithmic_koeff.setColumnCount(3)

    def __get_manual_koeff(self):
        try:
            numbers = self.__get_numbers(self.manual_table, 0, check=True)
        except:
            return

        koeff = round(get_koeff(numbers), 5)
        self.manual_koeff.setItem(0, 0, QTableWidgetItem(str(koeff)))

    def __generate_numbers(self):
        self.tabular_table.setRowCount(count)
        self.algorithmic_table.setRowCount(count)

        for digit in range(1, 4):
            self.__fill_numbers(self.tabular_table, digit - 1, self.table_generator.read_s(digit, count))
            self.__fill_numbers(self.algorithmic_table, digit - 1, self.algorithm_generator.get_sequence(digit, count))

    def __get_koeffs(self):
        algorithmic_koeffs = []
        tabular_koeffs = []

        for column in range(3):
            algorithmic_numbers = self.__get_numbers(self.algorithmic_table, column)
            algorithmic_koeffs.append(round(get_koeff(algorithmic_numbers), 5))
            tabular_numbers = self.__get_numbers(self.tabular_table, column)
            tabular_koeffs.append(round(get_koeff(tabular_numbers), 5))

        self.__fill_koeffs(self.tabular_koeff, tabular_koeffs)
        self.__fill_koeffs(self.algorithmic_koeff, algorithmic_koeffs)

    def __get_numbers(self, table, column, check=False):
        numbers = []

        for i in range(table.rowCount()):
            try:
                item = table.model().index(i, column).data()

                if check:
                    self.__check_number(item)
            except:
                raise ValueError
            else:
                numbers.append(int(item))

        return numbers

    def __fill_numbers(self, table, column, numbers):
        for i in range(table.rowCount()):
            table.setItem(i, column, QTableWidgetItem(str(numbers[i])))

    def __fill_koeffs(self, table, koeffs):
        for i, koeff in enumerate(koeffs):
            table.setItem(0, i, QTableWidgetItem(str(koeff)))

    def __check_number(self, item):
        try:
            item = int(item)
        except:
            self.__error_msg('Необходимо ввести целое число.')
            raise ValueError
        else:
            if item < 0 or item // 10 != 0:
                self.__error_msg('Число должно быть одноразрядным и положительным.')
                raise ValueError

    def __error_msg(self, text):
        msg = QMessageBox()

        msg.setText(text)
        msg.setWindowTitle(error_message)

        msg.exec()