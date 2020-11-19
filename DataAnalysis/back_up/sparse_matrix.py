#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import csv
from scipy.sparse import lil_matrix
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = pd.read_csv(r"/Users/CliffordMan/Downloads/stock_port (1).csv") 
data.columns = ["name_of_ccass_participant","stock_code","shareholding"]
covariance=np.cov(data)
display(data.head())
display(data.shape)
BYTES_TO_MB_DIV = 0.000001
def print_memory_usage_of_data_frame(df):
    mem = round(df.memory_usage().sum() * BYTES_TO_MB_DIV, 3) 
    print("Memory usage is " + str(mem) + " MB")
    
print_memory_usage_of_data_frame(data)
data_one_hot = pd.get_dummies(data, columns=['name_of_ccass_participant', 'stock_code'])
display(data_one_hot.head())
display(data_one_hot.shape)
print_memory_usage_of_data_frame(data_one_hot)

def convert_to_sparse_pandas(df, exclude_columns=[]):
    """
    Converts columns of a data frame into SparseArrays and returns the data frame with transformed columns.
    Use exclude_columns to specify columns to be excluded from transformation.
    :param df: pandas data frame
    :param exclude_columns: list
        Columns not be converted to sparse
    :return: pandas data frame
    """
    df = df.copy()
    exclude_columns = set(exclude_columns)

    for (columnName, columnData) in df.iteritems():
        if columnName in exclude_columns:
            continue
        df[columnName] = pd.SparseArray(columnData.values, dtype='uint8')

    return df

data_one_hot_sparse = convert_to_sparse_pandas(data_one_hot, exclude_columns=['shareholding'])
display(data_one_hot_sparse.dtypes)
print_memory_usage_of_sparse_data_frame(data_one_hot_sparse)

data_one_hot_sparse = pd.get_dummies(data, columns=['name_of_ccass_participant', 'stock_code'], sparse=True)
display(data_one_hot_sparse.dtypes)
print_memory_usage_of_data_frame(data_one_hot_sparse)

y = data_one_hot['shareholding']
X = data_one_hot[data_one_hot.columns.difference(['shareholding'])]
y_sparse = data_one_hot_sparse['shareholding']
X_sparse = data_one_hot_sparse[data_one_hot_sparse.columns.difference(['shareholding'])]
print_memory_usage_of_data_frame(X)
print_memory_usage_of_data_frame(X_sparse)


# In[ ]:




vector_dict = {'Pandas dataframe': [X,y],
    'Sparse pandas dataframe': [X_sparse, y_sparse]}

for key, item in vector_dict.items():
    print(key)
    
    start = time.time()
    X_train, X_test, y_train, y_test = train_test_split(item[0], item[1], test_size=0.3, random_state=42)
    end = time.time()
    duration = round(end-start, 2)
    print("Train-test split: " + str(duration) + " secs")
    
    start = time.time()
    model = LogisticRegression(random_state=0, multi_class='ovr', solver = 'liblinear')
    model.fit(X_train, y_train)
    end = time.time()
    duration = round(end-start, 2)
    print("Training: " + str(duration) + " secs")
    print("\n")


# In[ ]:



def data_frame_to_scipy_sparse_matrix(df):
    """
    Converts a sparse pandas data frame to sparse scipy csr_matrix.
    :param df: pandas data frame
    :return: csr_matrix
    """
    arr = lil_matrix(df.shape, dtype=np.float32)
    for i, col in enumerate(df.columns):
        ix = df[col] != 0
        arr[np.where(ix), i] = 1

    return arr.tocsr()

def get_csr_memory_usage(matrix):
    mem = (X_csr.data.nbytes + X_csr.indptr.nbytes + X_csr.indices.nbytes) * BYTES_TO_MB_DIV
    print("Memory usage is " + str(mem) + " MB")

y_csr = y_sparse
X_csr = data_frame_to_scipy_sparse_matrix(X_sparse)
get_csr_memory_usage(X_csr)

vector_dict = {'Pandas dataframe': [X,y],
    'Sparse pandas dataframe': [X_sparse, y_sparse],
    'Scipy sparse matrix': [X_csr, y_csr]
    }

for key, item in vector_dict.items():
    print(key)
    
    start = time.time()
    X_train, X_test, y_train, y_test = train_test_split(item[0], item[1], test_size=0.3, random_state=42)
    end = time.time()
    duration = round(end-start, 2)
    print("Train-test split: " + str(duration) + " secs")
    
    start = time.time()
    model = LogisticRegression(random_state=0, multi_class='ovr', solver = 'liblinear')
    model.fit(X_train, y_train)
    end = time.time()
    duration = round(end-start, 2)
    print("Training: " + str(duration) + " secs")
    print("\n")


# In[ ]:




