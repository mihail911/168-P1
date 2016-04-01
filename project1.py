import numpy as np
import collections
import copy
import hashlib
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


NUM_HASH = 4
NUM_COUNTERS = 256

def count_min_sketch(num_trial, trial_stream):
    sketch_array = np.zeros((NUM_HASH, NUM_COUNTERS))
    for table_idx in xrange(4): # 0 -> 4
        for elem in trial_stream:
            elem_string = str(elem) + str(num_trial-1)
            hex_string = hashlib.md5(elem_string.encode('utf-8')).hexdigest()
            hash_value = int(hex_string[table_idx*2: table_idx*2 + 2], 16)
            sketch_array[table_idx, hash_value] += 1

    return sketch_array


def conservative_count_min_sketch(num_trial, trial_stream):
    sketch_array = np.zeros((NUM_HASH, NUM_COUNTERS))
    for elem in trial_stream:
        curr_counts = []
        hash_values = []
        for table_idx in xrange(4): # 0 -> 4
            elem_string = str(elem) + str(num_trial-1)
            hex_string = hashlib.md5(elem_string.encode('utf-8')).hexdigest()
            hash_value = int(hex_string[table_idx*2: table_idx*2 + 2], 16)

            curr_counts.append(sketch_array[table_idx, hash_value])
            hash_values.append(hash_value)

        arr_counts = np.array(curr_counts)
        # Perform conservative updates
        minimum_count_idx = np.where(arr_counts == arr_counts.min())[0]
        for min_idx in minimum_count_idx:
            min_hash = int(hash_values[min_idx])
            sketch_array[min_idx, min_hash] += 1

    return sketch_array


def find_value(count_min_array, value, num_trial):
    values = []
    for table_idx in xrange(4): # 0 -> 4
        elem_string = str(value) + str(num_trial-1)
        hex_string = hashlib.md5(elem_string.encode('utf-8')).hexdigest()
        hash_value = int(hex_string[table_idx*2: table_idx*2 + 2], 16)
        values.append(count_min_array[table_idx, hash_value])


    return min(np.array(values))


###### Conservative Updates in Count-Min Sketch

if __name__ == "__main__":

    # Part 2
    # Generate stream
    stream = []
    for idx in range(1, 10):
        minimum = 1000 * (idx-1) + 1
        maximum = 1000 * idx
        for elem in range(minimum, maximum+1):
            for t in range(idx):
                stream.append(elem)
                # TODO: Check that stream is properly being generated

    for idx in range(1, 51):
        value = 9000 + idx
        for t in range(idx**2):
            stream.append(value)


    # Heavy hitters in stream without count_min_sketch
    total_elems = len(stream)
    # print "Total elems: ", total_elems
    heavy_hitter_threshold = 0.01*total_elems
    # stream_counter = collections.Counter(stream)
    # heavy_hitters = []
    # for elem in stream_counter:
    #     if stream_counter[elem] > heavy_hitter_threshold:
    #         heavy_hitters.append(elem)
    #
    # print heavy_hitters
    # print len(heavy_hitters)

    # Data streams
    forward = copy.copy(stream)

    # Stream is now reversed
    stream.reverse()


    shuffled = copy.copy(stream)
    random.shuffle(shuffled)



    # (b).
    # Hash elems -- forward
    # heavy_hitter_arr = np.zeros((9050, 10))
    # for t in xrange(10):
    #     count_min_array = count_min_sketch(t, forward)
    #
    #     print "Trial: ", t
    #     for elem in xrange(1, 9051):
    #         # Compute estimates
    #         min_value = find_value(count_min_array, elem, t)
    #         heavy_hitter_arr[elem-1, t] = min_value
    #
    #
    # arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    # heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    # print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 23
    # print "Freq 9050: ", arr_averages_forward[9049] # Returns 2643.2
    #
    #
    #
    # # Hash elems -- backward
    #
    # heavy_hitter_arr = np.zeros((9050, 10))
    # for t in xrange(10):
    #     count_min_array = count_min_sketch(t, stream)
    #
    #     print "Trial: ", t
    #     for elem in xrange(1, 9051):
    #         # Compute estimates
    #         min_value = find_value(count_min_array, elem, t)
    #         heavy_hitter_arr[elem-1, t] = min_value
    #
    #
    # arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    # heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    # print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 23
    # print "Freq 9050: ", arr_averages_forward[9049] # Returns 2643.2
    #
    #
    # #
    # # # Hash elems -- shuffled
    # #
    # heavy_hitter_arr = np.zeros((9050, 10))
    # for t in xrange(10):
    #     count_min_array = count_min_sketch(t, shuffled)
    #
    #     print "Trial: ", t
    #     for elem in xrange(1, 9051):
    #         # Compute estimates
    #         min_value = find_value(count_min_array, elem, t)
    #         heavy_hitter_arr[elem-1, t] = min_value
    #
    #
    # arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    # heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    # print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 23
    # print "Freq 9050: ", arr_averages_forward[9049] # Returns 2643.2




    ################# Conservative Updates
    heavy_hitter_arr = np.zeros((9050, 10))
    for t in xrange(10):
        count_min_array = conservative_count_min_sketch(t, forward)

        print "Trial: ", t
        for elem in xrange(1, 9051):
            # Compute estimates
            min_value = find_value(count_min_array, elem, t)
            heavy_hitter_arr[elem-1, t] = min_value


    arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 23
    print "Freq 9050: ", arr_averages_forward[9049] # Returns 2576.2



    # Hash elems -- backward

    heavy_hitter_arr = np.zeros((9050, 10))
    for t in xrange(10):
        count_min_array = conservative_count_min_sketch(t, stream)

        print "Trial: ", t
        for elem in xrange(1, 9051):
            # Compute estimates
            min_value = find_value(count_min_array, elem, t)
            heavy_hitter_arr[elem-1, t] = min_value


    arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 21
    print "Freq 9050: ", arr_averages_forward[9049] # Returns 2500.0


    #
    # # Hash elems -- shuffled
    #
    heavy_hitter_arr = np.zeros((9050, 10))
    for t in xrange(10):
        count_min_array = conservative_count_min_sketch(t, shuffled)

        print "Trial: ", t
        for elem in xrange(1, 9051):
            # Compute estimates
            min_value = find_value(count_min_array, elem, t)
            heavy_hitter_arr[elem-1, t] = min_value


    arr_averages_forward = heavy_hitter_arr.mean(axis=1)
    heavy_hitters_forward = np.where(arr_averages_forward > heavy_hitter_threshold)
    print "Num heavy hitters: ", len(heavy_hitters_forward[0]) # Returns 21
    print "Freq 9050: ", arr_averages_forward[9049] # Returns 2500.0


##################################
    # Part 1

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
