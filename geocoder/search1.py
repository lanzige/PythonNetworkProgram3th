#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/2/23 11:03
# @Author    : duzy
# @File      : search1.py.py
# @Software  : PyCharm

import threading
import time

class Mother:
    def __init__(self,evt):
        self.evt = evt
        self.sign = True

    def MakeCook(self):
        while self.sign:
            print('饭没好呢，等等吧')
            time.sleep(2)
        self.evt.set()

    def CookFinish(self):
        self.sign = False

class Son():
    def __init__(self,evt):
        self.evt = evt

    def EatCook(self):
        print('妈！什么时候吃饭啊！')
        self.evt.wait()
        print('真香')

evt = threading.Event()
mon = Mother(evt)
sss = Son(evt)
A = threading.Thread(target=sss.EatCook)
B = threading.Thread(target=mon.MakeCook)

A.start()
B.start()
time.sleep(10)
mon.CookFinish()
