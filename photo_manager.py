"""
작성자	: chaos7ds
작성일	: 2020.12.29 ~
"""
# 도입부
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
from PIL import Image
import getpass

# 정의부
form_class = uic.loadUiType("gui.ui")[0]

dir_root = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리'
dir_unsorted = dir_root + '/unsorted_정리할 사진'
dir_sorted = dir_root + '/sorted_정리된 사진'


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 환경 확인
        self.check_dir(dir_root)
        self.check_dir(dir_sorted)
        self.check_dir(dir_unsorted)

        # 기존 사진 이름 리스트
        self.name_list = []
        self.make_name_list()
        print(self.name_list)

        # make DB
        self.make_DB()

        # 리스트 설정
        for i in range(len(self.DB[0])):
            self.list_widget_1.addItem(self.DB[0][i])

        # 리스트 기능 설정
        """self.list_widget_1.itemClicked.connect(함수)
        self.list_widget_2.itemClicked.connect(함수)
        self.list_widget_3.itemClicked.connect(함수)"""

        # 버튼 기능 설정
        self.btn_trash.clicked.connect(self.move_trash)
        self.btn_execute.clicked.connect(self.move_execute)
        self.btn_find_1.clicked.connect(lambda: self.btn_find(1))
        self.btn_find_2.clicked.connect(lambda: self.btn_find(2))
        self.btn_find_3.clicked.connect(lambda: self.btn_find(3))
        self.btn_add_1.clicked.connect(lambda: self.btn_add(1))
        self.btn_add_2.clicked.connect(lambda: self.btn_add(2))
        self.btn_add_3.clicked.connect(lambda: self.btn_add(3))

    # general func
    def name2lst(self, n):
        return n.split('_')

    def lst2name(self, l):
        ans = ''
        for i in l:
            ans = ans + i + '_'
        return ans[:-1]

    # special func
    def check_dir(self, d):
        if not os.path.isdir(d):
            os.makedirs(os.path.join(d))

        if d == dir_unsorted:
            im = Image.new("RGB", (512, 512), "white")
            im.save(dir_unsorted + '/���오류 방지용 파일.jpg')

    def make_name_list(self):
        for i in os.listdir(dir_sorted):
            i = i[:i.rfind('.')]
            self.name_list.append(self.name2lst(i))

    def make_DB(self):
        self.DB = [[], [], ['(oo)', '(ox)', '(xx)']]
        tmp1 = ''
        tmp2 = []
        for i in range(len(self.name_list)):
            tmp = self.name_list[i]
            if not tmp[0] == tmp1:
                if tmp1 != '':
                    self.DB[0].append(tmp1)
                    self.DB[1].append(tmp2)
                tmp1 = tmp[0]
                tmp2 = []
            if not tmp[1] in tmp2:
                tmp2.append(tmp[1])
        self.DB[0].append(tmp1)
        self.DB[1].append(tmp2)

        print(self.DB)

    def move_trash(self):
        print("휴지통")

    def move_execute(self):
        print("exe")

    def btn_find(self, k):
        print(f"find {k}")

    def btn_add(self, k):
        print(f"add {k}")


# 집행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
