#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r""" Implementation of scattering in the GR model.
"""

__author__ = "Maxime Trépanier", "Shanny Pelchat-Voyer"
__date__ = "21-03-2015"

# Dependancies
import numpy as np
from matplotlib import pyplot as plt


class GaspardRice:
    """ Simulation of scattering in the Gaspard-Rice model (i.e. an array of
    reflecting spheres) in d dimensions.
    """
    def __init__(self, d=2, max_r=6):
        """ d is the dimension of space, max_r the maximal distance within
        which the spheres are contained.
        """
        self.d = d
        self.spheres = [(np.zeros(d), max_r)]  # outer sphere

    def add_sphere(self, x, r):
        r""" Adds a sphere at position x with radius r.

        :param x: center of the sphere
        :type x: numpy array
        :param r: radius
        :type r: float
        :rtype: none
        """

        if len(x) != self.d:
            raise ValueError("x should have dimension " + str(self.d))
        if np.linalg.norm(x) + r > self.spheres[0][1]:
            raise ValueError("this sphere lies outside the maximal radius ",
                             str(self.spheres[0][1]))
        self.spheres.append((x, r))

    def draw_spheres(self, axis):
        """ Draws all the spheres of the model on the given plot. (only for d=2)
        """

        assert self.d == 2
        for x, r in self.spheres[1:]:
            c = plt.Circle(x, r, fill=False, color='k', linewidth=1)
            axis.add_artist(c)

    def order_from(self, x0):
        """ Returns the list of indices of spheres ordered by their distance
        from x0.
        """

        def dist_from(sph, x0):
            return np.linalg.norm(sph[0] - x0) - sph[1]
        dist = [(i, dist_from(self.spheres[i], x0))
                for i in range(1, len(self.spheres))]
        dist.sort(key=lambda x: x[1])
        dist.append((0, 0))
        return map(lambda x: x[0], dist)

    def iterate(self, x, v):
        r""" Finds the next intersection of the ray at position x in direction v
        with any of the spheres, and calculates the reflection. v is assumed to
        be unit norm.

        :param x0: current position
        :type x0: numpy array
        :param v0: current direction
        :type v0: numpy array
        :return: exited?, x_(i+1), v_(i+1)
        """

        for sphere_index in self.order_from(x):
            r = self.spheres[sphere_index][1]  # radius
            # vector from x0 to center of sphere
            d = self.spheres[sphere_index][0] - x

            # does the ray intersect this sphere?
            # if it is aimed in the wrong direction, then no
            if np.dot(v, d) < 0 and sphere_index != 0:
                continue

            # finding the intersection of a line and a sphere corresponds to
            # solving a quadratic equation:
            vd = np.dot(v, d)
            d2 = np.dot(d, d)

            # calculate the discriminant
            disc = r**2 + vd**2 - d2

            # if disc > 0, the ray intersects the sphere, for d<0 it doesn't
            if disc < 0:
                continue

            # calculate the intersection point
            disc = disc**0.5
            # sign of the square root
            w = -1
            if sphere_index == 0:  # if we are inside the sphere -> outer sphere
                w = 1
            xnext = x + (vd + w*disc)*v
            normal_vector = self.spheres[sphere_index][0] - xnext
            vnext = v - 2*np.dot(normal_vector, v)*normal_vector / r
            vnext = vnext / np.linalg.norm(vnext)

            if w == 1:
                return True, xnext, v
            return False, xnext, vnext
        # did not intersect any sphere
        return True, x, v

    def single_scattering_event(self, b, max_iteration=1000):
        """ Calculates the path of a single ray with impact paramater b. """

        # Ray tracing
        xi = np.array([-3, b], dtype=np.float128)
        vi = np.array([1, 0], dtype=np.float128)
        path = [(xi, vi)]

        # Ray tracing
        for i in range(max_iteration):
            exited, xi, vi = self.iterate(xi, vi)
            path.append((xi, vi))
            if exited:
                break

        return path

    def scattering_range_angles(self, b, max_iteration=1000):
        """ Calculates the exit angle and number of reflections for each value
        of the impact parameter b.
        """

        # Incoming rays. Pick x coordinate outside the system (here -3)
        rays = np.array([-3 * np.ones(len(b)), b]).T
        angle_out = []  # Exit angle
        reflections = []  # Number of reflections

        # Ray tracing
        for r in rays:
            xi = r
            vi = np.array([1, 0])
            ti = 0
            for i in range(max_iteration):
                ti += 1
                exited, xi, vi = self.iterate(xi, vi)
                if exited:
                    break

            # exit angle
            angle_out.append(np.arctan2(vi[1], vi[0]))
            reflections.append(ti)

        angle_out = np.array(angle_out)
        # Convert interval [-pi, pi] to [0, 2*pi]
        angle_out = np.mod(angle_out, 2*np.pi*np.ones(len(angle_out)))
        reflections = np.array(reflections)

        return angle_out, reflections
