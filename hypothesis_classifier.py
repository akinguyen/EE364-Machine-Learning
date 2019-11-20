import matplotlib.pyplot as plt
import scipy.io as io
import numpy as np
import math


def calculate_a(μX0, μY0, μX1, μY1, σX, σY, ρXY):
    return (2*(μX0 - μX1))/(σX*σX) + (2*ρXY*(μY1 - μY0))/(σX*σY)


def calculate_b(μX0, μY0, μX1, μY1, σX, σY, ρXY):
    return (2*(μY0 - μY1))/(σY*σY) + (2*ρXY*(μX1 - μX0))/(σX*σY)


def calculate_c(μX0, μY0, μX1, μY1, σX, σY, ρXY):
    return (μX1*μX1 - μX0*μX0)/(σX*σX) + (2*ρXY*(μX0*μY0 - μX1*μY1))/(σX*σY) + (μY1*μY1 - μY0*μY0)/(σY*σY)


def calculuate_mean_x_and_y(dataset):
    total_x = 0
    total_y = 0
    for x, y in dataset:
        total_x += x
        total_y += y
    return total_x/1000, total_y/1000


def plot_joint_gaussian(dataset_h0, dataset_h1, μX0, μY0, μX1, μY1, σX, σY, ρXY):
    error = 0
    a = calculate_a(μX0, μY0, μX1, μY1, σX, σY, ρXY)
    b = calculate_b(μX0, μY0, μX1, μY1, σX, σY, ρXY)
    c = calculate_c(μX0, μY0, μX1, μY1, σX, σY, ρXY)

    for x, y in dataset_h0:
        if a*x + b*y <= 0:
            error += 1
        plt.plot(x, y, 'bo')

    for x, y in dataset_h1:
        if a*x + b*y > 0:
            error += 1
        plt.plot(x, y, 'ro')

    # PLOT HYPOTHESIS THRESHHOLD LINE
    x = np.linspace(-10, 10, 100)
    y = (-c - a*x)/b

    plt.plot(x, y, '-r')
    plt.show()
    print(error, error/2000)
    return


''' READ DATASETS '''
tempmat = io.loadmat('gaussiandata.mat')
parta_H0_data = tempmat['parta_H0_data']
parta_H1_data = tempmat['parta_H1_data']
partb_H0_data = tempmat['partb_H0_data']
partb_H1_data = tempmat['partb_H1_data']
partc_H0_data = tempmat['partc_H0_data']
partc_H1_data = tempmat['partc_H1_data']

''' PLOT DATASETS '''
# part a
plot_joint_gaussian(parta_H0_data, parta_H1_data, 2, 2, -2, -2, 2, 1, 0)

# part b
plot_joint_gaussian(partb_H0_data, partb_H1_data, 1, 1, 3, -1,
                    math.sqrt(3/2), math.sqrt(2), 1/math.sqrt(3))

# part c
μX0, μY0 = calculuate_mean_x_and_y(partc_H0_data)
μX1, μY1 = calculuate_mean_x_and_y(partc_H1_data)

plot_joint_gaussian(partc_H0_data, partc_H1_data, μX0, μY0, μX1, μY1,
                    math.sqrt(2), 1, 0)
