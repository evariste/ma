


from sympy.ntheory import nextprime, factorint
from sympy.ntheory.primetest import isprime
from sympy.ntheory.residue_ntheory import is_quad_residue
import numpy as np


from itertools import product




def solve_x2_plus_y2_equals_N(N):
    """
    Use number theoretic results to find the solutions to x^2 + y^2 = N
    based on the factorisation of N
    :param N:
    :return:
    """

    if N == 1:
        return [(1,0)]

    factors = factorint(N)

    prime_factors = list(factors.keys())
    all_pairs = {}

    for p in prime_factors:
        exponent = factors[p]

        if ((p % 4) == 3) and ((exponent % 2) == 1):
            # For N to be expressed as the sum of two squares,
            # every prime factor of the form 4k+3 must have
            # an even exponent.
            return []


        all_pairs[p] = solve_x2_plus_y2_equals_prime_power(p, exponent)


    # Prime factors of form 4k+1
    ps_A = [p for p in prime_factors if (p%4)==1]

    # Remaining prime factors
    ps_B = [p for p in prime_factors if (p%4)==3]

    if 2 in prime_factors:
        ps_B.append(2)

    # The reps for the primes in set A
    sets_A = [all_pairs[p] for p in ps_A]

    # The reps for the rest of the primes.
    pairs_B = []
    for p in ps_B:
        pairs_B += all_pairs[p]

    n_A = len(sets_A)

    pairs_set_A = []

    # Loop over the product of all the sets for primes of form 4k+1, i.e. choose one pair for each prime.
    for tup_a in product(*sets_A):
        if len(tup_a) < 1:
            continue

        # Consider all possible flips when combining the pairs.
        # The complement of a flip pattern produces the same result as the original.
        # E.g. for pairs [ (a,b), (c,d) ] a flip pattern '10' leads to [ (b,a), (c,d) ] and when combined to give a single pair
        # the result will be the same as given by the flip pattern '01' i.e. by [ (a,b), (d,c) ]
        for n in range(2 ** (n_A - 1)):
            list_a = list(tup_a)

            x = n
            for k in range(n_A):
                if x & 1:
                    list_a[k] = list_a[k][::-1]
                x = x >> 1

            a,b = combine_x2_plus_y2_pairs_multiple(list_a)
            pairs_set_A.append((a,b))




    pairs_sets_all = []

    if len(pairs_set_A) > 0:
        for pair_A in pairs_set_A:
            a,b = combine_x2_plus_y2_pairs_multiple(pairs_B + [pair_A])
            pairs_sets_all.append((a,b))
    else:
        a, b = combine_x2_plus_y2_pairs_multiple(pairs_B)
        pairs_sets_all.append((a, b))

    return pairs_sets_all



def combine_x2_plus_y2_pairs_multiple(pairs):
    a, b = pairs[0]
    for k in range(1, len(pairs)):
        a, b = combine_x2_plus_y2_pairs(a, b, pairs[k][0], pairs[k][1])
    return a,b

def combine_x2_plus_y2_pairs(a, b, c, d):
    """
    Given two numbers that are expressed as m = a^2 + b^2 and n = c^2 + d^2
    Return e,f where mn = e^2 + f^2

    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """

    return abs(a*c - b*d), abs(a*d + b*c)
    # Varying the order of the arguments can only give two possible results.
    # a,b,c,d -> ac-bd, ad+bc  Y
    # within pair swaps of the first and/or second pairs
    # a,b,d,c -> ad-bc, ac+bd  X
    # b,a,c,d -> bc-ad, bd+ac  X
    # b,a,d,c -> bd-ac, bc+ad  Y
    # swap of whole pairs
    # c,d,a,b -> ca-db, cb+da  Y

def solve_x2_plus_y2_equals_N_brute_force(N):

    pairs_brute = []
    M = int(np.round(np.sqrt(N)))

    for k in range(M+1):
        j = np.sqrt(N - k*k)
        if j == np.round(j):
            j = int(j)

            if k < j:
                k, j = j, k

            pairs_brute.append((j, k))

    pairs_brute = list(set(pairs_brute))

    return pairs_brute




