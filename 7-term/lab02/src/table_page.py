from PyQt6.QtWidgets import (
    QWidget,
    QSpinBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from system import System

spinbox_width = 40
form_text = 'Количество состояний системы: '
btn_width = 110
btn_text = 'Определить'

table_width = 1022
matrix_table_height = 400
result_table_height = 100
error_title = 'Ошибка ввода'
min_number_states = 1
max_number_states = 10

class TablePage(QWidget):
    def __init__(self):
        super().__init__()

        self.matrix_size_spinbox = QSpinBox()
        self.matrix_size_spinbox.setFixedWidth(spinbox_width)
        self.matrix_size_spinbox.setRange(min_number_states,
                                   max_number_states)
        self.matrix_size_spinbox.valueChanged.connect(self.__change_tables)

        self.system = System(int(self.matrix_size_spinbox.value()))

        self.__create_tables()

        form = QFormLayout()
        form.addRow(form_text, self.matrix_size_spinbox)

        btn = QPushButton(btn_text)
        btn.setFixedWidth(btn_width)
        btn.clicked.connect(self.__calculate_time_and_probs)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(form)
        self.hbox.addWidget(btn)

        vbox = QVBoxLayout()
        vbox.addLayout(self.hbox)
        vbox.addWidget(QLabel('Матрица интенсивностей переходов:'))
        vbox.addWidget(self.matrix)
        vbox.addWidget(QLabel('Вероятности и среднее относительное время пребывания в предельном стационарном состоянии:'))
        vbox.addWidget(self.results)
        self.setLayout(vbox)

    def __create_tables(self):
        self.matrix = QTableWidget()
        self.matrix.setFixedSize(table_width, matrix_table_height)
        self.matrix.setRowCount(self.system.number_states)
        self.matrix.setColumnCount(self.system.number_states)

        self.results = QTableWidget()
        self.results.setFixedSize(table_width, result_table_height)
        self.results.setRowCount(2)
        self.results.setColumnCount(self.system.number_states)
        self.results.setVerticalHeaderItem(0, QTableWidgetItem('P  '))
        self.results.setVerticalHeaderItem(1, QTableWidgetItem('t  '))

    def __change_tables(self):
        prev_size = self.system.number_states
        self.system.number_states = int(self.matrix_size_spinbox.value())

        if self.system.number_states > prev_size:
            for i in range(self.system.number_states - prev_size):
                self.matrix.insertRow(prev_size + i)
                self.matrix.insertColumn(prev_size + i)
                self.results.insertColumn(prev_size + i)
        elif self.system.number_states < prev_size:
            for i in range(prev_size - self.system.number_states):
                self.matrix.removeRow(prev_size - i - 1)
                self.matrix.removeColumn(prev_size - i - 1)
                self.results.removeColumn(prev_size - i - 1)

    def __calculate_time_and_probs(self):
        try:
            self.__set_system()
            probabilities = self.system.get_limit_probabilities()
            self.__fill_probs(probabilities)
            time = self.system.get_time_to_stable(probabilities)
            self.__fill_time(time)
        except:
            self.__error_msg('Матрица интенивностей вырожденная, задайте больше интенсивностей')


    def __set_system(self):
        matrix = []

        for i in range(self.system.number_states):
            matrix.append([])
            for j in range(self.system.number_states):
                try:
                    item = self.matrix.model().index(i, j).data()
                    if not item:
                        item = 0
                    self.__check_item(item)
                except:
                    raise ValueError
                else:
                    matrix[i].append(float(item))

        self.system.intensity_matrix = matrix

    def __fill_probs(self, probs):
        for state, probs in enumerate(probs):
            self.results.setItem(0, state,
                               QTableWidgetItem(str(round(probs, 2))))

    def __fill_time(self, time):
        for state, value in enumerate(time):
            self.results.setItem(1, state,
                               QTableWidgetItem(str(round(value, 2))))

    def __check_item(self, item):
        try:
            item = float(item)
            if item < 0:
                self.__error_msg('Интенсивность перехода из состояния в состояние должна быть неотрицательной.')
                raise ValueError
        except:
            self.__error_msg('Интенсивность перехода из состояния в состояние должна быть вещественным числом.')
            raise ValueError

    def __error_msg(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(error_title)
        msg.exec()