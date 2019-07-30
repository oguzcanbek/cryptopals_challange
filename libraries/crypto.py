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
from string import ascii_letters


letterset = printable


class Crypto(numeral.Numeral):
    
    encoding = 'ISO-8859-1'
    
#     encoding = 'utf-8' 
    
    def __init__(self, plaintext=None, ciphertext=None, base=16):
        
        if plaintext is None:
            self.plaintext = ""
        else:
            self.plaintext = plaintext
            self.value = Crypto.ASCIIToHex(self.plaintext)
            self.base = 16
            
        if ciphertext is None:
            self.ciphertext = ""
        else:
            self.ciphertext = ciphertext
            self.value = ciphertext
            self.base = base
        
          
    def encodeSingleByteXOR(self, key_value):
        
        text_len = len(self.plaintext)
        
        key = numeral.Numeral(base=16)
        dummy_key = ""
        for i in range(text_len):
            dummy_key += key_value
        key.value = dummy_key
        
        key.value = Crypto.ASCIIToHex(key.value)
        key.value = Crypto.XOR(self, key)
        key.Base16()        
        result = key.value
        self.ciphertext = result
        
        return result
    
    
    def decodeSingleByteXOR(self, key_value):
        
        text_len = len(self.ciphertext)
        
        key = numeral.Numeral(base=16)
        dummy_key = ""
        for i in range(text_len):
            dummy_key += key_value
        key.value = dummy_key
        
        key.value = Crypto.ASCIIToHex(key.value)
        key.value = Crypto.XOR(self, key)
        key.Base16()        
        result = Crypto.toASCII(key.value)
        self.plaintext = result
        
        return result
    
    
    def encodeRepeatingByteXOR(self, key_value):
        
        text_len = len(self.plaintext)
        key_len = len(key_value)
        repeat_len = int(text_len/key_len) + 1
        key = numeral.Numeral(base=16)
        dummy_key = ""        
        for i in range(repeat_len):
            dummy_key += key_value
        dummy_key = dummy_key[:text_len]
        key.value = dummy_key
        key.value = Crypto.ASCIIToHex(key.value)
        
        key.value = Crypto.XOR(self, key)
        key.Base16()        
        self.ciphertext = key.value
        
        return self.ciphertext
    
    
    def decodeRepeatingByteXOR(self, key_value):
        
        text_len = len(self.ciphertext)
        key_len = len(key_value)
        repeat_len = int(text_len/key_len) + 1
        
        key = numeral.Numeral(base=16)
        dummy_key = ""
        for i in range(repeat_len):
            dummy_key += key_value
        dummy_key = dummy_key[:text_len]
        key.value = dummy_key
        key.value = Crypto.ASCIIToHex(key.value)
        
        key.value = Crypto.XOR(self, key)
        key.Base16()        
        result = Crypto.toASCII(key.value)
        self.plaintext = result
        
        return self.plaintext
    
    
    def findCipherLetterFrequencyScore(self):
        score_array = np.zeros(len(letterset))

        for idx, letter in enumerate(letterset):
            result = self.decodeSingleByteXOR(letter)
            pretty_result = re.sub(r'[\x00-\x1F]+', '', result)
            score_array[idx] = Crypto.evaluateString(pretty_result)
        
        return score_array
    
    
    def decipherSingleByteXOR(self, print_sln=False, N=1):
        
        score_array = self.findCipherLetterFrequencyScore()
        
        # Find the first N letters with the greates score
        max_letters_idx = np.array(score_array).argsort()[-N:][::-1]
        
        for i in range(N):
            letter = letterset[max_letters_idx[i]]
            solution = self.decodeSingleByteXOR(letter)
            pretty_solution = re.sub(r'[\x00-\x1F]+', '', solution)
            if print_sln:
                print("Key: ", letter, " / Solution: ", pretty_solution)
        
        return score_array, letter
    
    
    def findHammingDistance(self, key_text):
        
        key = numeral.Numeral(base=16)
        key.value = Crypto.ASCIIToHex(key_text)
        key.Base2()
        print(key.value)
        comparison = Crypto.XOR(self, key)
        distance = 0
        for bit in comparison:
            if int(bit) == 1:
                distance += 1
    
        return distance
    
    
    def findKeysize(self):
        
        self.Base2()
        binarytext = self.value
        keysize = 2
        keysize_range = 40
        score_array = np.zeros(keysize_range)
        for i in range(keysize_range):
            keysize_score = Crypto.findKeysizeScore(keysize, binarytext, pad=True, average=True)
            score_array[i] = keysize_score
            keysize += 1        
        
        return score_array
    
    
    @staticmethod    
    def toASCII(string_text):
        try:
            ASCII_str = bytearray.fromhex(string_text).decode(Crypto.encoding)
        except ValueError:
            string_text = string_text[1:]
            ASCII_str = bytearray.fromhex(string_text).decode(Crypto.encoding)
