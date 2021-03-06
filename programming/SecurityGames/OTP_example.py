from PrivateKeyEncryption import PrivateKeyEncryption
import random
from bitstring import BitArray


class OTP(PrivateKeyEncryption):
    def Enc(self, k: BitArray, m: BitArray):
        # example OTP: c = bitwise XOR of message and key
        assert len(k) == len(m), "In case of the one-time pad, message and key have to be of the same length"
        return k ^ m

    def Dec(self, k, c):
        # example OTP: c = bitwise XOR of message and key
        assert len(k) == len(c), "In case of the one-time pad, ciphertext and key have to be of the same length"
        return k ^ c

class OTP_adversary(Adversary):
    def challenge_plaintexts(self, n: int):
        m_0 = '\x00'
        m_1 = '\x11'
        return m_0, m_1

    def guess_bit(self, c):
        # ignore the ciphertext and return a random bit
        b_guess = random.randrange(0, 1)
        return b_guess


otp = OTP()
m = b"The president"
key = otp.KeyGen(len(m))
c = otp.Enc(key, b"The president")
print(otp.Dec(key, c))
