#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Plotting toolbox for Gaspard-Rice model
"""

__author__ = "Maxime Trépanier"
__date__ = "20-01-2024"

import numpy as np
from matplotlib import pyplot as plt

# Matplotlib configuration
params = {'legend.fontsize': 20, 'axes.labelsize': 25}
plt.rcParams['axes.linewidth'] = 3
plt.rcParams['xtick.major.size'] = 8
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 4
plt.rcParams['xtick.minor.width'] = 2
plt.rcParams['ytick.major.size'] = 8
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 4
plt.rcParams['ytick.minor.width'] = 2
plt.rcParams.update(params)
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)

c_orange = np.array([0.85, 0.4, 0])
c_blue = np.array([0.35, 0.8, 0.8])
c_blue_1 = "#449D9D"
c_blue_3 = "#2F8782"


def round_sig(x, sig=1):
    """ Round x to sig significative digits """
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def tex_uncertainty(x, dx, scientific=-1):
    r""" Returns the TEX string \num{x ± dx}, keeping only the significant
    number of digits. scientific specifies the number of decimal places below
    which one should use scientific notation. """
    # number of decimals places for x, dx
    nb_dec_x = int(math.floor(math.log10(abs(x))))
    nb_dec_dx = int(math.floor(math.log10(abs(dx))))

    # the number of significant digits is 1 + the difference
    sig = 1 + nb_dec_x - nb_dec_dx
    if dx*10**(-nb_dec_dx) < 3:
        # if the dx starts with 3 or less, keep 2 significant digits
        sig = sig+1

    # using scientific notation:
    if nb_dec_x < scientific:
        # x, dx rounded to significant digits
        xr = round_sig(10**(-nb_dec_x)*x, sig)  # round
        dxr = round_sig(10**(-nb_dec_x)*dx, sig - (nb_dec_x - nb_dec_dx))
        # format and remove trailing zeros
        xr = "{:.14f}".format(xr).rstrip('0')
        dxr = "{:.14f}".format(dxr).rstrip('0')
        return r"\num{" + xr + r" \pm " + dxr + ' e' + "{}".format(nb_dec_x)\
               + '}'
    # using regular notation:
    else:
        xr = round_sig(x, sig)
        xr = "{:.14f}".format(xr).rstrip('0')
        dxr = round_sig(dx, sig - (nb_dec_x - nb_dec_dx))
        dxr = "{:.14f}".format(dxr).rstrip('0')
        return r"\num{" + xr + r" \pm " + dxr + '}'


def set_graph_axis_in_pi_multiple(axis, dx, x_min, x_max, den, which='x'):
    """ Relabels the ticks of axis (matplotlib.axis) in multiples of pi. x_min,
    x_max, dx are counted in multiples of pi. which selects either the 'x', 'y'
    or 'z' axis.

    :param axis: Ref to a matplotlib axis object
    :param dx: distance between ticks
    :type dx: float
    :param x_min: lower range of x
    :type x_min: float
    :param x_max: upper range of x
    :type x_max: float
    :param den: denominator of the fractions
    :type den: int
    :rtype: None
    """

    ticks = np.arange(x_min, x_max+dx, dx)  # coordinates of ticks
    labels = []

    # build labels for ticks
    for x in ticks:
        # special cases:
        if x == 0:
            labels.append(r"$0$")
        # if x is divisible by d
        elif x % den == 0:
            if x/den == 1:
                text = ''
            elif x/den == -1:
                text = '-'
            else:
                text = x // den
            labels.append(r"${}\pi$".format(text))
        elif den == 1:
            labels.append(r"${} \pi $".format(int(i)))
        # generic case
        else:
            if x == 1:
                text = ''
            elif x == -1:
                text = '-'
            else:
                text = x
            labels.append(r"$\frac{" + "{}".format(text) + r" \pi}{"
                          + "{}".format(den) + r"}$")

    if which == 'x':
        axis.set_xlim(x_min*np.pi/den, x_max*np.pi/den)
        axis.set_xticks(ticks*np.pi/den)
        axis.set_xticklabels(labels)
    if which == 'y':
        axis.set_ylim(x_min*np.pi/den, x_max*np.pi/den)
        axis.set_yticks(ticks*np.pi/den)
        axis.set_yticklabels(labels)
    if which == 'z':
        axis.set_zlim(x_min*np.pi/den, x_max*np.pi/den)
        axis.set_zticks(ticks*np.pi/den)
        axis.set_zticklabels(labels)


def plot_path_single_event(gr, path, nfig=1):
    """ Returns a figure of the given path. """

    fig = plt.figure(nfig, figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    gr.draw_spheres(ax)

    pts = np.array([x for x, v in path]).T
    ax.plot(pts[0], pts[1], 'k-')
    return fig


def save_anim_path(gr, path, filename, nfig=1):
    fig = plt.figure(nfig, figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    gr.draw_spheres(ax)

    pts = np.array([x for x, v in path]).T
    vec = np.array([v for x, v in path]).T
    traj, = ax.plot(pts[0], pts[1], 'k-')

    for i in range(len(path)):
        traj.set_xdata(pts[0][:i+1])
        traj.set_ydata(pts[1][:i+1])
        fig.canvas.draw()
        plt.savefig(filename + "{}.png".format(i))

    return fig


def plot_angle_out(b, angle_out, nfig=1):
    fig = plt.figure(nfig, figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.set_xlabel(r"$b$")
    ax.set_ylabel(r"Exit angle")
    set_graph_axis_in_pi_multiple(ax, 2, 0, 6, 3, 'y')  # Rename labels
    ax.plot(b, angle_out, '-', color=c_blue_3)
    plt.tight_layout()

    return fig


def plot_transit_time(b, transit, nfig=1):
    fig = plt.figure(nfig, figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.plot(b, transit-2, color=c_blue_3)
    ax.set_xlabel("$b$")
    ax.set_ylabel("Nb. reflections")
    plt.tight_layout()

    return fig
