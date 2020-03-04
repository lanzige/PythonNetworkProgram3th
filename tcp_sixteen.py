#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import socket,dns.resolver,argparse

def LookUp(name):
    for qtype in 'A','AAAA','CNAME','MX','NS':
        answer = dns.resolver.query(name,qtype,raise_on_no_answer=False)
        if answer.rrset is not None:
            print(answer.rrset)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Resolve a name using DNS')
    parse.add_argument('name',help='name that you want to lookup in DNS')
    LookUp(parse.parse_args().name)

