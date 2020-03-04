#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/2/24 18:35
# @Author    : duzy
# @File      : getname.py
# @Software  : PyCharm
import socket

if __name__ == '__main__':
    hostname = 'www.python.org'
    addr = socket.gethostbyname(hostname)
    print(addr)
