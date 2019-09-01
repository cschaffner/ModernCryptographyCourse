# Python 2 / 3
# author: Christian Schaffner
from random import randint

KEY_LENGTH = 80
KEY = ['{0:02x}'.format(randint(0,255)) for x in range(KEY_LENGTH)]

"""
useful python commands:

    ord(c) -> integer
    Return the integer ordinal of a one-character string.
    Example: ord('d') == 100

    chr(i) -> character    
    Return a string of one character with ordinal i; 0 <= i < 256.
    Example: chr(100) == 'd'

    int(x, base=16) -> int or long        
    Converts hexadecimal string x to an integer
    Example:  int('7b', 16) == 123

    '{0:02x}'.format(integer)
    returns the hexadecimal representation (at least two characters) of an integer
    Example: '{0:02x}'.format(123)  ==  '7b'

    '{0:08b}'.format(integer)
    returns the binary representation (at least 8 characters) of an integer
    Example: '{0:08b}'.format(23) == '00010111'

    x.__xor__(y) <==> x^y   
    bitwise XOR of x and y
    Example: 23 ^ 156 == 139 , because  00010111 XOR 10011100 == 10001011
"""


def main():
    fout = open('ciphertexts.txt', 'w')
    for line in  open('messages.txt', 'r'):
        ciphertext = ''
        pos = 0
        for char in line.rstrip('\n'): # ignore the \n character at the end of the line if it's there
            ciphertext += '{0:02x}'.format((int(ord(char)) ^ int(KEY[pos], 16)))
            pos += 1
        fout.write('{}\n'.format(ciphertext))

    fout.close()
    print(KEY)
    return True


if __name__ == "__main__":
    main()
