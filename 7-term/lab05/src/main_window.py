from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QMessageBox
)
from PyQt6.QtGui import QAction
from page import Page


title = 'Лабораторная работа №5 по курсу "Моделирование", тема: Моделирование работы информационного центра'
width = 500
height = 600
info_title = 'Подробнее о программе'
info_text = 'Автор: Калашков Павел, ИУ7-76Б'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.__createToolbar()
        page = Page()
        self.setCentralWidget(page)

    def __createToolbar(self):
        toolbar = QToolBar()
        info_button = QAction(info_title, self)
        info_button.triggered.connect(self.__get_info)
        info_button.setCheckable(True)
        toolbar.addAction(info_button)
        self.addToolBar(toolbar)

    def __get_info(self):
        info = QMessageBox()
        info.setText(info_text)
        info.setWindowTitle(info_title)
        info.exec()
