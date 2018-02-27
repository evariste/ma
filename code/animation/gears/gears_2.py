

import numpy as np

from matplotlib import pyplot as plt

from scipy.interpolate import CubicSpline
from scipy.integrate import simps


def cost_func(A, r1, theta, target_val):
    y = r1 / (A - r1)
    return simps(y, theta) - target_val



def calc_theta2(A, r1, d_theta_1):
    theta2 = np.zeros(r1.shape)

    for k in range(1, len(theta2)):
        # fb = r1[k] / (A - r1[k])
        # fa = r1[k-1] / (A - r1[k-1])
        # d_theta_2 = d_theta_1 * 0.5 * (fa + fb)

        d_theta_2 = d_theta_1 * r1[k-1] / (A - r1[k-1])

        theta2[k] = theta2[k - 1] + d_theta_2

    return theta2

def calc_theta2_end(A, r1, d_theta_1):
    theta2 = calc_theta2(A, r1, d_theta_1)
    return theta2[-1]


n_knots = 5

t = np.linspace(0, 1, num=n_knots)

r = np.random.rand(n_knots) - 0.5
r[:2] = 0
r[-2:] = 0


spl = CubicSpline(t, r, bc_type='periodic')


n_pts = 400

t1 = np.linspace(0, 1, num=n_pts)

r1 = spl(t1)


r_lo = 2

r1 += np.min(r1) + r_lo



A = np.max(r1) + 0.05

target_val = 2.0 * np.pi

theta1 = np.linspace(0, 2.0*np.pi, len(r1))

theta2_end = target_val + cost_func(A, r1, theta1, target_val)

r_incr = 0.1


while theta2_end > target_val:
    A_left = A
    A += r_incr
    theta2_end = target_val + cost_func(A, r1, theta1, target_val)

A_right = A

from scipy import optimize

f = lambda x : cost_func(x, r1, theta1, target_val)
A_star = optimize.brentq(f, A_left, A_right)

A = A_star

theta2_scattered = calc_theta2(A_star, r1, theta1[1]-theta1[0])


n_step = 5
ax = plt.subplot(111)

pad = 0.3

xlim_lo = -1.0 * np.max(r1) - pad
ylim_lo = xlim_lo - pad
ylim_hi = -1.0 * ylim_lo
xlim_hi = A + (A - np.min(r1)) + pad


# for offset in np.linspace(0, 2*np.pi, n_step):

for k in range(1, n_pts, n_step):

    ix = range(k,n_pts) + range(0,k)

    x = r1 * np.cos(theta1[ix])
    y = r1 * np.sin(theta1[ix])

    x = list(x) + [x[0]]
    y = list(y) + [y[0]]
    ax.plot(x, y, 'g')

    plt.plot([0,x[0]], [0, y[0]], 'g' )

    # second point at (2,0)

    x2 = A - (A - r1) * np.cos(theta2_scattered[ix])
    y2 =   r1 * np.sin(theta2_scattered[ix])

    x2 = list(x2) + [x2[0]]
    y2 = list(y2) + [y2[0]]

    ax.plot(x2, y2, 'k')
    plt.plot([A,x2[0]], [0, y2[0]], 'k' )

    ax.set_aspect(1.0)
    ax.set_xlim([xlim_lo, xlim_hi])
    ax.set_ylim([ylim_lo, ylim_hi])

    ax.cla()


print('x')


