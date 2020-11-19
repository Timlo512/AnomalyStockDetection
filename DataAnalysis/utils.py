import pandas as pd
import numpy as np

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