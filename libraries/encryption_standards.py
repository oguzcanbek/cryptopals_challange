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
        
     
    def pad_text(self, blocksize):
        obj_bits = len(self.value)
        while obj_bits % blocksize != 0:
            self.value += "0"
            obj_bits = len(self.value)
    
    # Electronic Code Book encryption
    def encrypt_ECB(self, key):
        
        # In bits
        blocksize = 128
        # Convert the message value to base 2
        self.Base2()
        # Pad the text if necessary for the blocksize
        pad_text(blocksize)
        
        # Divide the plaintext into blocksize sized block (küül)
        number_of_blocks = int(len(self.value)/blocksize)
        blocks = [crypto.Crypto(ciphertext=self.value[i*blocksize:(i+1)*blocksize], base=2) for i in range(number_of_blocks)]

        
        