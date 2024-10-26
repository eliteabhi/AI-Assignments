# import all required libraries
import pandas as pd
import numpy as np
from typing import Tuple

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

    weights: np.ndarray = np.zeros( train_data.shape[1] , dtype=float );

    for _, row in train_data.iterrows():
        input_field: np.ndarray = row.drop( 'C' ).to_numpy()
        label: int = row[ 'C' ]

        h: np.ndarray = np.dot( weights[:-1], input_field ) + weights[-1]

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

        prediction: np.int64 = 1 if activation_function( h ) >= threshold else 0
        
        if prediction == target:
            correct_predictions += 1

    accuracy: float = correct_predictions / total_tests

    return accuracy

# ----------------------------------------------------------------

# Gradient Descent function
def gradient_descent( df_train, df_test, learning_rate=0.05, threshold=0.5 ) -> Tuple[ float, float ]:

    weights: np.ndarray = train( train_data=df_train, learning_rate=learning_rate )
    
    training_accuracy: float = test( test_data=df_train, weights=weights, threshold=threshold )
    testing_accuracy: float = test( test_data=df_test, weights=weights, threshold=threshold )

    return ( training_accuracy, testing_accuracy )

# ----------------------------------------------------------------

# Threshold of 0.5 will be used to classify the instance for the test. If the value is >= 0.5, classify as 1 or else 0.
threshold: float = 0.7

# ----------------------------------------------------------------

start: float = 0.05
stop: float = 1.0
step: float = 0.01

for learning_rate in np.arange( start, stop + step, step, dtype=float ):
    training_accuracy, testing_accuracy = gradient_descent( df_train=gd_training_dataset_df, df_test=gd_test_dataset_df, learning_rate=learning_rate, threshold=threshold )
    print( 'Accuracy for LR of %.2f on Training set = %.2f' % ( learning_rate, training_accuracy ) )
    print( 'Accuracy for LR of %.2f on Testing set = %.2f\n' % ( learning_rate, testing_accuracy ) )

# Main algorithm loop
# Loop through all the different learning rates [0.05, 1]
    # For each learning rate selected, call the gradient descent function to obtain the train and test accuracy values
    # Print both the accuracy values as "Accuracy for LR of 0.1 on Training set = x %" OR "Accuracy for LR of 0.1 on Testing set = x %"