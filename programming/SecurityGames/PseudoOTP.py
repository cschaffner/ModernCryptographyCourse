from PseudoRandomGenerator import PseudoRandomGenerator, Distinguisher, compute_probability_difference, test_distinguisher
from bitstring import BitArray
import random

class PRG(PseudoRandomGenerator):
    '''
    uses the python internal random PRG, probably a good one
    '''
    def l_out(self, n: int) -> int:
        return 2*n

    def evaluate(self, s: BitArray) -> BitArray:
        random.seed(a=s.uint)  # sets the seed to the given seed
        return BitArray(uint=random.getrandbits(2*n), length=2*n)


class PRG_Dist(Distinguisher):
    '''
    distinguisher against G(s) = s || s
    '''
    def distinguish(self, x: BitArray) -> bool:
        '''
        takes input x and tries to distinguish if it's sampled from pure randomness or output by a PRG
        :param x:
        :return: the distinguisher's guess
        '''

        # TODO: do something more clever here!
        return True


def Dist(x: BitArray) -> bool:
    n = len(x)
    assert n % 2 == 0, 'input length should be even'
    return x[0] == x[int(n/2)]


def D_const(x: BitArray) -> bool:
    return True


def D_bruteforce(x: BitArray) -> bool:
    n = int(len(x) / 2)
    prg = PRG()
    for s in range(0, 2**n):
        if prg.evaluate(BitArray(uint=s, length=n)) == x:
            return True
    return False

prg = PRG()
dist = PRG_Dist()

n = 5
probability_difference = compute_probability_difference(D_bruteforce, prg, n)
# assert probability_difference >= 1 - (2 ** n)

#test_distinguisher(Dist, prg, 8, 10000)


