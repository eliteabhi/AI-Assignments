# import all required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Union, Any, List
from copy import deepcopy

# ----------------------------------------------------------------

# Assume that the data files are in the following folder -- THIS WILL BE USED BY THE TA
basePath: str = r"/content/drive/My Drive/Colab Notebooks/Artificial Intelligence/Data/"
basePath: str = r'./datasets/'

# ----------------------------------------------------------------

# Data file name variables
gd_training_dataset_path: str = f'{ basePath }gd-train.dat'
gd_test_dataset_path: str = f'{ basePath }gd-test.dat'

# ----------------------------------------------------------------

# Read the training and testing data files
gd_training_dataset_df: pd.DataFrame = pd.read_table( gd_training_dataset_path, delimiter='	' )
gd_test_dataset_df: pd.DataFrame = pd.read_table( gd_test_dataset_path, delimiter='	' )

# ----------------------------------------------------------------

# Activation Function - implement Sigmoid
def activation_function( h: np.float64 ) -> np.float64:

    return 1 / ( 1 + np.exp( -h ) )

# ----------------------------------------------------------------

# Train the model using the given training dataset and the learning rate
# return the "weights" learnt for the perceptron - include the weight assocaited with bias as the last entry

def train( train_data: pd.DataFrame, learning_rate: float = 0.05 ) -> np.ndarray:

    weights: np.ndarray = np.zeros( train_data.shape[1] , dtype=float )

    for _, row in train_data.iterrows():
        input_field: np.ndarray = row.drop( 'C' ).to_numpy()
        label: int = row[ 'C' ]

        h: np.float64 = np.dot( weights[:-1], input_field ) + weights[-1]

        z: np.float64 = activation_function( h )

        # weights_copy: np.ndarray = np.copy( weights )
        weights[:-1] += learning_rate * ( label - z ) * input_field
        weights[-1] += learning_rate * ( label - z )

    return weights

# ----------------------------------------------------------------

# Test the model (weights learnt) using the given test dataset
# return the accuracy value

def test( test_data: pd.DataFrame, weights: np.ndarray, threshold: float=0.5 ) -> float:
    total_tests: int = test_data.shape[0]

    if total_tests == 0:
        return 0

    correct_predictions: int = 0

    for _, row in test_data.iterrows():
        input_field: np.ndarray = row.drop( 'C' ).to_numpy()
        target: int = row[ 'C' ]

        h: np.float64 = np.dot( weights[:-1], input_field ) + weights[ -1 ]

        prediction: int = 1 if activation_function( h ) >= threshold else 0

        if prediction == target:
            correct_predictions += 1

    accuracy: float = correct_predictions / total_tests

    return accuracy

# ----------------------------------------------------------------

# Gradient Descent function
def gradient_descent( df_train: pd.DataFrame, df_test: pd.DataFrame, learning_rate: float=0.05, threshold: float=0.5, weights: np.ndarray = np.array( None ) ) -> Tuple[ float, float ]:

    if not weights.shape:
        weights = train( train_data=df_train, learning_rate=learning_rate )

    training_accuracy: float = test( test_data=df_train, weights=weights, threshold=threshold )
    testing_accuracy: float = test( test_data=df_test, weights=weights, threshold=threshold )

    return ( training_accuracy, testing_accuracy )

# ----------------------------------------------------------------

# Threshold of 0.5 will be used to classify the instance for the test. If the value is >= 0.5, classify as 1 or else 0.
thresh: float = 0.5

# ----------------------------------------------------------------


# Main algorithm loop

start: float = 0.05
stop: float = 1.0
step: float = 0.01

accuracies_shape: int = int( ( stop - start ) / step ) + 1
training_accuracies: np.ndarray = np.zeros( shape=accuracies_shape )
testing_accuracies:np.ndarray = np.zeros( shape=accuracies_shape )

