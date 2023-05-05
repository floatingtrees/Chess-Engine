#import tensorflow
import numpy as np
import timeit

x = np.random.rand(1, 1024).astype("float16")
print(type(x))
layer1 = np.random.rand(1024, 1024).astype("float16")
bias1 = np.random.rand(1, 1024).astype("float16")
layer2 = np.random.rand(1024, 1).astype("float16")



start = timeit.default_timer()
print("starting")

for i in range(500):
    v = (x @ layer1 + bias1) @ layer2

print(timeit.default_timer() - start)
