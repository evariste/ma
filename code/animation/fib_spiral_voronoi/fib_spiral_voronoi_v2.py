

import numpy as np

from matplotlib import pyplot as plt

from scipy.interpolate import interp1d

from scipy.spatial import Voronoi, voronoi_plot_2d

from shutil import copy


def field_2d(pts, n_knots=10, sz_noise=0.4):

    xp = np.linspace(0, 1, n_knots)
    yp = np.zeros(xp.shape)

    yp[1:-1] = np.random.randn(n_knots-2) * sz_noise

    x_lo, y_lo = np.min(pts, axis=0)
    x_hi, y_hi = np.max(pts, axis=0)

    xx = pts[:, 0]
    yy = pts[:, 1]

    xx = (xx - x_lo) / (x_hi - x_lo)
    yy = (yy - y_lo) / (y_hi - y_lo)

    yp[1:-1] = np.random.rand(n_knots - 2) * sz_noise
    f_i = interp1d(xp, yp, kind='cubic')

    yp[1:-1] = np.random.rand(n_knots - 2) * sz_noise
    f_j = interp1d(xp, yp, kind='cubic')

    return f_i(xx) * f_j(yy)

def get_field_pair(pts, n_knots=10, sz_noise=0.3):
    xy_disp = np.zeros(pts.shape + (2,))

    xy_disp[:, 0, 0] = field_2d(pts, n_knots=n_knots, sz_noise=sz_noise)

    xy_disp[:, 1, 0] = field_2d(pts, n_knots=n_knots, sz_noise=sz_noise)

    xy_disp[:, 0, 1] = field_2d(pts, n_knots=n_knots, sz_noise=sz_noise)

    xy_disp[:, 1, 1] = field_2d(pts, n_knots=n_knots, sz_noise=sz_noise)
    return xy_disp


phi = (1.0 + np.sqrt(5.0)) / 2.0

n_pts = 50

ns = np.arange(n_pts)

R = np.sqrt(ns)

A = ns * np.pi * (2 - phi)

t = phi * ns

x = R * np.cos(A)
y = R * np.sin(A)


xy = np.zeros((len(x),2))
xy[:,0] = x
xy[:,1] = y


xy_list = xy.tolist()
xy_list.sort()
ix_dup = np.zeros(len(xy))

for k in range(1, len(xy)):
    p1 = np.asarray(xy_list[k])
    p2 = np.asarray(xy_list[k-1])
    d = np.sum(np.abs(p1-p2))
    if d < 0.01:
        ix_dup[k] = 1

xy = np.asarray(xy_list)
xy_clean = xy[ix_dup < 1]

sz_noise = 0.0

xy_noise = sz_noise * np.random.randn(xy_clean.shape[0], xy_clean.shape[1], 2)
xy_noise[xy_noise > sz_noise] = sz_noise
xy_noise[xy_noise < -sz_noise] = sz_noise


##############

x_lim_lo = -2
x_lim_hi = 5
y_lim_lo = -2
y_lim_hi = 5


n_frames = 60

ax = plt.subplot(111)

method = 2

plot_centres = True

if method == 1:
    vor = Voronoi(xy_clean) # type: Voronoi
    xy_disp = get_field_pair(vor.vertices, n_knots=20, sz_noise=1.2)
else:
    xy_disp = get_field_pair(xy_clean, n_knots=20, sz_noise=0.8)

bg_color = '#cccc00'

for k,t in enumerate(np.linspace(0,1,n_frames)):

    if method == 1:
        nn = (1-t) * xy_disp[...,0] + t *  xy_disp[...,1]
        vertices_vor = vor.vertices + nn
    else:
        nn = (1-t) * xy_disp[...,0] + t *  xy_disp[...,1]
        xy = xy_clean + nn
        vor = Voronoi(xy)
        vertices_vor = vor.vertices


    ax = plt.subplot(111, axisbg=bg_color)

    if plot_centres:
        ax.plot(xy[:,0], xy[:,1], '.r')


    for reg in vor.regions:
        if len(reg) < 1:
            continue
        if np.any([x < 0 for x in reg]):
            continue

        reg.append(reg[0])
        reg_xy = vertices_vor[reg]
        ax.plot(reg_xy[:,0], reg_xy[:,1], 'w')

    ax.set_xlim(x_lim_lo, x_lim_hi)
    ax.set_ylim(y_lim_lo, y_lim_hi)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_autoscale_on(False)

    curr_frame = 'frames/f_{:03d}.png'.format(k)
    plt.savefig(curr_frame)


    kk = 2 * n_frames - 1 - k
    copy(curr_frame, 'frames/f_{:03d}.png'.format(kk))

    ax.cla()

    print('x')




