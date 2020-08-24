import random
from math import gcd, sqrt
from tqdm import tqdm

def F(x: int, N: int) -> int:
    return x**2 + 1 % N

def PollardsRho(N: int) -> int:
    """
    Pollards rho algorithm

    """
    x = random.randint(1, N-1)
    xp = x
    i=1
    for i in tqdm(range(int(sqrt(N)))):
        x = F(x, N)
        xp = F(F(xp, N), N)
        p = gcd(x-xp, N)
        if not p in [1, N]:
            return p
        i += 1

print(PollardsRho(52343523))
