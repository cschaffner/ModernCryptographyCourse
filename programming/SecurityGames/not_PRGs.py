from PseudoRandomGenerator import PseudoRandomGenerator, Distinguisher, compute_probability_difference
from bitstring import BitArray

class PRG(PseudoRandomGenerator):
    '''
    G(s) = s || s
    outputs the seed concatenated with itself
    this is not a PRG, why not?
    '''
    def l_out(self, n:int) -> int:
        return 2*n

    def evaluate(self, s: BitArray) -> bytes:
        return s + s

class PRG_Dist(Distinguisher):
    '''
    distinguisher against G(s) = s || s
    '''
    def distinguish(self, x: bytes) -> bool:
        '''
        takes input x and tries to distinguish if it's sampled from pure randomness or output by a PRG
        :param x:
        :return: the distinguisher's guess
        '''

        # TODO: do something more clever here!
        return True

not_a_PRG_1 = PRG()
not_a_PRG_Dist = PRG_Dist()

n = 10
probability_difference = compute_probability_difference(not_a_PRG_Dist, not_a_PRG_1, n)
print("")
assert probability_difference >= 1 - (2 ** n)


