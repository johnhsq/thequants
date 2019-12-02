import numpy as np

prices = np.array([1, 3, -2, 9, 5, 7, 2])
print(prices)

# buy one share of stock when the price is above 2 dollars and the buy 3 more shares when it's above 4 dollars.
signal_one = prices > 2
signal_three = prices > 4

print(signal_one)
print(signal_three)

signal_one = signal_one.astype(np.int)
signal_three = signal_three.astype(np.int)

print(signal_one)
print(signal_three)

pos_one = 1 * signal_one
pos_three = 3 * signal_three

print(pos_one)
print(pos_three)

long_pos = pos_one + pos_three

print(long_pos)