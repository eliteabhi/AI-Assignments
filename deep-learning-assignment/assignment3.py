import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

from typing import List, Any, Tuple, Optional

#----------------------------------------------------------------
#----------------------------------------------------------------

# Load the data - training as well as testing

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar100.load_data(label_mode='fine')


print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

# Prepare the data that can be used by the next step - creating and training the DL model

x_train = x_train.astype( 'float32' ) / 255.0
x_test = x_test.astype( 'float32' ) / 255.0


# The data from TensforFlow and Keras will only have integer class labels. Each of those 100 integer class labels correspond to the following names, in the correct order
fine_labels = ['apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur', 'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone', 'television', 'tiger', 'tractor', 'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm']

# These are the string labels for the 20 superclasses. You may not need to use this at all, just provided here for reference.
coarse_labels = ['aquatic_mammals', 'fish', 'flowers', 'food_containers', 'fruit_and_vegetables', 'household_electrical_devices', 'household_furniture', 'insects', 'large_carnivores', 'large_man-made_outdoor_things', 'large_natural_outdoor_scenes', 'large_omnivores_and_herbivores', 'medium_mammals', 'non-insect_invertebrates', 'people', 'reptiles', 'small_mammals', 'trees', 'vehicles_1', 'vehicles_2']

#----------------------------------------------------------------
#----------------------------------------------------------------

plt.figure( figsize=(20,20) )
classes_displayed = set()
num_images = 0

for i in range(len(x_train)):
    label = y_train[i][0]
    if label not in classes_displayed:
        plt.subplot(10, 10, num_images+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(x_train[i])
        plt.xlabel(fine_labels[label])
        classes_displayed.add(label)
        num_images += 1

    if num_images >= 100:
        break

plt.tight_layout()
plt.show()

#----------------------------------------------------------------
#----------------------------------------------------------------

y_train_categorical = keras.utils.to_categorical( y_train, num_classes=100 )
y_test_categorical = keras.utils.to_categorical( y_test, num_classes=100 )

model = keras.models.Sequential()

model.add( Conv2D( 32, ( 3, 3 ), activation='relu', input_shape=( 32, 32, 3 ) ) )
model.add( MaxPooling2D( ( 2, 2 ) ) )

model.add( Conv2D( 64, ( 3, 3 ), activation='relu' ) )
model.add( MaxPooling2D( ( 2, 2 ) ) )

model.add( Conv2D( 128, ( 3, 3 ), activation='relu' ) )
model.add( MaxPooling2D( ( 2, 2 ) ) )

model.add( Flatten() )
model.add( Dense( 128, activation='relu' ) )
model.add( Dropout( 0.5 ) )
model.add( Dense( 100, activation='softmax' ) )

model.compile( optimizer=Adam( learning_rate=0.001 ),
              loss='categorical_crossentropy',
              metrics=[ 'accuracy' ] )

model.summary()

history = model.fit( x_train, y_train_categorical,
                    epochs=20,
                    batch_size=64,
                    validation_split=0.2 )
test_loss, test_acc = model.evaluate( x_test, y_test_categorical )
print( f"Test accuracy: { test_acc:%0.4f }" )
