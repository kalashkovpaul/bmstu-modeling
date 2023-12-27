from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QMessageBox
)
from PyQt6.QtGui import QAction

from main_page import MainPage


title = 'Лабораторная работа №3 по курсу "Моделирование", тема: Генерация псевдослучайных чисел'
width = 900
height = 600
info_title = 'Подробнее о программе'
info_text = 'Автор: Калашков Павел, ИУ7-76Б'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.__create_toolbar()
        page = MainPage()
        self.setCentralWidget(page)

    def __create_toolbar(self):
        toolbar = QToolBar()
        info_button = QAction(info_title, self)
        info_button.triggered.connect(self.__show_author)
        info_button.setCheckable(True)
        toolbar.addAction(info_button)
        self.addToolBar(toolbar)

    def __show_author(self):
        info = QMessageBox()
        info.setText(info_text)
        info.setWindowTitle(info_title)
        info.exec()