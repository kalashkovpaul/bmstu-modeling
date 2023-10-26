from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QMessageBox
)
from PyQt6.QtGui import QAction

from table_page import TablePage


title = 'Лабораторная работа №2 по курсу "Моделирование", тема: Марковские процессы'
width = 1080
height = 740
info_title = 'Подробнее о программе'
info_text = 'Автор: Калашков Павел, ИУ7-76Б'



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(width, height)
        self.setWindowTitle(title)

        self.__createToolbar()
        page = TablePage()
        self.setCentralWidget(page)

    def __createToolbar(self):
        toolbar = QToolBar()
        btn = QAction(info_title, self)
        btn.triggered.connect(self.__show_author)
        btn.setCheckable(True)
        toolbar.addAction(btn)

        self.addToolBar(toolbar)

    def __show_author(self):
        info = QMessageBox()
        info.setText(info_text)
        info.setWindowTitle(info_title)
        info.exec()