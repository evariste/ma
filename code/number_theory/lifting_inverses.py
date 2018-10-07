

from sympy.ntheory.primetest import isprime
from sympy.core.numbers import igcd

import numpy as np

def inv_mod_p_brute_force(x, p):


    if not isprime(p):
        print('Modulus is not prime! Returning 0.')
        return 0


    y = x
    y = y % p

    if y == 0:
        print('Cannot find inverse of 0 mod p')
        return 0

    n = 1
    while not(y == 1):
        y += x
        y = y % p
        n += 1

    return n


def inv_mod_N_brute_force(x, N):

    y = x
    y = y % N

    if y == 0:
        print('Cannot find inverse of 0 mod N')
        return 0

    if igcd(y, N) > 1:
        print('x must be co-prime to N for an inverse to exist.')
        return 0


    n = 1
    while not(y == 1):
        y += x
        y = y % N
        n += 1

    return n



def inv_mod_power_of_p(x, p, k):
    """
    Find inverse of x mod p^k using LIFTING!
    Start by finding z = x^-1 mod p
    Then lift z to higher powers of p
    :param x:
    :param p:
    :param k:
    :return: inverse
    """

    y = inv_mod_p_brute_force(x, p)

    e = 1
    N = p

    p_to_the_k = 1

    while e < k:

        if e & k:
            p_to_the_k *= N

        r = (x * y - 1) / N
        z = y - y * r * N
        N = N*N
        z = z % N

        e *= 2
        y = z




    y = y % (p**k)

    return y


def test_stub():

    p = 2
    k = 3
    N = p**k
    x = 11

    a = inv_mod_power_of_p(x, p, k)

    b = inv_mod_N_brute_force(x, N)


    N = 15


    for x in range(1, N):
        z = inv_mod_N_brute_force(x, N)
        if z == 0:
            continue

        print(x, z, x * z, (x*z) % N)

    print('x')