#         self.plaintext = ASCII_str
        return ASCII_str
    
    
    @staticmethod
    def ASCIIToHex(string_text):
#         hexadecimal = string.value
        hexadecimal = binascii.hexlify(bytes(string_text, Crypto.encoding))
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
        
        key = numeral.Numeral(base=16)
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
        
        key = numeral.Numeral(base=16)
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
        

#         eng_letter_frq = {"a": "248362256", "b": "47673928", "c": "79962026", "d": "134044565", "e": "390395169", "f": "72967175",
#                           "g": "61549736", "h": "193607737", "i": "214822972", "j": "4507165", "k": "22969448", "l": "125951672",
#                           "m": "79502870", "n": "214319386", "o": "235661502", "p": "55746578", "q": "3649838", "r": "184990759",
#                           "s": "196844692", "t": "282039486", "u": "88219598", "v": "30476191", "w": "69069021", "x": "5574077",
#                           "y": "59010696", "z": "2456495", " ": "600000000"}
        
        eng_letter_frq = {"a": "0.08167", "b": "0.01492", "c": "0.02782", "d": "0.04253", "e": "0.12702", "f": "0.02228",
                          "g": "0.02015", "h": "0.06094", "i": "0.06966", "j": "0.00153", "k": "0.00772", "l": "0.04025",
                          "m": "0.02406", "n": "0.06749", "o": "0.07507", "p": "0.01929", "q": "0.00095", "r": "0.05987",
                          "s": "0.06327", "t": "0.09056", "u": "0.02758", "v": "0.00978", "w": "0.02360", "x": "0.00150",
                          "y": "0.01974", "z": "0.00074", " ": "0.12000"}
        
        score = 0
        for char in string:
            char = char.lower()
            try:
                score += float(eng_letter_frq[char])
            except:
                score -= 0
                
        return score
    
    
    @staticmethod
    def findKeysizeScore(keysize, binarytext, pad=False, average=False):
        
        binarytext_len = len(binarytext)
        byte_len = 8 * keysize  
        if pad:
            # Add 0's to the and of the data so that it is evenly divisible to KEYSIZE bytes
            remainder = binarytext_len % byte_len
            for i in range(abs(byte_len - remainder)):
                binarytext += "0"
            binarytext_len = len(binarytext)
    #         print(binarytext_len)
    #         print("***")
        
        iteration_no = int(binarytext_len / byte_len)
        
        n_loop = 3
        if average:
            n_loop = iteration_no
        
        total_distance = 0
        # Check every KEYSIZE step
        for i in range(n_loop):       
            first_chunk  = binarytext[(i*byte_len):(i+1)*byte_len]
            second_chunk = binarytext[(i+1)*byte_len:(i+2)*byte_len]
            str_1 = numeral.Numeral(value=first_chunk)
            str_2 = numeral.Numeral(value=second_chunk)

            comparison = Crypto.XOR(str_1, str_2)

            distance = 0
            for bit in comparison:
                if int(bit) == 1:
                    distance += 1
                    
            total_distance += distance
        
        if average:
            total_distance = total_distance / iteration_no

        return total_distance/keysize

    

