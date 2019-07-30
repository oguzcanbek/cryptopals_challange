from libraries import numeral
from libraries import crypto

import re
import binascii
import numpy as np
from string import printable
from string import ascii_letters


letterset = printable


class Encrypto(crypto.Crypto):
    
    def __init(self):
        super().__init__()
        