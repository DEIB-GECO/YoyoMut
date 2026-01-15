import os

import pandas as pd

from data_collection.data_collection_all_protein import collect_data
from utils.smoothing_data import smooth_data_per_days, smooth_data_per_num_of_sequences


def data_preparation():
    print("Data preparation:")
    data_path = '../data/all_protein_data/'
    folders = os.listdir(data_path)

    print(folders)
    for folder in folders:
        print("Currently: ", folder)
        data_path = f'../data/all_protein_data/{folder}/'
        files = os.listdir(data_path)
        if len(files) == 0:
            collect_data()
        dfs_per_days = []
        dfs_per_seq = []
        for i in range(len(files)):
            file = files[i]
            if i % 100 == 0:
                print(f"{i} of {len(files)}\n")
            smoothed_data = smooth_data_per_days(file, data_path)
            df = pd.DataFrame(smoothed_data)
            df['name'] = file
            dfs_per_days.append(df)
            smoothed_data = smooth_data_per_num_of_sequences(file, data_path)
            df = pd.DataFrame(smoothed_data)
            df['name'] = file
            dfs_per_seq.append(df)
        df_days = pd.concat(dfs_per_days)
        os.makedirs('../data/smoothed_protein_data/', exist_ok=True)
        df_days.to_csv('../data/smoothed_protein_data/' + folder + '_days.csv')
        df_seq = pd.concat(dfs_per_seq)
        df_seq.to_csv('../data/smoothed_protein_data/' + folder + '_seq.csv')


