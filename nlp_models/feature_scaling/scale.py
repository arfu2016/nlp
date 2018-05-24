"""
@Project   : DuReader
@Module    : pca.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/24/18 1:16 PM
@Desc      : 
"""

from sklearn.datasets import load_iris
import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt

from sklearn import decomposition
from sklearn.preprocessing import scale


def scale2(X):
    # Standardize by remove average
    X = X - X.mean(axis=0)
    print(X.mean(axis=0))

    # print(X.std(axis=0))

    X = X/X.std(axis=0)
    # make standard deviation equal to 1
    print(X.std(axis=0))


if __name__ == '__main__':

    iris = load_iris()
    X = iris.data
    k = 2

	x1 = scale(X)
    x2 = scale2(X)

