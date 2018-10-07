

from sympy.ntheory.primetest import isprime

from sympy.ntheory.residue_ntheory import legendre_symbol

import numpy as np

from lifting_inverses import inv_mod_power_of_p

def sq_root_mod_p(a, p, verbose=False):

    if p > 2:
        return sq_root_mod_p_cipolla(a, p, verbose=verbose)

    assert p == 2

    return sq_root_mod_2_power_k(a, k, verbose=verbose)




def sq_root_mod_p_cipolla(n, p, verbose=False):
    """
    Find x such that x^2 = n mod p
    :param n:
    :param p:
    :return: x
    """

    assert isprime(p)

    assert p > 2

    if legendre_symbol(n, p) < 1:
        if verbose:
            print('{:d} is not a square mod {:d}'.format(n, p))
        return None


    # Find a such that a^2-p is not a square
    # Trial and error
    a = np.random.randint(1, p)

    while legendre_symbol(a*a-n, p) > -1:
        a = np.random.randint(1, p)

    z = (a*a - n) % p

    b = 1

    k = (p+1) / 2

    c, d = a_plus_b_root_z_power_k_mod_n(a, b, z, k, p)

    assert d == 0

    return c


# Field extension arithmetic mod n:

def a_plus_b_root_z_squared_mod_n(a, b, z, n):
    """
    Given x = (a + b sqrt(z))
    Find x^2 = c + d sqrt(z)
    where c = a^2 + b^2 z
    and d = 2 a b
    are the reduced coefficients mod n
    :return: (c, d)
    """

    c = (a**2 + b**2 * z) % n
    d = ( 2 * a * b ) % n
    return c, d

def prod_as_plus_bs_root_z_mod_n(a1, b1, a2, b2, z, n):
    """
    Given x = a1 + b1 sqrt(z) and y = a2 + b2 sqrt(z)
    Find x y = c + d sqrt(z)
    Where c = a1 a2 + b1 b2 z
    and d = a1 b2 + a2 b1
    are reduced mod n
    :return: (c, d)
    """
    c = (a1 * a2 + b1 * b2 * z) % n
    d = (a1 * b2 + a2 * b1) % n
    return c, d

def a_plus_b_root_z_power_k_mod_n(a, b, z, k, n):
    """
    Given x = (a + b sqrt(z))
    Find x^k in the form c + d sqrt(z)
    where c and d are the reduced coefficients mod n
    :return: (c, d)
    """

    # Use successive squaring.

    # current power
    p = 1

    x = (a, b)

    val = (1, 0)
    while p <= k:
        if k & p:
            # accumulate
            val = prod_as_plus_bs_root_z_mod_n(val[0], val[1], x[0], x[1], z, n)

        x = a_plus_b_root_z_squared_mod_n(x[0], x[1], z, n)

        p *= 2

    return val


def sq_root_mod_2_power_k_brute_force(a, k):

    p_power_k = 2 ** k

    n = 1 + p_power_k/2
    a = a % p_power_k
    x = None

    for j in range(n):

        if ((j*j) % p_power_k) == a:
            x = j
            break

    return x



def sq_root_mod_2_power_k(a, k, verbose=False):
    """

    :param a:
    :param k:
    :param verbose:
    :return:
    """

    if k < 3:
        # brute force
        return sq_root_mod_2_power_k_brute_force(a, k)


    # first just find p^k
    p_power_k = 1
    ee = 1
    nn = 2
    while ee <= k:
        if ee & k:
            p_power_k *= nn
        ee *= 2
        nn = nn * nn


    # Find a power of two, p^e, for which
    # x^2 == a mod p^e makes sense, i.e.
    # for which p^e > a
    e = 1
    p_power_e = 2

    while p_power_e <= a:
        e += 1
        p_power_e *= 2


    # Get x such that x^2 == a mod 2^e
    x = sq_root_mod_2_power_k_brute_force(a, e)

    if x is None:
        if verbose:
            print('{:d} is not a square mod 2^{:d}'.format(a, k))
        return None

    # Lift the square root if needed.
    while e <= k:
        r = (x*x - a) / p_power_e

        if (r % 2) == 1:
            # Need to shift x
            x += (p_power_e / 2)

        e += 1
        p_power_e *= 2

        x = x % p_power_e

    return x % p_power_k


def sq_root_mod_p_power_k(a, p, k, verbose=False):

    if p == 2:
        # Lifting square roots is different when p is 2
        return sq_root_mod_2_power_k(a, k, verbose=verbose)


    # p is odd.

    # Get x such that x^2 == a mod p
    x = sq_root_mod_p(a, p)

    if x is None:
        if verbose:
            print('{:d} is not a square mod {:d}^{:d}'.format(a, p, k))
        return None


    e = 1
    p_power_e = p
    p_power_k = 1


    # e will run through the powers of 2 ...

    while e <= k:

        if e & k:
            p_power_k *= p_power_e

        # find square root of n mod p^2e

        # Find inverse of 2x mod p^e
        b = inv_mod_power_of_p(2*x, p, e) # assert (2*x*b) % (p**e) == 1

        r = (x * x - a) / p_power_e

        z = x - b * r * p_power_e    # assert (z * z) % (p ** (2 * e)) == a

        x = z

        # e -> 2e
        e *= 2

        # p^e -> p^(2e)
        p_power_e = p_power_e * p_power_e

        # reduce x mod p^(2e)
        x = x % p_power_e     # assert (x*x) % p_power_e == a


    return x % p_power_k


def test_stub():

    print('   p == 2')

    p = 2
    k = 6
    p_power_k = p ** k

    squares = sorted(list(set([n * n % p_power_k for n in range(1, p_power_k)])))

    for a in squares:

        v = sq_root_mod_p_power_k(a, p, k)

        if v is None:
            continue

        assert (v*v) % p_power_k == a

        print('{:d}^2 == {:d} mod {:d}^{:d} = {:d}'.format(v, a, p, k, p_power_k))



    print('Odd prime')

    p = 5
    k = 6

    p_power_k = p ** k

    reps = 5
    r = 0

    while r < reps:
        a = np.random.randint(p_power_k)

        v = sq_root_mod_p_power_k(a, p, k)

        if v is None:
            continue

        r += 1

        assert (v*v) % p_power_k == a

        print('{:d}^2 == {:d} mod {:d}^{:d} = {:d}'.format(v, a, p, k, p_power_k))


    print('x')


# test_stub()

