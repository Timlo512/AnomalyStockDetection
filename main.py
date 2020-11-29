import sys
import platform
import re

import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

from DataAnalysis.utils import *

# Define data_path
if platform.system() == 'Windows':
    data_path = '.\DataAnalysis\data\stock_port.csv'
else:
    data_path = './DataAnalysis/data/stock_port.csv'

# Define the truth_path
if platform.system() == 'Windows':
    truth_path = '.\DataAnalysis\data\STOCK.csv'
else:
    truth_path = './DataAnalysis/data/STOCK.csv'

def main():

    print('')
    print('>> Preparing the matrix to fit into the models...')
    # Load dataset from data path
    df = load_data(data_path)

    # Convert df to sparse matrix
    sp_matrix, row_ind_dict, col_ind_dict = convert_data_sparse_matrix(df)
    ind_row_dict = {ind: stock_code for stock_code, ind in row_ind_dict.items()}
    row_dim = sp_matrix.shape[0]

    # Calculate shareholding % by stock_code
    sp_matrix_stock = sp_matrix / np.sum(sp_matrix, axis = 1).reshape(row_dim, -1)

    # Apply K-Mean to sp_matrix_stock
    n_clusters = 30
    min_pts = 25
    kmeans = KMeans(n_clusters = n_clusters, random_state=0).fit(sp_matrix_stock)
    prediction = cluster_predict(kmeans.labels_, min_pts = min_pts)

    print('')
    print('>> The Anomaly Stock predicted by K-means Algorithm')
    result = [ind_row_dict[ind] for ind, predict in enumerate(list(prediction)) if predict == 1]
    print(result)

    # Apply DBSCAN
    eps = 0.2
    min_samples = 20
    min_pts = 30
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(sp_matrix_stock)
    prediction = cluster_predict(clustering.labels_, min_pts=min_pts)

    print('')
    print('>> The Anomaly Stock predicted by DBSCAN Algorithm')
    result = [ind_row_dict[ind] for ind, predict in enumerate(list(prediction)) if predict == 1]
    print(result)

    # Apply Isolation Forest
    n_estimators = 200
    max_features = 100
    contamination = 0.1
    max_samples = 256
    clf = IsolationForest(n_estimators=n_estimators, max_features=max_features, 
                        contamination=contamination, max_samples=max_samples,
                        random_state=0).fit(sp_matrix_stock)
    label = clf.predict(sp_matrix_stock)
    prediction = [1 if i == -1 else 0 for i in label]

    print('')
    print('>> The Anomaly Stock predicted by Isolation Forest Algorithm')
    result = [ind_row_dict[ind] for ind, predict in enumerate(list(prediction)) if predict == 1]
    print(result)


if __name__ == '__main__':
    main()
