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
    parser.add_argument('-b', type=float, default=0, nargs='+',
                        help='Either the impact parameter, or two numbers\
                        defining the range of impact parameters')
    parser.add_argument('--save', type=str, default="",
                        help="Save graphs to given filename")
    parser.add_argument('--anim', action="store_true", default=False,
                        help="Save an animated version?")
    args = parser.parse_args()

    print("\nChaotic scattering in the Gaspard-Rice model (2d)")

    # GR model with 3 discs
    gr = scatter.GaspardRice()

    # 2 Modes:
    # (SSE) Single scattering event
    # (SRA) Scattering over a range of angles
    if len(args.b) == 1:  # SSE
        path = gr.single_scattering_event(args.b[0])
        # -2 accounts for initial + final point
        print("b = {} has {} relfections".format(args.b[0], len(path)-2))
        if args.anim:
            plotting.save_anim_path(gr, path, args.save)
        else:
            plotting.plot_path_single_event(gr, path)
            if args.save:
                plt.savefig(args.save + "-{:.6f}b.pdf".format(args.b[0]))
            else:
                plt.show()
    elif len(args.b) == 2:  # SRA
        b = np.linspace(args.b[0], args.b[1], 1000)
        angle, transit = gr.scattering_range_angles(b)
        fig1 = plotting.plot_angle_out(b, angle, 1)
        fig2 = plotting.plot_transit_time(b, transit, 2)
        if args.save != "":
            fig1.savefig(args.save + "-angle.png")
            fig2.savefig(args.save + "-reflections.png")
        else:
            plt.show()
    else:  # SSE
        raise ValueError("Wrong number of parameters for b")
