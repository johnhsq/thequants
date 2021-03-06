import numpy as np

array = np.arange(10)

print(array)
print(type(array))
print(array.dtype)
print('-'*50)

float_arr = array / 2

print(float_arr)
print(type(float_arr))
print(float_arr.dtype)
print('-'*50)

# cast float64 to int64
int_arr = float_arr.astype(np.int64)

print(int_arr)
print(type(int_arr))
print(int_arr.dtype)