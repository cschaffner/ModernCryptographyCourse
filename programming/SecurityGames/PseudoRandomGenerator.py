#

import nacl.secret
import nacl.utils


class PseudoRandomGenerator(object):
    """
    a pseudorandom generator: a deterministic function that is length-increasing
    """

    def evaluate(self, s: bytes) -> bytes:
        """
        evaluates the deterministic function on the seed s. Outputs a strictly longer string than the input seed.
        :param s: seed
        :return:  G(s)
        """
        output = s + b'0'  # come up with something better than this, that's definitely not a PRG
        assert len(s) < len(output)
        return output