for lr, i in zip( np.arange( start, stop + step, step, dtype=float ), range( training_accuracies.shape[0] ) ):
    training_acc, testing_acc = gradient_descent( df_train=gd_training_dataset_df, df_test=gd_test_dataset_df, learning_rate=lr, threshold=thresh )
    print( 'Accuracy for LR of %.2f on Training set = %.2f' % ( lr, training_acc ) )
    print( 'Accuracy for LR of %.2f on Testing set = %.2f\n' % ( lr, testing_acc ) )

    training_accuracies[ i ] = training_acc * 100
    testing_accuracies[ i ] = testing_acc * 100

# ----------------------------------------------------------------

# Plot the graphs for accuracy results.

plt.plot( np.arange( start, stop + step, step, dtype=float ), training_accuracies, label='Training Accuracy (in %)' )
plt.plot( np.arange( start, stop + step, step, dtype=float ), testing_accuracies, label='Testing Accuracy (in %)' )
plt.xlabel( 'Learning Rate' )
plt.ylabel( 'Accuracy' )
plt.legend()
plt.show()

# ----------------------------------------------------------------

# Data file name variables
id3_training_dataset_path = f"{ basePath }id3-train.dat"
id3_testing_dataset_path = f"{ basePath }id3-test.dat"

# ----------------------------------------------------------------

# Pseudocode for the ID3 algorithm. Use this to create function(s).

# def ID3( dataset: pd.DataFrame, root, attributes_remaining ):
    

# def ID3(data, root, attributesRemaining):
    # If you reach a leaf node in the decision tree and have no examples left or the examples are equally split among multiple classes
        # Choose and the class that is most frequent in the entire training set and return the updated tree
    # If all the instances have only one class label
        # Make this as the leaf node and use the label as the class value of the node and return the updated tree
    # If you reached a leaf node but still have examples that belong to different classes (there are no remaining attributes to be split)
        # Assign the most frequent class among the instances at the leaf node and return the updated tree
    # Find the best attribute to split by calculating the maximum information gain from the attributes remaining by calculating the entropy
    # Split the tree using the best attribute and recursively call the ID3 function using DFS to fill the sub-tree
    # return the root as the tree


# Entropy calculation
def entropy(y: pd.Series) -> float:
    value_counts = y.value_counts(normalize=True)
    return -1 * sum(value_counts * np.log2(value_counts))

# Information Gain calculation
def information_gain( dataset: pd.DataFrame, attribute: str, target_attribute: str ) -> float:
    total_entropy: float = entropy(dataset[target_attribute])
    weighted_entropy: float = 0.0

    for _, subset in dataset.groupby( attribute ):
        subset_entropy: float = entropy(subset[target_attribute])
        weighted_entropy += ( subset.shape[0] / dataset.shape[0] ) * subset_entropy

    return total_entropy - weighted_entropy

# ID3 Algorithm
def ID3( dataset: pd.DataFrame, target_attribute: str, attributes_remaining: List[ str ] ) -> Union[ str, Dict[ str, Any ] ]:
    
    # Check if all target values are the same
    unique_targets: np.ndarray = np.unique( dataset[ target_attribute ] )
    if unique_targets.shape[0] == 1:
        return unique_targets[0]

    # Check if no more attributes to split
    if not attributes_remaining:
        return dataset[ target_attribute ].mode()[0]

    # Calculate information gain for each attribute
    gains: Dict[ str, float ] = { attr: information_gain( dataset, attr, target_attribute ) for attr in attributes_remaining }

    # Find the attribute with the maximum information gain
    best_attribute: str = max( gains )

    # Create a new tree node
    tree: Dict[ str, Any ] = { best_attribute: {} }

    # Recursive splitting
    remaining_attributes: List[str] = [ attr for attr in attributes_remaining if attr != best_attribute ]
    for value, subset in dataset.groupby( best_attribute ):
        subtree = ID3( subset, target_attribute, deepcopy( remaining_attributes ) )
        tree[ best_attribute ][ value ] = subtree
    
    return tree
