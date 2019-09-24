import nacl.secret
import nacl.utils
from bitstring import BitArray

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

    def Enc(self, k: BitArray, m: BitArray) -> BitArray:
        """
        encrypts message m with key k
        :param k: the secret key k
        :param m: the message to be encrypted
        :return: the ciphertext
        """
        pass

    def Dec(self, k: BitArray, c: BitArray) -> BitArray:
        """
        decrypts ciphertext c with key k
        :param k: secret key
        :param c: ciphertext
        :return: decrypted message
        """
        pass


class Adversary(object):
    """
    adversary playing in the PrivK game
    """
    def challenge_plaintexts(self, n: int):
        """
        The first part of the adversary receives the security parameter n and returns two challenge plaintexts
        of the same length
        :param n: security parameter
        :return: (m1, m2) two challenge plaintexts of the same length
        """
        pass

    def guess_bit(self, c: BitArray) -> int:
        """
        The second part of the adversary receives the challenge ciphertext from the challenger and has to guess which
        of its two challenge plaintexts was encrypted
        :param c:
        :return:
        """
        pass


def PrivK(Pi: PrivateKeyEncryption, Adv: Adversary, n: int) -> bool:
    """
    Private-key security game played between a challenger and adversary
    1. Adv is given the security parameter and comes up with two challenge plaintexts m_0 and m_1
    2. Challenger generates a new secret key and picks a random bit b
    3. Chall encrypts message m_b into challenge ciphertext c
    4. Based on c, Adv has to guess the bit b in order to win the game

    :param Pi: private-key encryption scheme
    :param A: adversary
    :param n: security parameter
    :return: a Boolean value whether the Adversary has won the game or not
    """

    # 1. Adv is given the security parameter and comes up with two challenge plaintexts m_0 and m_1
    m_0, m_1 = Adv.challenge_plaintexts(n)

    # 2. Challenger generates a new secret key and picks a random bit b
    key = Pi.KeyGen(n)
    b = nacl.utils.random(1)

    # 3. Chall encrypts message m_b into challenge ciphertext c
    if b == 0:
        c = Pi.Enc(key, m_0)
    elif b == 1:
        c = Pi.Enc(key, m_1)

    # 4. Based on c, Adv has to guess the bit b in order to win the game
    b_guess = Adv.guess_bit(c)

    return b == b_guess


def test_adversary(Pi: PrivateKeyEncryption, Adv: Adversary, n: int, nr_runs: int) -> int:
    """
    tests how well Adv does when playing in the PrivK security game by executing the game nr_runs times
    and taking statistics
    :param Pi: private-key encryption scheme
    :param A: adversary
    :param n: security parameter
    :param nr_runs: number of runs of the PrivK_{Pi, Adv}(1^n) game
    :return: the number of wins
    """
    wins = 0
    for i in range(nr_runs):
        if PrivK(Pi, Adv, n):
            wins += 1

    print("out of {} runs, the adversary has won {}".format(nr_runs, wins))
    return wins

