import pickle
import pandas

def unpickle_to_df(filepath: str) -> pandas.DataFrame:
    with open(filepath, 'rb') as file:
        data = pickle.load(file, encoding='bytes')
        return pandas.DataFrame(data[b'data'].T, columns=data[b'filenames'])

# Define the dataset files
DATASET_ROOT_DIR = r'./cifar-10-batches-py'
DATASET_FILES = [
    f'{ DATASET_ROOT_DIR }/data_batch_1',
    f'{ DATASET_ROOT_DIR }/data_batch_2',
    f'{ DATASET_ROOT_DIR }/data_batch_3',
    f'{ DATASET_ROOT_DIR }/data_batch_4',
    f'{ DATASET_ROOT_DIR }/data_batch_5',
    f'{ DATASET_ROOT_DIR }/test_batch'
]

SAVE_DIR: str = r'./unpickled_cifar-10'

# Save the dataset files in seperate directory
for file in DATASET_FILES:
    df = unpickle_to_df(file)
    df.to_csv(f'{SAVE_DIR}/{file.split("/")[-1].split(".")[0]}.csv', index=False)