def solve_x2_plus_y2_equals_prime_power(p, exponent):
    """
    Find all the ways of expressing p^k as the sum of two squares.
    :param p:
    :param exponent:
    :return:
    """

    ret_val = []

    if ((p % 4) == 3) and ((exponent % 2) == 0):
        ret_val.append((p ** (exponent / 2), 0))


    if p == 2:
        if (exponent % 2) == 0:
            ret_val.append((2 ** (exponent / 2), 0))
        else:
            n = (exponent - 1) / 2
            ret_val.append( (2**n, 2**n) )


    if (p % 4) == 1:

        a, b = solve_x2_plus_y2_equals_prime(p)

        q = a + b * (0+1j)
        qbar = q.conjugate()

        for j in range(1 + int(np.floor(exponent / 2))):
            z = q**j * qbar**(exponent - j)
            a = int(abs(z.real))
            b = abs(int(z.imag))
            if a > b:
                a, b = b, a
            ret_val.append( (a, b) )

    return ret_val




def solve_x2_plus_y2_equals_prime(p):
    """
    Solve for x, y in x^2 + y^2 = p

    :param p: Prime number 2, or p == 1 mod 4
    :return: x,y where x^2 + y^2 = p
    """

    if not isprime(p):
        return None

    if p == 2:
        return 1, 1

    if (p % 4) == 3:
        return None


    # p = 1 mod 4

    # Get a solution of the equation x^2 == -1 mod p
    c = get_non_residue(p)
    x = power_a_b_mod_n(c, (p - 1) / 4, p)

    A = p
    B = x
    R = A % B

    if R > 1:
        while R * R > p:
            A = B
            B = R
            R = A % B
        A = B
        B = R
        R = A % B

    return B, R  # B^2 + R^2 == p



def power_a_b_mod_n(a, b, n):
    """
    Find a^b mod(n)
    :param a:
    :param b:
    :param n:
    :return:
    """

    if b < n:
        val = 1
        a = a % n  # a mod(n)
        # The binary representation of the index can be used.
        # a^index can be expressed as a product of a subset of elements chosen from
        # a^1 a^2 a^4 a^8 ...
        # The subset corresponds to the ones in the binary representation of index
        if a == 0:
            return 0

        while (b > 0) & (val > 0):
            if b % 2 > 0:
                val = (val * a) % n
            a = (a * a) % n
            b = b / 2

        return val


    # If we got here then index >= n
    # Look for a cycle in the sequence of powers.


    storedPowers = np.zeros((2*n,), dtype=np.int64)
    storedPowers[0] = a % n
    storedPowers = [ a % n ]

    i = 1
    cycleFound = False
    ix_start, cycle_length = None, None

    while (i < 2 * n) & (not cycleFound):

        curr = (a * storedPowers[i - 1]) % n
        storedPowers.append( curr )

        if curr in storedPowers[:-1]:
            ix_start = storedPowers.index(curr)
            cycleFound = True
            cycle_length = i - ix_start
        i += 1

    if (i == 2 * n) & (not cycleFound):
        print "Error : power_a_b_mod_n : no cycle found"
        exit()

    ix = ix_start + (b - 1 - ix_start) % cycle_length

    return storedPowers[ix]


def search_for_non_residue(p):
    max_iter = 10000

    q = 2
    j = 0

    while (j < max_iter) and is_quad_residue(q, p):
        j += 1
        q = nextprime(q)

    if j >= max_iter:
        raise Exception('Reached max iterations!')

    return q


def get_non_residue(p):

    if not isprime(p):
        return None

    if p == 2:
        return 0


    p_mod_4 = p % 4

    if p_mod_4 == 1:

        if (p % 8) == 5:
            return 2

        if (p % 24) == 17:
            return 3


    # p = 3 mod 4 OR p = 1 mod 24
    return search_for_non_residue(p)

