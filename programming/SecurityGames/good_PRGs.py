from PseudoRandomGenerator import PseudoRandomGenerator, Distinguisher, compute_probability_difference, test_distinguisher
from bitstring import BitArray


class PRG(PseudoRandomGenerator):
    '''
    G(s) = s || s
    outputs the seed concatenated with itself
    this is not a PRG, why not?
    '''
    def l_out(self, n: int) -> int:
        return 2*n

    def evaluate(self, s: BitArray) -> BitArray:
        return s + s


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

prg = PRG()
dist = PRG_Dist()

n = 8
# probability_difference = compute_probability_difference(Dist, prg, n)
# assert probability_difference >= 1 - (2 ** n)

test_distinguisher(D_const, prg, 10, 10000)


