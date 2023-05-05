#import tensorflow
import tensorflow as tf
import timeit
from tensorflow import keras
from tensorflow.keras import layers

embed_dims = 32
dropout_rate = 0.2

inputs1 = keras.Input(shape = (1024)) #baseline: 178.7 
 #
x = layers.Dense(1024, activation = 'relu')(inputs1)
x = layers.Dropout(0.2)(x)
output = layers.Dense(1)(x)
model = keras.Model(inputs1, output)
model.compile(keras.optimizers.Adam(), 'MSE', ["mean_absolute_error"], steps_per_execution = 1)
print(model.summary())


feeder = tf.sparse.SparseTensor(indices=[[0, 3], [0, 4]],
                      values=[10, 20],
                      dense_shape=[1, 1024])

v = model.predict(feeder)

start = timeit.default_timer()
print("starting")

for i in range(5000):
	x = model(feeder)

print(timeit.default_timer() - start)
