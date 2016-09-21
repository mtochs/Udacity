#!/usr/bin/python

""" 
Simple function that displays a scatter plot with two feature inputs
from data_dict
"""


import numpy as np
import matplotlib.pyplot as plt
from feature_format import featureFormat, targetFeatureSplit

def scatplot(data, x, y):
    d = featureFormat(data, [x, y, 'poi'])
    for point in d:
        xp = point[0]
        yp = point[1]
        poi = point[2]
        color = 'red' if poi else 'blue'
        plt.scatter(xp, yp, color=color)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()




