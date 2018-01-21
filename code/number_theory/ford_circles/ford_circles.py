import sys

from matplotlib import pyplot as plt

from fractions import Fraction

import numpy as np

PHI = 0.5 * (1 + np.sqrt(5))

RESOLUTION=50


#######################################################


def circle(xy=(0.0,0.0), r=1.0, res=RESOLUTION):
    N = res + 1
    theta = np.linspace(0, 2*np.pi, num=N)

    pts = np.zeros((2, N))

    pts[0, :] = xy[0] + r * np.cos(theta)
    pts[1, :] = xy[1] + r * np.sin(theta)

    return pts


def ford_circle(frac # type: Fraction
                ):

    b = frac.denominator

    x = float(frac)
    y = 1.0 / b / b / 2.0

    return circle(xy=(x,y), r=y)

#######################################################

def fibonacci(n):

    if n == 0:
        return 0
    if n == 1:
        return 1

    k = 1
    a = 0
    b = 1
    c = 1

    while k < n:
        c = b + a
        a = b
        b = c
        k += 1

    return c

#######################################################

def fib_rat(n):


    if n <= 1:
        return Fraction(1,1)

    if n == 2:
        return Fraction(2,1)


    k = 2

    a = Fraction(1,1)
    b = Fraction(2,1)
    c = None

    while k < n:

        c = Fraction(a.numerator + b.numerator, a.denominator + b.denominator)
        a = b
        b = c
        k += 1

    return c


#######################################################

def poly_interesect_rect(p, rect):

    rect_xlo, rect_xhi, rect_ylo, rect_yhi = rect

    inside = np.bitwise_and(p[0] > rect_xlo, p[0] < rect_xhi)
    inside = np.bitwise_and(inside, p[1] > rect_ylo)
    inside = np.bitwise_and(inside, p[1] < rect_yhi)

    return np.any(inside)


#######################################################

def fib_ratio_ford_circles():

    ax = plt.subplot()

    N = 10

    for k in range(2, N+1):
        fr = fib_rat(k)
        c = ford_circle(fr)
        ax.fill(c[0], c[1], alpha=0.5, color=(0.5, 0.5, 0.5))
        ax.plot(c[0], c[1], linewidth=0.7, color='k')


    ax.set_aspect(1.0)
    plt.show()

#######################################################

def fib_ratio_ford_circles_2():

    xlo_0, xhi_0 = 1.2, 2.6
    ylo_0, yhi_0 = 0.0, 1.0

    cx, cy = (PHI, 0.0)

    fac = 0.95


    xlo, xhi = xlo_0, xhi_0
    ylo, yhi = ylo_0, yhi_0


    n_frames = 250

    for ix_fr in range(n_frames):

        print(ix_fr)

        fov_rect = (xlo, xhi, ylo, yhi)
        ax = plt.subplot()

        N = 0
        k = 1

        while N < 8:
            k += 1
            fr = fib_rat(k)
            c = ford_circle(fr)

            if not(poly_interesect_rect(c, fov_rect)):
                continue

            N += 1

            ax.fill(c[0], c[1], alpha=0.3, color=(0.5, 0.5, 0.5))
            ax.plot(c[0], c[1], linewidth=0.7, color='k')


        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)

        ax.set_xticks([PHI])
        ax.set_xticklabels(['$\phi$'])

        ax.set_aspect(1.0)
        plt.savefig('pics/frame{:03d}.png'.format(ix_fr), dpi=240)

        ax.cla()

        xlo = cx + fac * (xlo - cx)
        xhi = cx + fac * (xhi - cx)
        ylo = cy + fac * (ylo - cy)
        yhi = cy + fac * (yhi - cy)

    print('x')

#######################################################

def example_kissing_fractions():

    f1 = Fraction(71,26)
    f2 = Fraction(30,11)
    f3 = Fraction(101,37)

    # f1 = Fraction(1,2)
    # f2 = Fraction(6,11)
    # f3 = Fraction(7,13)

    fs = [f1, f2, f3]

    ax = plt.subplot()
    for f in fs:
        c = ford_circle(f)
        ax.fill(c[0], c[1], alpha=0.5, color=(0.5, 0.5, 0.5))
        ax.plot(c[0], c[1], linewidth=0.7, color='k')

    ax.set_aspect(1.0)
    plt.show()


#######################################################

def main():

    # fib_ratio_ford_circles()

    # example_kissing_fractions()

    fib_ratio_ford_circles_2()

    print('x')



#######################################################

if __name__ == '__main__':
    sys.exit(main())