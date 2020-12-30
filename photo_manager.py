"""
작성자	: chaos7ds
작성일	: 2020.12.29 ~
"""
# 도입부
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# 정의부
form_class = uic.loadUiType("gui.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 집행부
app = QApplication(sys.argv)
myWindow = WindowClass()
myWindow.show()
app.exec_()
