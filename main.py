import sys, os
from keras.models import Sequential
from keras.layers import Dense, Conv3D, Flatten, MaxPooling3D
from utility_functions import opening_files
from create_partition import create_partition_and_labels
from DataGenerator import DataGenerator

# get arguments
# _, generate_samples = sys.argv
root_path = os.getcwd()
sample_dir = "/".join([root_path, "samples"])

# create partition
partition, labels = create_partition_and_labels(sample_dir, 0.8, randomise=True)

# generators
# Parameters
params = {'dim': (256, 256, 32),
          'batch_size': 16,
          'n_channels': 1,
          'shuffle': True}

training_generator = DataGenerator(partition['train'], labels, **params)
validation_generator = DataGenerator(partition['validation'], labels, **params)

# train model
model = Sequential()
model.add(Conv3D(64, kernel_size=(5, 5, 3), strides=(1, 1, 1), activation='relu', padding="same",
                 input_shape=(None, None, None, 1)))

model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2)))

model.add(Conv3D(64, kernel_size=(3, 3, 3), strides=(1, 1, 1), activation='relu', padding="same"))

model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2)))

model.add(Conv3D(64, kernel_size=(3, 3, 3), strides=(1, 1, 1), activation='relu', padding="same"))

model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2)))

model.add(Conv3D(64, kernel_size=(3, 3, 3), strides=(1, 1, 1), activation='relu', padding="same"))

model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2)))

model.add(Conv3D(1024, kernel_size=(16, 16, 1), strides=(1, 1, 1), activation='relu'))

model.add(Conv3D(3, kernel_size=(1, 1, 1), strides=(1, 1, 1)))
# output_shape=(1, 1, 1, 3)

"""
for layer in model.layers:
    print(layer.name)
    print(layer.input_shape)
    print(layer.output_shape)
"""

model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'])

# train the model
model.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=True,
                    workers=6,
                    epochs=10)

model.save('main-model.h5')

# show predictions

