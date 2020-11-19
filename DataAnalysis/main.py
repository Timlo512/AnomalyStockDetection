from utils import *
import sys
import platform
import pandas as pd

# Define data_path
if platform.system() == 'Windows':
    data_path = '.\data\stock_port.csv'
else:
    data_path = './data/stock_port.csv'

def main():

    # load data
    df = load_data(data_path)

    # Convert df to sparse_matrix
    sparse_matrix = convert_data_sparse_matrix(df)

    print('Total shareholding: ', sparse_matrix.sum())

if __name__ == '__main__':
    main()