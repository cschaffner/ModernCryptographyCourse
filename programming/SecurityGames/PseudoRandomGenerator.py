import nacl.secret
import nacl.utils


class PseudoRandomGenerator(object):
    """
    a pseudorandom generator: a deterministic function that is length-increasing
    """
    def l_out(self, n:int) -> int:
        """
        the output length of the PRG when a seed of length n is input
        :param n: length of seed
        :return: output length
        """
        n_out = n + 1  # e.g. stretching by a single bit
        assert n_out > n, 'PRG needs to be length-expanding'
        return n_out

    def evaluate(self, s: bytes) -> bytes:
        """
        evaluates the deterministic function on the seed s. Outputs a strictly longer string than the input seed.
        :param s: seed
        :return:  G(s)
        """
        output = s + b'0'  # come up with something better than this, that's definitely not a PRG
        assert len(output) == self.l_out(len(s))
        return output


class Distinguisher(object):
    """
    a distinguisher trying to figure out whether he's fed pure randomness or the output of a PRG
    """
    def distinguish(self, x: bytes) -> bool:
        """
        takes input x and tries to distinguish if it's sampled from pure randomness or output by a PRG
        :param x:
        :return: the distinguisher's guess
        """
        return True  # come up with something more clever than that


def PRG_IND(D: Distinguisher, G: PseudoRandomGenerator, n: int) -> bool:
    """
    The PRG indistinguishability game from Figure 2 in Week 2, Exercise 3.5 from [KL]:
    1. challenger C picks a bit b
    2. if b=0: C samples a fully random string r of length G.l_out(n) and sends r to D
       if b=1: C samples a uniform seed s of length n and sends G.evaluate(s) to D
    3. D returns a bit b' and wins if and only if b==b'

    :param D: the distinguisher
    :param G: the PRG
    :param n: security parameter, seed-length
    :return: a bit stating whether the D was successful
    """
    # 1. challenger C picks a bit b
    b = nacl.utils.random(1)

    # 2. if b=0: C samples a fully random string r of length G.l_out(n) and sends r to D
    #    if b=1: C samples a uniform seed s of length n and sends G.evaluate(s) to D
    if b == 0:
        r = nacl.utils.random(G.l_out(n))
        w = r
    elif b == 1:
        s = nacl.utils.random(n)
        w = G.evaluate(s)

    # 3. D returns a bit b_guess and wins if and only if b==b_guess
    b_guess = D(w)
    return b_guess == b


def test_distinguisher(D: Distinguisher, G: PseudoRandomGenerator, n: int, nr_runs: int) -> int:
    """
    tests how well D does when playing in the PRG indistinguishability security game by executing the game nr_runs times
    and taking statistics
    :param D: the distinguisher
    :param G: the PRG
    :param n: security parameter
    :param nr_runs: number of runs of the PRG_{D, G}(n) game
    :return: the number of wins
    """
    wins = 0
    for i in range(nr_runs):
        if PRG_IND(D, G, n):
            wins += 1

    print("out of {} runs, the adversary has won {}".format(nr_runs, wins))
    return wins


def compute_probability_difference(D: Distinguisher, G: PseudoRandomGenerator, n: int) -> float:
    """
    Def 3.14 [KL]: A PRG G is secure if no PPT distinguisher D can distinguish an output from G (with random seed) from
    a fully uniform output. Formally, we should have that
    | Pr_{s <- {0,1}^n} [ D( G(s) ) = 1 ] - Pr_{w <- {0,1}^G.l_out(n)} [ D(w) = 1 ] | < negl(n)

    For small parameters of n, we can brute-force compute these probabilities and output the absolute difference
    :param D: PRG distinguisher
    :param G: PRG
    :param n: security parameter
    :return: the absolute difference in probability
    """

    print("Computing ")

    l_out = G.l_out(n)
    assert l_out <= 14, 'for output lengths l_out larger than 14, the brute-force computation of the probabilities will take too long'

    # compute Pr_{s <- {0,1}^n} [ D( G(s) ) = 1 ]
    counter = 0
    for s in bitstrings(n):
        w = G.evaluate(s)
        if D(w):
            counter += 1
    pr_g = counter / (2 ** n)

    print("")

    # compute Pr_{w <- {0,1}^G.l_out(n)} [ D(w) = 1 ]
    counter = 0
    for w in bitstring(l_out):
        w = G.evaluate(s)
        if D(w):
            counter += 1
    pr_w = counter / (2 ** l_out)

    # output difference
    print("")
    return abs(count_g - count_w)
