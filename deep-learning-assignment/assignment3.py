import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import pickle
from typing import List, Any, Tuple, Optional

# Load the data - training as well as testing
def unpickle_to_df( filepath: str ) -> pd.DataFrame:
    with open( filepath, 'rb' ) as file:
        data: dict = pickle.load( file, encoding='bytes' )
    return pd.DataFrame( data[b'data'].T, columns=data[b'filenames'])

DATASET_ROOT_DIR: str = r'./cifar-10-batches-py'

# Define the dataset files
DATASET_FILES: List[ str ] = [
    f'{ DATASET_ROOT_DIR }/data_batch_1',
    f'{ DATASET_ROOT_DIR }/data_batch_2',
    f'{ DATASET_ROOT_DIR }/data_batch_3',
    f'{ DATASET_ROOT_DIR }/data_batch_4',
    f'{ DATASET_ROOT_DIR }/data_batch_5',
    f'{ DATASET_ROOT_DIR }/test_batch'
]

dataset_batched: List[ pd.DataFrame ] = [ unpickle_to_df( dataset_filepath ) for dataset_filepath in DATASET_FILES ]

# Prepare the data that can be used by the next step - creating and training the DL model

def prepare_data( dataset_batched: List[ pd.DataFrame ] ) -> Tuple[ np.ndarray, np.ndarray, np.ndarray, np.ndarray ]:
    images: List[ np.ndarray ] = []
    fine_labels: List[ int ] = []
    coarse_labels: List[ int ] = []

    for dataset in dataset_batched:
        images.extend( dataset.iloc[:, :].values / 255.0 ) 
        fine_labels.extend( dataset.iloc[:, -1].values )
        coarse_labels.extend( dataset.iloc[:, -2].values )

    return np.array( images ), np.array( fine_labels ), np.array( coarse_labels )

# The data from TensforFlow and Keras will only have integer class labels. Each of those 100 integer class labels correspond to the following names, in the correct order
fine_labels: List[ str ] = ['apple', 'aquarium_fish', 'baby', 'bear', 'beaver', 'bed', 'bee', 'beetle', 'bicycle', 'bottle', 'bowl', 'boy', 'bridge', 'bus', 'butterfly', 'camel', 'can', 'castle', 'caterpillar', 'cattle', 'chair', 'chimpanzee', 'clock', 'cloud', 'cockroach', 'couch', 'crab', 'crocodile', 'cup', 'dinosaur', 'dolphin', 'elephant', 'flatfish', 'forest', 'fox', 'girl', 'hamster', 'house', 'kangaroo', 'keyboard', 'lamp', 'lawn_mower', 'leopard', 'lion', 'lizard', 'lobster', 'man', 'maple_tree', 'motorcycle', 'mountain', 'mouse', 'mushroom', 'oak_tree', 'orange', 'orchid', 'otter', 'palm_tree', 'pear', 'pickup_truck', 'pine_tree', 'plain', 'plate', 'poppy', 'porcupine', 'possum', 'rabbit', 'raccoon', 'ray', 'road', 'rocket', 'rose', 'sea', 'seal', 'shark', 'shrew', 'skunk', 'skyscraper', 'snail', 'snake', 'spider', 'squirrel', 'streetcar', 'sunflower', 'sweet_pepper', 'table', 'tank', 'telephone', 'television', 'tiger', 'tractor', 'train', 'trout', 'tulip', 'turtle', 'wardrobe', 'whale', 'willow_tree', 'wolf', 'woman', 'worm']

# These are the string labels for the 20 superclasses. You may not need to use this at all, just provided here for reference.
coarse_labels: List[ str ] = ['aquatic_mammals', 'fish', 'flowers', 'food_containers', 'fruit_and_vegetables', 'household_electrical_devices', 'household_furniture', 'insects', 'large_carnivores', 'large_man-made_outdoor_things', 'large_natural_outdoor_scenes', 'large_omnivores_and_herbivores', 'medium_mammals', 'non-insect_invertebrates', 'people', 'reptiles', 'small_mammals', 'trees', 'vehicles_1', 'vehicles_2']


