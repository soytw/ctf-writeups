

# This file was *autogenerated* from the file coppersmith.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_128 = Integer(128); _sage_const_2020 = Integer(2020); _sage_const_3 = Integer(3); _sage_const_16 = Integer(16); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2)
import sys

def calc(c, nonce, n):
    P = PolynomialRing(Zmod(n), names=('x',)); (x,) = P._first_ngens(1)
    flag = b''
    for i in range(_sage_const_0 , len(c), _sage_const_128 ):
        nonce = (nonce + _sage_const_2020 ) % n
        cc = int.from_bytes(c[i:i+_sage_const_128 ], 'big')
        f = (cc - x) ** _sage_const_3  - nonce
        flag += int(f.monic().small_roots()[_sage_const_0 ]).to_bytes(_sage_const_16 , 'big')
    return flag

print(calc(bytes.fromhex(sys.argv[_sage_const_1 ]), int(sys.argv[_sage_const_2 ]), int(sys.argv[_sage_const_3 ])))

