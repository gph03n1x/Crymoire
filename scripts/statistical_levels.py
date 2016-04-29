#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is used for calculating the levels at flags.py
# which determine the noise added to the encrypted string
import __init__
from core.statistical import StatisticalEntropy


def get_levels():
    se = StatisticalEntropy()
    sums = []
    for i in se._occurances:
        for j in se._occurances:
            sums.append(se._occurances[i] + se._occurances[j])

    sums.sort()
    for i in range(4):
        print "Position: ", (i+1)*len(sums)/4-1," level:\
", sums[(i+1)*len(sums)/4-1]


if __name__ == "__main__":
    get_levels()
