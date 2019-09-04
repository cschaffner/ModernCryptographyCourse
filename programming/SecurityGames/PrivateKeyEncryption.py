import nacl.secret
import nacl.utils

class PrivateKeyEncryption(object):
    """
    A private-key encryption scheme
    """
    def KeyGen(self, n: int):
        """
        returns a secret key of n bits
        :param n: security parameter
        :return: secret key of bit-length n
        """
        key = nacl.utils.random(n)
        return key

    def Enc(self, k, m):
        """
        encrypts message m with key k
        :param k: the secret key k
        :param m: the message to be encrypted
        :return: the ciphertext
        """
        pass

    def Dec(self, k, c):
        """
        decrypts ciphertext c with key k
        :param k: secret key
        :param c: ciphertext
        :return: decrypted message
        """
        pass

