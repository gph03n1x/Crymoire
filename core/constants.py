#!/usr/bin/env python
    
class NOISELEVELS():
    """
    These levels dictate the noise level which is the upper border
    dictated from the sum of two characters occurance which ranges
    from 0.0 - 21.4
    """
    LOW = 3.98
    MEDIUM = 7.43
    HIGH = 10.54
    # The _NOISE variables dictates how many noise characters
    # we are going to add after a substitution
    LOW_NOISE = 0
    MEDIUM_NOISE = 1
    HIGH_NOISE = 2
    # In case our levels are higher than high
    DEFAULT_NOISE = 3


DEFAULT_OCCURANCES = {
    'A': 8.55, 'C': 3.16, 'B': 1.60, 'E': 12.10, 'D': 3.87,
    'G': 2.09, 'F': 2.18, 'I': 7.33, 'H': 4.96, 'K': 0.81,
    'J': 0.22, 'M': 2.53, 'L': 4.21, 'O': 7.47, 'N': 7.17,
    'Q': 0.10, 'P': 2.07, 'S': 6.73, 'R': 6.33, 'U': 2.68,
    'T': 8.94, 'W': 1.83, 'V': 1.06, 'Y': 1.72, 'X': 0.19,
    'Z': 0.11
}