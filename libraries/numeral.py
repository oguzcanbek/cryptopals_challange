import numpy as np

class Numeral():
    
    
    def __init__(self, value ="0", base=2):
        self.value = value
        self.base = base
       
    
    def setValue(self, value):
        self.value = value
       
    
    def getValue(self):
        print(self.value)
        
    
    # Convert a decimal digit to 4-bit binary representation
    def decimalDigitToBinary(self, decimal):
        binary_dict = {
            "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
            "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001"
        }
        return binary_dict[decimal]
        
        
    # Convert a decimal digit to a hexadecimal digit
    def decimalDigitToHex(self, decimal):
        hexadecimal_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                            "a", "b", "c", "d", "e", "f"]
        return hexadecimal_list[int(decimal)]
        
    
    # Convert a hexadecimal digit to 4-bit binary representation
    def hexDigitToBinary(self, hexadecimal):
        binary_dict = {
            "0": "0000", "1": "0001", "2": "0010", "3": "0011",
            "4": "0100", "5": "0101", "6": "0110", "7": "0111",
            "8": "1000", "9": "1001", "a": "1010", "b": "1011", 
            "c": "1100", "d": "1101", "e": "1110", "f": "1111"
        }
        return binary_dict[hexadecimal]
    
    
    # Convert a decimal number to a Base64 digit
    def base64Digit(self, index):
        base_64_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
                        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"]
        return base_64_list[int(index)]
    
    
    # Pad the binary number until it becomes an integer multiple of 6
    def padding(self, binary):
        reversed_binary = binary[::-1]
        while (len(reversed_binary) % 6) != 0:
            reversed_binary += "0"
        return reversed_binary[::-1]

    
    # Convert a hexadecimal digit to a decimal digit
    def hexDigitToDecimal(self, hexadecimal):
        hexadecimal_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                            "a", "b", "c", "d", "e", "f"]
        return hexadecimal_list.index(hexadecimal)     
        
    
    # Convert a Base64 digit to decimal
    def base64DigitToDecimal(self, base64):
        base_64_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
                        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"]
        return base_64_list.index(base64)
    
    
    # Convert a binary string to decimal
    def binaryToDecimal(self,binary):
        decimal = 0
        for exponent, bit in enumerate(binary[::-1]):
            decimal += int(bit) * (np.power(2, exponent))
        return str(decimal)
    
    
    # Convert a binary string to hexadecimal
    def binaryToHex(self, binary):        
        hexadecimal = ""        
        binary = binary[::-1]
        
        nibbles = [binary[i:i+4] for i in range(0, len(binary), 4)]
        for nibble in nibbles:
            decimal_nibble = self.binaryToDecimal(nibble[::-1])
            hexadecimal = self.decimalDigitToHex(decimal_nibble) + hexadecimal   
        return hexadecimal
    
    
    # Convert a binary string to Base64
    def binaryToBase64(self, binary):
        base64 = ""
        padded_binary = self.padding(binary)
        padded_binary = padded_binary[::-1]
        
        six_bits = [padded_binary[i:i+6] for i in range(0, len(padded_binary), 6)]
        for six_bit in six_bits:
            decimal_six_bit = self.binaryToDecimal(six_bit[::-1])
            base64 = self.base64Digit(decimal_six_bit) + base64
        return base64
    
    
    # Convert a decimal string to binary
    def decimalToBinary(self, decimal):
        binary = ""
        if int(decimal) == 0:
            binary = "0"
        quotient = int(decimal)
        while (quotient != 0):
            quotient, remainder = np.divmod(quotient, 2)
            binary += str(remainder)
        return binary[::-1]
    
    
    # Convert a hexadecimal string to binary
    def hexToBinary(self, hexadecimal):
        binary = ""
        for digit in hexadecimal:
            binary += self.hexDigitToBinary(digit)
        return binary 
    
    
    # Convert a hexadecimal string to binary
    def base64ToBinary(self, base64):
        binary = ""
        for digit in base64:
            decimal_digit = self.base64DigitToDecimal(digit)
            binary_digit = self.decimalToBinary(decimal_digit)
            binary += self.padding(binary_digit)
        return binary 
    
    
    def Base2(self, isPrint=False):
        if self.base == 10:
            self.value = self.decimalToBinary(self.value)
        elif self.base == 16:
            self.value = self.hexToBinary(self.value)
        elif self.base == 64:
            self.value = self.base64ToBinary(self.value)
        self.base = 2
        if isPrint:
            print(self.value)
    
    
    def Base10(self, isPrint=False):
        if self.base == 16:
            self.value = self.hexToBinary(self.value)
        elif self.base == 64:
            self.value = self.base64ToBinary(self.value)
#         elif self.base == 10:
#             return
        self.value = self.binaryToDecimal(self.value)
        self.base = 10
        if isPrint:
            print(self.value)

    
    def Base16(self, isPrint=False):
        if self.base == 10:
            self.value = self.decimalToBinary(self.value)
        elif self.base == 64:
            self.value = self.base64ToBinary(self.value)
#         elif self.base == 16:
#             return
        self.value = self.binaryToHex(self.value)
        self.base = 16
        if isPrint:
            print(self.value)
        
    
    def Base64(self, isPrint=False):
        if self.base == 10:
            self.value = self.decimalToBinary(self.value)
        elif self.base == 16:
            self.value = self.hexToBinary(self.value)
#         elif self.base == 64:
#             return
        self.value = self.binaryToBase64(self.value)
        self.base = 64
        if isPrint:
            print(self.value)
