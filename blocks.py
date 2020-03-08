#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/3/7 17:58
# @Author    : duzy
# @File      : blocks.py.py
# @Software  : PyCharm
import socket,struct
from argparse import ArgumentParser

header_struct = struct.Struct('!I')

def recvall(sock,length):
    '''
    从传入的一个socket中获取长度为length的数据
    :param sock: 一个socket
    :param length: 需要获取数据的长度
    :return: 获取到的所有的数据
    '''
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError(F'socket closed with {length} bytes left in this block.')
        length = length - len(block)
        blocks.append(block)
    return b''.join(blocks)

def get_block(sock):
    #下面获取的数据是先传输过来的总的数据长度，这里使用header_struct.size
    #是因为发送的时候，将长度的数据用header_struct封装，规定死了长度了
    block_length_data = recvall(sock,header_struct.size)
    (block_length,) = header_struct.unpack(block_length_data)
    print(block_length)
    #上面获取了数据长度的信息，这里就是根据数据长度来获取数据了
    return recvall(sock,block_length)

def put_block(sock,message):
    block_length = len(message)
    print(block_length)
    sock.send(header_struct.pack(block_length))
    sock.send(message)

def server(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(address)
    sock.listen(1)
    print('Run this script in another window with -C to continue.')
    print('Listening at ',sock.getsockname())
    sc ,sockname = sock.accept()
    print('Accepted connection from ',sockname)
    sc.shutdown(socket.SHUT_WR)
    while True:
        block = get_block(sc)
        if not block:
            break
        print('Block says:',repr(block))
    sc.close()
    sock.close()


def client(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock, b'11111111111111111111111')
    put_block(sock, b'22222222222222222222')
    put_block(sock, b'33333333333333333333333')
    put_block(sock, b'')
    sock.close()

if __name__ == '__main__':
    parser = ArgumentParser(description='Transmit & receive blocks over TCP')
    parser.add_argument('hostname',nargs='?',default='127.0.0.1',help='IP Address or Hostname (default 127.0.0.1)')
    parser.add_argument('-C',action='store_true',help='run as a client')
    parser.add_argument('-P',type=int,metavar='port',default=1060,help='TCP port default 1060')
    args = parser.parse_args()
    function = client if args.C else server
    function((args.hostname,args.P))
