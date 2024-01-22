# Chaotic scattering in the Gaspard-Rice model

## Introduction
The Gaspard-Rice model [^1] is a simple example of a model which exhibits
chaos. In its simplest form, it consists of 3 discs in a plane (thought of as
reflective mirrors), and we're interested in the scattering of rays against
them. This turns out to be chaotic: a small variation of the impact parameter
$b$ of the incoming ray can lead to a large change in the scattering angle of
the outgoing ray.

## Overview
This repository contains a cleaned up version of the code I wrote for a project
on chaos theory (2015), in which I reproduced the results of the paper [^1].  

It contains 3 files:
 - main.py: A simple script to study scattering, either for a given impact
   parameter, e.g. by running

        $ ./main.py -b 0.1509
   or for a range of impact parameters, e.g.

        $ ./main.py -b 0 0.5
 - scatter.py: Implementation of a class GaspardRice which simulates the model
 - plotting.py: Additional methods to create graphs

[^1]: P. Gaspard, S. A. Rice; Scattering from a classically chaotic
  repellor. *J. Chem. Phys*. 15 February 1989; 90 (4): 2225–2241.
