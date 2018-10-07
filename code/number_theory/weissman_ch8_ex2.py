from lifting_square_roots import *


# Is 41 a square mod 1,000,000 ?

# 10^6 = 2^6 5^6


k = 6

u = sq_root_mod_2_power_k(41, k)

v = sq_root_mod_p_power_k(41, 5, k)

two_to_k = 2**k

p_to_k = 5**k



# Use Chinese remainder theorem to find a number
# that is equal to u mod (2^k) and equal to v mod(5^k)

found = False

w = v # == v mod 5^6

for _ in range(two_to_k):

    if w % two_to_k == u:
        found = True
        break

    w += p_to_k



assert found

r = (w*w) % (10**k)

assert r == 41


print(' {:d}^2 = {:d} = 41 mod 2^{:d}'.format(u, u*u, k))

print(' {:d}^2 = {:d} = 41 mod 5^{:d}'.format(v, v*v, k))

print(' {:d}^2 = {:d} = 41 mod 10^{:d}'.format(w, w*w, k))


# Other solutions possible.
# 13^2 = 169 = 41 mod 2^6
# 696^2 = 484416 = 41 mod 5^6
# 703821^2 = 495364000041 = 41 mod 10^6

print('x')
