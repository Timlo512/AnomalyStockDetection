import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import re

def convert_data_sparse_matrix(df, row_label = 'stock_code', col_label = 'name_of_ccass_participant', value_label = 'shareholding'):
    """
        Pivot table
    """
    try:
        # Prepare zero matrix
        row_dim = len(df[row_label].unique())
        col_dim = len(df[col_label].unique())
        sparse_matrix = np.zeros((row_dim, col_dim))

        # Prepare label to index dictionaries
        row_ind_dict = {label: ind for ind, label in enumerate(sorted(df[row_label].unique().tolist()))}
        col_ind_dict = {label: ind for ind, label in enumerate(sorted(df[col_label].unique().tolist()))}

        # Transform row_label column and col_label column to index
        df['row_ind'] = df[row_label].apply(lambda x: row_ind_dict[x])
        df['col_ind'] = df[col_label].apply(lambda x: col_ind_dict[x])

        for ind, row in df.iterrows():
            # Get index and shareholding
            row_ind = row['row_ind']
            col_ind = row['col_ind']
            value = row[value_label]
            
            # Assign to sparse matrix
            sparse_matrix[row_ind, col_ind] += value

        return sparse_matrix, row_ind_dict, col_ind_dict
    except Exception as e:
        print(e)
        return None

def load_data(data_path):

    # Read csv files
    df = pd.read_csv(data_path)

    # Convert stock code to formatted string
    df['stock_code'] = df['stock_code'].apply(lambda x: ('00000' + str(x))[-5:])

    return df

def f_score(y_truth, y_pred, beta = 1):
    
    try:
        # Run confusion_matrix
        tn, fp, fn, tp = confusion_matrix(y_truth, y_pred).ravel()
        
        precision_value = precision(tp, fp)
        recall_value = recall(tp, fn)
        # print recall
        print('True positive: {}, True Negative: {}, False Positive: {}, False Negative: {}'.format(tp, tn, fp, fn))
        print('Precision is ', format(precision_value * 100, '.2f'), '%')
        print('Recall is ', format(recall_value * 100, '.2f'), '%')
        
        return (1 + beta**2) * (precision_value * recall_value) / ((beta**2 * precision_value + recall_value))
    except Exception as e:
        print(e)
        return None

def precision(tp, fp):
    return tp / (tp + fp)

def recall(tp, fn):
    return tp / (tp + fn)

def get_truth_label(path, threshold = 0.3):
    # Load dataset
    df = pd.read_csv(path)

    # preprocess the data in order to get a proper data structure
    df = df.set_index('Unnamed: 0').transpose().dropna()
    df = df.reset_index()
    df['index'] = df['index'].apply(lambda x: retrieve_stock_code(x))
    df = df.set_index('index')

    # Define col_dim and empty dataframe
    col_dim = len(df.columns)
    temp = pd.DataFrame()

    # Create a list of column name without the first element
    first_dim = df.columns[0]
    col_list = df.columns.to_list()
    col_list.remove(first_dim)

    for col in col_list:
        # Assign the col to second_dim, as current date
        second_dim = col

        # Calculate the daily % change of stock price
        temp[col] = (df[second_dim] - df[first_dim]) / df[first_dim]

        # Assign the col to first dim, as previous date
        first_dim = col

    result = np.sum(temp > threshold, axis = 1)

    return {stock_code:1 if count > 0 else 0 for stock_code, count in result.items()}

def retrieve_stock_code(x):
    d = re.search('[0-9]*', x)
    if d:
        return ('00000' + d.group(0))[-5:]
    else:
        return None

def cluster_predict(label, min_pts = 'auto'):
    """
        Input: an array of clsutered label for each instance
        return: an array of anomal label for each instance
    """
    try:
        # Get Unqiue label and its counts
        (unique, counts) = np.unique(label, return_counts = True)
    
        # Define minimum points that it should have in a cluster, if auto, it will take the min count
        if min_pts == 'auto':
            min_pts = min(counts)
            print('Minimum points of a cluster among the clusters: ', min_pts)
        else:
            min_pts = int(min_pts)

        # Prepare label_dict for mapping
        label_dict = {label: 0 if count > min_pts else 1 for label, count in zip(unique, counts)}

        # Map label_dict to label
        return np.array([label_dict[i] for i in label])
    except Exception as e:
        print(e)
        return None
