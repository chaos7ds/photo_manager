"""
작성자	: chaos7ds
작성일	: 2021.01.05
"""
import os
#import shutil

d = 'C:/Users/chaos/Desktop/MOE(20210102)/사진/anizzal'
n = [str(i) for i in range(10)]
#eng = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
#print(eng)
for i in os.listdir(d):
    mod = 0
    for j in range(len(i)):
        if mod == 10 and i[j] == '.':
            mod = 11
        if mod == 9 and i[j] == ')':
            mod = 10
        if mod == 8 and i[j] == '(':
            mod = 9
        if mod == 7 and i[j] == '_':
            mod = 8
        if mod == 6 and i[j] in n:
            mod = 7
        if mod == 5 and i[j] in n:
            mod = 6
        if mod == 4 and i[j] in n:
            mod = 5
        if mod == 3 and i[j] in n:
            mod = 4
        if mod == 2 and i[j] in n:
            mod = 3
        if mod == 1 and i[j] == '_':
            mod = 2
        if mod == 0 and i[j] == '_':
            mod = 1

    if mod != 11:
        print(i)