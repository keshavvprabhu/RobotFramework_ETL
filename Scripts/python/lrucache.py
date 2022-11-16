from functools import lru_cache
import matplotlib.pyplot as plt
import timeit

import numpy as np
from sklearn.linear_model import LinearRegression

def primes(start, end):
    if start < 2:
        exit(-1)
    st = timeit.default_timer()
    list_primes = list()
    for i in range(start, end+1):
        is_prime = True
        for j in range(2, i//2 + 1):
            if i % j == 0:
                is_prime=False
                break
        if is_prime:
            list_primes.append(i)

    print("Start: {}; End: {}".format(start, end))
    # print(list_primes)
    et = timeit.default_timer()
    elapsed_time = et - st
    print("Elapsed Time: {} s".format(elapsed_time))
    # plt.plot(list_primes)
    print(f"Prime numbers Count between {start} & {end}: {len(list_primes)}")
    len_primes = list(range(1, len(list_primes)+1))

    list_data = tuple(zip(list_primes, len_primes))
    np_data = np.array(list_data)

    np_primes = np.array(list_primes)
    #

    regressor = LinearRegression()
    regressor.fit(np_data, np_primes)
    print("Coefficient: {}".format(regressor.coef_))
    print("Intercept: {}".format(regressor.intercept_))
    # plt.scatter(len_primes, list_primes)
    # plt.plot(len_primes, list_primes)
    # plt.show()


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

primes(2, 500)
