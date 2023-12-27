from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)

from system import System

module = 'Промоделировать'
error_message = 'Ошибка ввода'

min_message_amount = 1
max_message_amount = 100000
min_probability = 0.00
max_probability = 1.00
step = 0.01


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        generation_title = QLabel('Настройка появления сообщений:')
        # generation_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_number = QSpinBox()
        self.msg_number.setRange(min_message_amount, max_message_amount)
        self.step = QDoubleSpinBox()
        self.step.setSingleStep(0.01)
        msg_parameters = QFormLayout()
        msg_parameters.addRow(QLabel('Общее число сообщений:'), self.msg_number)
        msg_parameters.addRow(QLabel('Шаг по времени:'), self.step)
        generation_law = QLabel('Параметры равномерного распределения:')
        generation_law.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.a = QDoubleSpinBox()
        self.a.setSingleStep(step)
        self.a.setRange(-20, 20)
        self.b = QDoubleSpinBox()
        self.b.setSingleStep(step)
        self.b.setRange(-20, 20)
        generation_parameters = QFormLayout()
        generation_parameters.addRow(QLabel('a:'), self.a)
        generation_parameters.addRow(QLabel('b:'), self.b)
        generation = QVBoxLayout()
        generation.addWidget(generation_title)
        generation.addLayout(msg_parameters)
        generation.addWidget(generation_law)
        generation.addLayout(generation_parameters)
        handling_title = QLabel('Настройка обработки сообщений:')
        # handling_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.return_probability = QDoubleSpinBox()
        self.return_probability.setSingleStep(step)
        self.return_probability.setRange(min_probability, max_probability)
        msg_return = QFormLayout()
        msg_return.addRow(QLabel('Вероятность возврата сообщения:'), self.return_probability)

        handling_law = QLabel('Параметры распределения Эрланга:')
        handling_law.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.k = QSpinBox()
        self.k.setSingleStep(1)
        self.k.setRange(1, 200)
        self.lambd = QDoubleSpinBox()
        self.lambd.setSingleStep(step)
        handling_parameters = QFormLayout()
        handling_parameters.addRow(QLabel('k:'), self.k)
        handling_parameters.addRow(QLabel('λ:'), self.lambd)
        handling = QVBoxLayout()
        handling.addWidget(handling_title)
        handling.addLayout(msg_return)
        handling.addWidget(handling_law)
        handling.addLayout(handling_parameters)

        queue_title = QLabel('Результат (максимальная длина очереди):')
        # queue_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.step_length = QLineEdit()
        self.eventful_length = QLineEdit()
        lengths = QFormLayout()
        lengths.addRow(QLabel('Принцип Δt:'), self.step_length)
        lengths.addRow(QLabel('Событийный принцип:'), self.eventful_length)

        queue = QVBoxLayout()
        queue.addWidget(queue_title)
        queue.addLayout(lengths)

        system = QVBoxLayout()
        system.addLayout(generation)
        system.addLayout(handling)
        button = QPushButton(module)
        button.clicked.connect(self.__calculate_max_length)
        system.addWidget(button)
        system.addLayout(queue)

        self.setLayout(system)

    def __calculate_max_length(self):
        msg_number = int(self.msg_number.value())
        step = float(self.step.value())
        return_probability = float(self.return_probability.value())

        a = float(self.a.value())
        b = float(self.b.value())

        k = int(self.k.value())
        lambd = float(self.lambd.value())

        self.system = System(a, b, k, lambd, msg_number, return_probability, step)
        step_max_length = self.system.delta_t()
        eventful_max_length = self.system.event_driven()

        self.step_length.setText(str(step_max_length))
        self.eventful_length.setText(str(eventful_max_length))