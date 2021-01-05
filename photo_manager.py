"""
작성자	: chaos7ds
작성일	: 2020.12.29 ~
"""
# 도입부
import sys
import os
import getpass
import shutil

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from PIL import Image

# 정의부
form_class = uic.loadUiType("gui.ui")[0]

dir_root = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리'
dir_unsorted = dir_root + '/unsorted_정리할 사진'
dir_sorted = dir_root + '/sorted_정리된 사진'
dir_trash = dir_root + '/휴지통'
dir_hold = dir_root + '/보류'


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("이미지 정리 프로그램")

        # 환경 확인
        self.check_dir(dir_root)
        self.check_dir(dir_sorted)
        self.check_dir(dir_unsorted)
        self.check_dir(dir_trash)
        self.check_dir(dir_hold)

        # 대기 상태 설정
        self.set_waiting_state()

        # 리스트뷰 기능 설정
        self.list_widget_1.itemClicked.connect(lambda: self.lw_1(-1))
        self.list_widget_2.itemClicked.connect(self.lw_2)

        # 버튼 기능 설정
        self.btn_trash.clicked.connect(self.move_trash)
        self.btn_hold.clicked.connect(self.move_hold)
        self.btn_execute.clicked.connect(self.move_execute)
        self.btn_find_1.clicked.connect(self.btn_find1)
        self.btn_add_1.clicked.connect(lambda: self.btn_add(1))
        self.btn_add_2.clicked.connect(lambda: self.btn_add(2))

    # vanilla func
    def resizeEvent(self, event):
        self.resize(event.size())
        event.accept()
        self.set_img()

    # general func
    def name2lst(self, n):
        return n.split('_')

    def lst2name(self, l):
        ans = ''
        for i in l:
            ans = ans + i + '_'
        return ans[:-1]

    # custom func
    def check_dir(self, d):
        if not os.path.isdir(d):
            os.makedirs(os.path.join(d))

        if d == dir_unsorted:
            im = Image.new("RGB", (512, 512), "white")
            im.save(dir_unsorted + '/���오류 방지용 파일.jpg')

    def set_waiting_state(self):
        # 변수 선언
        self.idx1 = -1
        self.idx2 = -1

        # 사진 띄우기
        self.set_img()

        # 기존 사진 이름 리스트
        self.name_list = []
        self.make_name_list()

        # make DB
        self.make_DB()

        # 리스트뷰 설정
        self.set_lw(1)
        self.set_lw(3)

    def set_img(self):
        self.sel_file = dir_unsorted + '/' + os.listdir(dir_unsorted)[0]

        pi = QPixmap()
        pi.load(self.sel_file)
        # resize
        if pi.width() > pi.height():
            pi = pi.scaledToWidth(self.label_1.width())
            if pi.height() > self.label_1.height():
                pi = pi.scaledToHeight(self.label_1.height())
        else:
            pi = pi.scaledToHeight(self.label_1.height())
            if pi.width() > self.label_1.width():
                pi = pi.scaledToWidth(self.label_1.width())
        # 이미지 적용
        self.label_1.setPixmap(pi)

    def make_name_list(self):
        for i in os.listdir(dir_sorted):
            i = i[:i.rfind('.')]
            self.name_list.append(self.name2lst(i))

    def make_DB(self):
        self.DB = [[], dict(), dict(), ['(oo)', '(ox)', '(xx)'], []]
        tmp1 = ''
        tmp2 = []
        tmp3 = dict()
        for i in range(len(self.name_list)):
            tmp = self.name_list[i]
            if not tmp[0] == tmp1:
                if tmp1 != '':
                    self.DB[0].append(tmp1)
                    self.DB[1][tmp1] = tmp2
                    self.DB[2][tmp1] = tmp3
                    self.DB[4].append(tmp1.replace(' ', ''))
                tmp1 = tmp[0]
                tmp2 = []
                tmp3 = dict()
            if not tmp[1] in tmp2:
                tmp2.append(tmp[1])
            key = tmp[1]
            tmp3[key] = int(float(tmp[2]))
        self.DB[0].append(tmp1)
        self.DB[1][tmp1] = tmp2
        self.DB[2][tmp1] = tmp3
        self.DB[4].append(tmp1.replace(' ', ''))

        for i in range(len(self.DB)):
            print(f"self.DB {i}\t\t{self.DB[i]}")

    def set_lw(self, k):
        idx = -1
        if k == 1:
            idx = 0
        if k == 3:
            idx = 3

        if idx != -1:
            getattr(self, f"list_widget_{k}").clear()
            for i in range(len(self.DB[idx])):
                getattr(self, f"list_widget_{k}").addItem(self.DB[idx][i])

    # widget func
    def lw_1(self, idx):
        if idx == -1:
            self.idx1 = self.list_widget_1.currentRow()
        self.list_widget_2.clear()

        key1 = self.DB[0][self.idx1]
        for i in range(len(self.DB[1][key1])):
            key2 = self.DB[1][key1][i]
            n = f"{str(self.DB[2][key1][key2]):>5}"
            self.list_widget_2.addItem(n + '_' + key2)

    def lw_2(self):
        self.idx2 = self.list_widget_2.currentRow()

    def move_trash(self):
        if not self.sel_file == dir_unsorted + '/���오류 방지용 파일.jpg':
            if os.path.isdir(dir_trash):
                newdir = dir_trash + '/' + os.listdir(dir_unsorted)[0]
                if not os.path.isfile(newdir):
                    shutil.move(self.sel_file, newdir)
                    self.set_waiting_state()

    def move_hold(self):
        if not self.sel_file == dir_unsorted + '/���오류 방지용 파일.jpg':
            if os.path.isdir(dir_hold):
                newdir = dir_hold + '/' + os.listdir(dir_unsorted)[0]
                if not os.path.isfile(newdir):
                    shutil.move(self.sel_file, newdir)
                    self.set_waiting_state()

    def move_execute(self):
        if not self.sel_file == dir_unsorted + '/���오류 방지용 파일.jpg':
            pass

    def btn_find1(self):
        txt = self.line_edit_1.text()
        txt = txt.replace(' ', '')

        for i in range(len(self.DB[4])):
            if txt in self.DB[4][i]:
                self.idx1 = i
                self.list_widget_1.item(self.idx1).setSelected(True)
                self.lw_1(self.idx1)
                break
        else:
            idx = self.list_widget_1.currentRow()
            self.list_widget_2.clear()
            if idx != -1:
                self.list_widget_1.item(idx).setSelected(False)

        self.line_edit_1.clear()

    def btn_add(self, k):
        txt = getattr(self, f"line_edit_{k}").text()

        if k == 1:
            # DB 0 업데이트
            self.DB[0].append(txt)
            self.DB[0].sort()
            idx = self.DB[0].index(txt)

            # DB 4 업데이트
            self.DB[4] = []
            for i in range(len(self.DB[0])):
                self.DB[4].append(self.DB[0][i].replace(' ', ''))

            # DB 1 업데이트
            key = txt
            self.DB[1][key] = []

            # list widget 업데이트
            self.set_lw(1)
            self.list_widget_2.clear()

            # list_widget_1 select
            self.idx1 = idx
            self.list_widget_1.item(self.idx1).setSelected(True)
            self.lw_1(self.idx1)

        if k == 2:
            # DB 1 업데이트
            idx = self.list_widget_1.currentRow()
            key = self.DB[0][idx]
            self.DB[1][key].append(txt)
            self.DB[1][key].sort()

            # DB 2 업데이트
            key1 = key
            self.DB[2][key1][txt] = 0

            # list_widget_2 업데이트
            self.lw_1(idx)

        getattr(self, f"line_edit_{k}").clear()


# 집행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    myWindow.set_img()  # 추가부분
    app.exec_()
