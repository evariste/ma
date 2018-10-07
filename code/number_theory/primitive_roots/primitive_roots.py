import numpy as np
from sympy.core.numbers import igcd
from sympy.ntheory import totient




N = 17

# Numbers co-prime to N

Phi_N = []

for v in range(1, N):
    if igcd(N, v) == 1:
        Phi_N.append(v)

print(Phi_N)


orders = []

elements_with_order = {}


prim_roots = []

print('order     powers sequence')
for v in Phi_N:

    g = v
    s = ''
    order = 1
    while not (g == 1):
        s = s + '{:>3d}'.format(g)
        g = (g * v) % N
        order += 1

    orders.append(order)

    if order in elements_with_order.keys():
        elements_with_order[order].append(v)
    else:
        elements_with_order[order] = [v]


    if order == (N-1):
        prim_roots.append(v)

    s = s + '{:>3d}'.format(1)
    s = '{:>3d}   '.format(order) + s
    print(s)



# Uniquify
orders = sorted(list(set(orders)))



print('   ===   ')

print('order     elements with this order')
for order in orders:
    print('{:>3d}       {:s}'.format(order, ' '.join(map(str, elements_with_order[order]))))

print('   ===   ')

print('order   Euler totient of this order')
for order in orders:
    t = totient(order)
    print('{:>3d}   {:>3d}'.format(order, t))


print('Primitive roots')
print(prim_roots)

print('x')
