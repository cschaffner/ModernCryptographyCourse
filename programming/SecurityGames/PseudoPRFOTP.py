from PseudoRandomGenerator import PseudoRandomGenerator, Distinguisher, compute_probability_difference, test_distinguisher
from PrivateKeyEncryption import PrivateKeyEncryption, Adversary
from bitstring import Bits
from typing import Tuple
import random
import secrets

class Good_PRG(PseudoRandomGenerator):
    '''
    uses the python internal random PRG, probably a good one
    '''
    def l_out(self, n: int) -> int:
        return 2*n

    def evaluate(self, s: Bits) -> Bits:
        random.seed(a=s.uint)  # sets the seed to the given seed
        return Bits(uint=random.getrandbits(2*n), length=2*n)


class Bad_PRG(PseudoRandomGenerator):
    '''
    G(s) = s || s
    outputs the seed concatenated with itself
    this is not a PRG, why not?
    '''
    def l_out(self, n: int) -> int:
        return 2*n

    def evaluate(self, s: Bits) -> Bits:
        return s + s



class PseudoOTP(PrivateKeyEncryption):
    '''
    the pseudo-OTP based on PRG G
    KeyGen: pick a n-bit key at random
    Enc(m) = m XOR G(k)
    Dec(c) = c XOR G(k)
    '''
    def __init__(self, G: PseudoRandomGenerator):
        self.G = G

    def Enc(self, k: Bits, m: Bits) -> Bits:
        '''
        :param k: key
        :param m: plaintext of length G.l_out(len(k))
        :param G: PRG
        :return: ciphertext
        '''
        assert len(m) == self.G.l_out(len(k)), 'message length not equal to output length of PRG evaluated on key'
        return m ^ self.G.evaluate(k)

    def Dec(self, k: Bits, c: Bits) -> Bits:
        '''

        :param k: key
        :param c: ciphertext
        :param G: PRG
        :return: plaintext
        '''
        assert len(c) == self.G.l_out(len(k)), 'ciphertext length not equal to output length of PRG evaluated on key'
        return c ^ self.G.evaluate(k)


def DistFromAdv(Adv: Adversary, w: Bits, n: int) -> bool:
    '''
    Given a successful attacker of the PseudoOTP scheme, we define a successful distinguisher of the PRG
    :param Adv: a PrivK attacker on the PseudoOTP scheme with PRG G
    :param w: input to the PRG
    :param n: security parameter
    :return: the distinguisher's output bit
    '''
    # we play the PrivK game towards the adversary

    # 1. Adv is given the security parameter and comes up with two challenge plaintexts m_0 and m_1
    m_0, m_1 = Adv.challenge_plaintexts(n)

    # 2. Challenger generates a new secret key and picks a random bit b
    b = secrets.randbelow(2)

    # 3. Instead of encrypting, we pad the message m_b with w
    if b == 0:
        c = m_0 ^ w
    elif b == 1:
        c = m_1 ^ w

    # 4. Based on c, Adv has to guess the bit b in order to win the game
    b_guess = Adv.guess_bit(c)

    return b == b_guess



bad_PRG = Bad_PRG()
good_PRG = Good_PRG()

bad_potp = PseudoOTP(bad_PRG)
good_potp = PseudoOTP(good_PRG)

n = 5


# probability_difference = compute_probability_difference(D_bruteforce, prg, n)
# assert probability_difference >= 1 - (2 ** n)

#test_distinguisher(Dist, prg, 8, 10000)


