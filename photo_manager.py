"""
작성자	: chaos7ds
작성일	: 2020.12.29 ~
"""
# 도입부
import shutil
import os
import tkinter as tk
from PIL import Image, ImageTk
import getpass


# 정의부
def folder_list():
    global folders
    folders = []
    for i in os.listdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리'):
        folders.append(i)


def sel_img():
    global sel_file
    global img
    sel_file = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진/' + \
              os.listdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진')[0]
    # resize image
    oimg = Image.open(sel_file)
    if oimg.size[0] > 750 or oimg.size[1] > 750:
        if oimg.size[0] > oimg.size[1]:
            oimg = oimg.resize((750, int(oimg.size[1] * 750 / oimg.size[0])))
        else:
            oimg = oimg.resize((int(oimg.size[0] * 750 / oimg.size[1]), 750))
    img = ImageTk.PhotoImage(oimg)


def update_image_label():
    sel_img()
    image_label.config(image=img)


def list_make():
    list_box.delete(0, list_box.size() - 1)
    for i in range(1, len(folders)):
        list_box.insert(i, folders[i])


def btn1cl():
    if not os.path.isdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/' + entry.get()):
        os.makedirs(os.path.join('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/' + entry.get()))
    folder_list()
    list_make()


def btn3cl():
    if not sel_file == 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진/�오류 방지용 파일.jpg':
        if os.path.isdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/' + entry.get()):
            newdir = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/' + entry.get() + '/'
            shutil.move(sel_file, newdir + os.listdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진')[0])
            update_image_label()


def btn5cl():
    if not sel_file == 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진/�오류 방지용 파일.jpg':
        if os.path.isdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/_휴지통'):
            newdir = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/_휴지통/'
            shutil.move(sel_file, newdir + os.listdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진')[0])
            update_image_label()


def btn6cl():
    if not sel_file == 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진/�오류 방지용 파일.jpg':
        newdir = 'C://Users/' + getpass.getuser() + '/Desktop/사진 정리/' + folders[list_box.curselection()[0] + 1] + '/'
        shutil.move(sel_file, newdir + os.listdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진')[0])
        update_image_label()


# 집행부
root = tk.Tk()
root.title('이미지 정리 프로그램')

if not os.path.isdir('C://Users/' + getpass.getuser() + '/Desktop/사진 정리'):
    os.makedirs(os.path.join('C://Users/' + getpass.getuser() + '/Desktop/사진 정리'))
    os.makedirs(os.path.join('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진'))
    im = Image.new("RGB", (512, 512), "white")
    im.save('C://Users/' + getpass.getuser() + '/Desktop/사진 정리/!정리할 사진/�오류 방지용 파일.jpg')

# 이동할 폴더 목록
folder_list()

# img 선택
sel_img()

# TK 레이아웃
btn1 = tk.Button(root, text='폴더 추가', width=12, height=17)
btn1.grid(row=0, column=0)

btn2 = tk.Button(root, text='', width=12, height=17)
btn2.grid(row=1, column=0)

btn3 = tk.Button(root, text='입력 이동', width=12, height=17)
btn3.grid(row=2, column=0)

btn4 = tk.Button(root, text='', width=12, height=17)
btn4.grid(row=0, column=2)

btn5 = tk.Button(root, text='휴지통', width=12, height=17)
btn5.grid(row=1, column=2)

btn6 = tk.Button(root, text='선택 이동', width=12, height=17)
btn6.grid(row=2, column=2)

image_label = tk.Label(root, image=img, width=750, height=750)
image_label.grid(row=0, column=1, rowspan=3)

entry = tk.Entry(root)
entry.grid(row=3, column=0, columnspan=3)

list_box = tk.Listbox(root, selectmode='single', font=('Fixed', 12), width=65, height=50)
list_make()
list_box.grid(row=0, column=3, rowspan=4)

# 버튼 이벤트
btn1.config(command=btn1cl)
btn3.config(command=btn3cl)
btn5.config(command=btn5cl)
btn6.config(command=btn6cl)

root.mainloop()
