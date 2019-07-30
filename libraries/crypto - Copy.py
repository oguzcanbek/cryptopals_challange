import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from libraries import numeral

import re
import binascii
import numpy as np
from string import printable



class Crypto(numeral.Numeral):
    
    encoding = 'ISO-8859-1'    
    
    def __init__(self, base=2):
        self.value = "0"
        self.base = base
        
        
    @staticmethod
    def toASCII(string):
        ASCII_str = bytearray.fromhex(string.value).decode(Crypto.encoding)
        return ASCII_str
    
    
    @staticmethod
    def ASCIIToHex(string):
#         hexadecimal = string.value
        hexadecimal = binascii.hexlify(bytes(string.value, Crypto.encoding))
        return hexadecimal.decode(Crypto.encoding) 
    
    
    @staticmethod
    def XOR(str_1, str_2):
        str_1.Base2()
        str_2.Base2()
        xor = ""
        for a, b in zip(str_1.value, str_2.value):
            sol = int(a) ^ int(b)
            xor += str(sol)
        str_1.Base16()
        str_2.Base16()
        return xor
    
    
    @staticmethod
    def singleByteXOR(string, key_value):
        
        ASCII_string = Crypto.toASCII(string)
        ASCII_len = len(ASCII_string)
        
        key = numeral.Numeral(16)
        dummy_key = ""
        
        for i in range(ASCII_len):
            dummy_key += key_value
        key.value = dummy_key
        key.value = Crypto.ASCIIToHex(key)
        
        key.value = Crypto.XOR(string, key)
        key.Base16()
        
        result = Crypto.toASCII(key)
        
        return result
    
    
    @staticmethod
    def repeatingByteXOR(string, key_value):
        
        ASCII_string = Crypto.toASCII(string)
        ASCII_len = len(ASCII_string)
        
        key = numeral.Numeral(16)
        dummy_key = ""
        
        for i in range(ASCII_len):
            dummy_key += key_value
        key.value = dummy_key
        key.value = Crypto.ASCIIToHex(key)
        
        key.value = Crypto.XOR(string, key)
        key.Base16()
        
#         result = Crypto.toASCII(key)
        
        return key # instead of result
        
    
    @staticmethod
    def evaluateString(string):
        

        eng_letter_frq = {"a": "248362256", "b": "47673928", "c": "79962026", "d": "134044565", "e": "390395169", "f": "72967175",
                          "g": "61549736", "h": "193607737", "i": "214822972", "j": "4507165", "k": "22969448", "l": "125951672",
                          "m": "79502870", "n": "214319386", "o": "235661502", "p": "55746578", "q": "3649838", "r": "184990759",
                          "s": "196844692", "t": "282039486", "u": "88219598", "v": "30476191", "w": "69069021", "x": "5574077",
                          "y": "59010696", "z": "2456495", " ": "700000000"}
        
#         eng_letter_frq = {"a": "0.08167", "b": "0.01492", "c": "0.02782", "d": "0.04253", "e": "0.12702", "f": "0.02228",
#                           "g": "0.02015", "h": "0.06094", "i": "0.06966", "j": "0.00153", "k": "0.00772", "l": "0.04025",
#                           "m": "0.02406", "n": "0.06749", "o": "0.07507", "p": "0.01929", "q": "0.00095", "r": "0.05987",
#                           "s": "0.06327", "t": "0.09056", "u": "0.02758", "v": "0.00978", "w": "0.02360", "x": "0.00150",
#                           "y": "0.01974", "z": "0.00074"}
        
        score = 0
        for char in string:
            char = char.lower()
            try:
                score += float(eng_letter_frq[char])
            except:
                score -= 0
                
        return score
    
    
    @staticmethod
    def findCipherLetterFrequencyScore(string):
        score_array = np.zeros(len(printable))

        for idx, letter in enumerate(printable):
            result = Crypto.singleByteXOR(string, letter)
            pretty_result = re.sub(r'[\x00-\x1F]+', '', result)
#             print(result)
#             print(pretty_result)
            score_array[idx] = Crypto.evaluateString(pretty_result)
        
        return score_array
    
    
    @staticmethod
    def decipherSingleByteXOR(string, print_sln=False):
        score_array = Crypto.findCipherLetterFrequencyScore(string)
        
        # Find the first N letters with the greates score
        N = 3
        max_letters_idx = np.array(score_array).argsort()[-N:][::-1]
        
        for i in range(N):
            letter = printable[max_letters_idx[i]]
            solution = Crypto.singleByteXOR(string, letter)
            pretty_solution = re.sub(r'[\x00-\x1F]+', '', solution)
            if print_sln:
                print("Key: ", letter, " / Solution: ", pretty_solution)
        
        return score_array
