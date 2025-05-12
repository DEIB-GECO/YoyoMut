from math import sqrt


def confidence_interval(count, total):
    # count = number of sequences with given mutation
    # total = total sequences that day
    p = count / total
    n = total
    # z = 1.9599639715843482
    z = 1.96
    lower_bound = (p + (z ** 2) / (2 * n) - z * sqrt((p * (1 - p)) / n + (z ** 2) / (4 * n ** 2))) / (1 + (z ** 2) / n)
    upper_bound = (p + (z ** 2) / (2 * n) + z * sqrt((p * (1 - p)) / n + (z ** 2) / (4 * n ** 2))) / (1 + (z ** 2) / n)
    return max(lower_bound, 0), max(upper_bound, 0)
