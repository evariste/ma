


import os

from prime_utils import get_non_residue, solve_x2_plus_y2_equals_prime, solve_x2_plus_y2_equals_N, solve_x2_plus_y2_equals_N_brute_force

import numpy as np

from sympy.ntheory import nextprime





def main():


    N = np.random.randint(1000)
    N = 5 * 5 * 5 * 13 * 7 * 7 * 4
    from sympy.ntheory import factorint

    facs = factorint(N)
    for p in facs.keys():
        e = facs[p]
        if ((p%4) == 3) and ((e%2)==1):
            N *= p


    xx = solve_x2_plus_y2_equals_N(N)

    # Find the number of ways of representing N as the sum
    # of two squares counting all possible signs and orders e.g.
    #  4 = 2^2 + 2^2 = (-2)^2 + 2^2 = 2^2 + (-2)^2 = (-2)^2 + (-2)^2
    # so r_2_n[4] = 4

    r_2_n = dict()

    for N in range(2, 50):
        xx = solve_x2_plus_y2_equals_N(N)
        print(N)
        print(xx)
        print('\n')
        r_2_n[N] = 0
        for a,b in xx:
            if (a == b) or (a == 0) or (b == 0):
                r_2_n[N] += 4
            else:
                r_2_n[N] += 8


    for N in r_2_n.keys():
        print('{:>4d} {:>4d}'.format(N, r_2_n[N]))


    p = 5

    exponent = 7

    N = p**exponent

    pairs = solve_x2_plus_y2_equals_N(N)
    print('Method A:')
    print( sorted(pairs ))


    pairs_brute = solve_x2_plus_y2_equals_N_brute_force(N)

    print('Brute force:')
    print(sorted(pairs_brute))



    return 0



if __name__ == '__main__':
    os.sys.exit(main())