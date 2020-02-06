

# This file was *autogenerated* from the file exp.sage
from sage.all_cmdline import *   # import sage library

_sage_const_100 = Integer(100); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_1024 = Integer(1024); _sage_const_10000 = Integer(10000); _sage_const_2 = Integer(2); _sage_const_32 = Integer(32); _sage_const_1812433253 = Integer(1812433253); _sage_const_624 = Integer(624); _sage_const_397 = Integer(397); _sage_const_31 = Integer(31); _sage_const_0x9908b0df = Integer(0x9908b0df); _sage_const_11 = Integer(11); _sage_const_0xffffffff = Integer(0xffffffff); _sage_const_7 = Integer(7); _sage_const_0x9d2c5680 = Integer(0x9d2c5680); _sage_const_15 = Integer(15); _sage_const_0xefc60000 = Integer(0xefc60000); _sage_const_18 = Integer(18); _sage_const_39091 = Integer(39091); _sage_const_100000 = Integer(100000)
import os
import socket
import logging

class remote:
    def __init__(self, host, port, timeout=_sage_const_100 ):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((host, port))
        logging.info('connected')
        self.buffer = b''
    def interactive(self):
        os.dup2(self.s.fileno(), _sage_const_0 )
        os.dup2(self.s.fileno(), _sage_const_1 )
    def recvuntil(self, text):
        text = self._convert_to_bytes(text)
        while text not in self.buffer:
            self.buffer += self.s.recv(_sage_const_1024 )
        index = self.buffer.find(text) + len(text)
        result, self.buffer = self.buffer[:index], self.buffer[index:]
        logging.debug('received:')
        logging.debug(result)
        return result
    def recvline(self):
        return self.recvuntil(b'\n')
    def recv(self, n=_sage_const_10000 ):
        result = self.s.recv(n)
        logging.debug('received:')
        logging.debug(result)
        return result
    def recvlines(self, n):
        lines = []
        for _ in range(n):
            lines.append(self.recvline())
        return lines
    def _convert_to_bytes(self, text):
        if type(text) is not bytes:
            text = str(text)
        if type(text) is str:
            text = text.encode()
        return text
    def send(self, text):
        text = self._convert_to_bytes(text)
        self.s.sendall(text)
        logging.debug('sent:')
        logging.debug(text)
    def sendline(self, text):
        text = self._convert_to_bytes(text)
        self.send(text + b'\n')
    def sendafter(self, prefix, text):
        self.recvuntil(prefix)
        self.send(text)
    def sendlineafter(self, prefix, text):
        self.recvuntil(prefix)
        self.sendline(text)

logging.basicConfig(level='DEBUG')

Z2 = GF(_sage_const_2 )
Z32 = GF(_sage_const_2 **_sage_const_32 )
VS32 = GF(_sage_const_2 )**_sage_const_32 

self_f = _sage_const_1812433253 
(self_w, self_n, self_m, self_r) = (_sage_const_32 , _sage_const_624 , _sage_const_397 , _sage_const_31 )
self_a = _sage_const_0x9908b0df 
(self_u, self_d) = (_sage_const_11 , _sage_const_0xffffffff )
(self_s, self_b) = (_sage_const_7 , _sage_const_0x9d2c5680 )
(self_t, self_c) = (_sage_const_15 , _sage_const_0xefc60000 )
self_l = _sage_const_18 
self_lower_mask = (_sage_const_1  << self_r) - _sage_const_1 
self_upper_mask = (_sage_const_1  << self_r)

def rand(x):
    y = x
    y = y ^ ((y >> self_u) & self_d)
    y = y ^ ((y << self_s) & self_b)
    y = y ^ ((y << self_t) & self_c)
    y = y ^ (y >> self_l)
    return y & _sage_const_0xffffffff 

def unrand(y):
    RR = rand_mat_repr().inverse()
    y = Z32.fetch_int(y)
    x = Z32(RR * vector(y))
    return x.integer_representation()

def rand_mat_repr():
    RR = matrix(Z2, _sage_const_32 , _sage_const_32 )
    g = Z32.gen()

    for i in range(_sage_const_32 ):
        y = (g**i).integer_representation()
        y = y ^ ((y >> self_u) & self_d)
        y = y ^ ((y << self_s) & self_b)
        y = y ^ ((y << self_t) & self_c)
        y = y ^ (y >> self_l)

        RR[:,i] = vector(Z32.fetch_int(y))
    return RR

def twist(state0, state1, state397):
    x = state0 & self_upper_mask
    x += state1 & self_lower_mask
    xA = x >> _sage_const_1 
    if x % _sage_const_2  != _sage_const_0 :
        xA ^= self_a
    state0 = state397 ^ xA
    return state0

r = remote('eof.ais3.org', _sage_const_39091 , timeout=_sage_const_1 )
#  r = remote('localhost', 1234, timeout=1)

r.sendlineafter('> ', '1')
r.sendlineafter('> ', '8787878')
r.recvuntil('Lucky Number: ')
state1 = unrand(int(r.recvline()))

r.sendlineafter('> ', '395')
r.sendlineafter('> ', '8787878')
r.recvuntil('Lucky Number: ')
state397 = unrand(int(r.recvline()))

state0 = twist(_sage_const_0 , state1, state397)
print('state[0,1,397] =',state0,state1,state397)

r.sendlineafter('> ', '226')
r.sendlineafter('> ', str(rand(state0)))

print(r.recv(_sage_const_100000 ))
print(r.recv(_sage_const_100000 ))

