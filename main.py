#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Simulation of the Gaspard-Rice model
"""

__author__ = "Maxime Trépanier"
__date__ = "20-01-2024"

from argparse import ArgumentParser
import numpy as np
from matplotlib import pyplot as plt

import scatter
import plotting

if __name__ == "__main__":
    parser = ArgumentParser(description="Usage of Gaspard-Rice simulator")
    parser.add_argument('-b', type=float, default=0, help='Impact parameter')
    parser.add_argument('--anim', action="store_true", default=False,
                        help="Save an animated version?")
    parser.add_argument('--angle', action="store_true", default=False,
                        help="Compute a graph of the deflected angle as a\
                        function of the impact parameter b.")
    parser.add_argument('--range', type=float, nargs=2, default=[0, 0.5],
                        help='Range for impact parameter')
    parser.add_argument('--save', type=str, default="",
                        help="Save graphs to given filename")
    args = parser.parse_args()

    print("\nChaotic scattering in the Gaspard-Rice model (2d)")

    # GR model with 3 discs
    gr = scatter.GaspardRice(max_r=5)
    d = 2.5
    for x in [(-(3**0.5)*d/6, d/2), (d/(3**0.5), 0), (-(3**0.5)*d/6, -d/2)]:
        gr.add_sphere(x, 1)

    # 2 Modes:
    # (SSE) Single scattering event
    # (SRA) Scattering over a range of angles
    if args.angle:  # SRA
        # here maybe use data/C++
        b = np.linspace(args.range[0], args.range[1], 1000)
        angle, transit = gr.scattering_range_angles(b)
        fig1 = plotting.plot_angle_out(b, angle, 1)
        fig2 = plotting.plot_transit_time(b, transit, 2)
        if args.save != "":
            fig1.savefig(args.save + "-angle.png")
            fig2.savefig(args.save + "-reflections.png")
        else:
            plt.show()
    else:  # SSE
        path = gr.single_scattering_event(args.b)
        # -2 accounts for initial + final point
        print("b = {} has {} relfections".format(args.b, len(path)-2))
        if args.anim:
            plotting.save_anim_path(gr, path, args.save)
        else:
            plotting.plot_path_single_event(gr, path)
            if args.save:
                plt.savefig(args.save + "-{:.6f}b.pdf".format(args.b))
            else:
                plt.show()
