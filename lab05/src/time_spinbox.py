from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QSpinBox,
    QLabel,
    QHBoxLayout
)

min_minutes = 1
max_minutes = 59

class TimeSpinBox(QWidget):
    def __init__(self, value=1, limit=1):
        super().__init__()
        self.value = QSpinBox()
        self.value.setRange(min_minutes, max_minutes)
        self.value.setValue(value)
        self.limit = QSpinBox()
        self.limit.setRange(min_minutes, max_minutes)
        self.limit.setValue(limit)
        sign = QLabel('±')
        sign.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.value)
        self.hbox.addWidget(sign)
        self.hbox.addWidget(self.limit)
