"""
authors: Pelin Kömürlüoğlu (pkoemuerlueo@uos.de)

This module contains helper and test functions for Problemset 3
 of the course "Cognitive Modeling" at the University of Osnabrueck.
 This module exists in order to load certain functionality into the
 assignment notebooks without involuntarily giving students access to
 solutions.
"""

import numpy as np

def act_func(x):

    return 1 / (1 + np.exp(-x))
def act_func_der(x):

    return x * (1-x)
