import numpy as np
import collections
import random

from project_util import plot_histogram


# Pick a random bin 
def strategy_1(num_b, num_runs):
    max_values = np.zeros(num_runs)
    for i in xrange(num_runs):
        bins = np.zeros(num_b)
        for j in xrange(num_b):
            bins[random.randint(0, num_b - 1)] += 1
        max_values[i] = max(bins)
    return max_values

# From two random bins, pick the one with fewer balls
def strategy_2(num_b, num_runs):
    max_values = np.zeros(num_runs)
    for i in xrange(num_runs):
        bins = np.zeros(num_b)
        for j in xrange(num_b):
            rand_values = np.random.choice(num_b, 2)
            if (bins[rand_values[0]] > bins[rand_values[1]]):
                bins[rand_values[1]] += 1
            elif (bins[rand_values[0]] < bins[rand_values[1]]):
                bins[rand_values[0]] += 1
            else:
                min_index = random.randint(0, 1)
                bins[rand_values[min_index]] += 1

        max_values[i] = max(bins)
    return max_values

# From three random bins, pick the one with the fewest balls
def strategy_3(num_b, num_runs):
    max_values = np.zeros(num_runs)
    for i in xrange(num_runs):
        bins = np.zeros(num_b)
        for j in xrange(num_b):
            rand_values = np.random.choice(num_b, 3)
            bin_choices = [bins[k] for k in rand_values] # The # of balls in each of the random bins
            min_value = min(bin_choices)
            # Get the indices of the bins with the fewest balls of the random bins
            bin_indices = [k for k in rand_values if bins[k] == min_value]
            # Select one of those bins at random
            num_duplicates = bin_choices.count(min_value)
            index_selected = random.randint(0, num_duplicates - 1)

            bins[bin_indices[index_selected]] += 1
        max_values[i] = max(bins)
    return max_values

# More or less get 2 sets of bins, and select a random bin from each set, and place the ball in the bin
# with the fewer balls of those two
def strategy_4(num_b, num_runs):
    max_values = np.zeros(num_runs)
    for i in xrange(num_runs):
        bins = np.zeros(num_b)
        for j in xrange(num_b):
            index_1 = random.randint(0, num_b / 2 - 1)
            index_2 = random.randint(num_b / 2, num_b - 1)
            if (bins[index_1] <= bins[index_2]):
                bins[index_1] += 1
            else:
                bins[index_2] += 1

        max_values[i] = max(bins)
    return max_values


def main():
    pass


if __name__ == "__main__":
    N = 200000
    num_runs = 40
    max_values = np.zeros([200000,4])
    most_balls_1 = strategy_1(N, num_runs)
    for i in most_balls_1:
        max_values[i, 0] += 1

    most_balls_2 = strategy_2(N, num_runs)
    for i in most_balls_2:
        max_values[i, 1] += 1

    most_balls_3 = strategy_3(N, num_runs)
    for i in most_balls_3:
        max_values[i, 2] += 1

    most_balls_4 = strategy_4(N, num_runs)
    for i in most_balls_4:
        max_values[i, 3] += 1

    plot_histogram(max_values)