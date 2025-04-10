import os
import streamlit as st
import pandas as pd

from data_collection.data_collection import collect_data
from utils.smoothing_data import smooth_data_per_num_of_sequences, smooth_data_per_days
from utils.name_conversion import get_name


@st.cache_data
def data_preparation(by_days=False):
    data_path = 'data/'
    # data_path = '../data_collection/data/test_data/'
    files = os.listdir(data_path)
    smoothed_data_files = {}
    # for file in files:
    if len(files) == 0:
        collect_data()
    for i in range(len(files)):
        file = files[i]
        if i % 100 == 0:
            print(f"{i} of {len(files)}\n")
        # time_frame = 7
        # overlap = 0
        if by_days:
            smoothed_data = smooth_data_per_days(file, data_path)
        else:
            smoothed_data = smooth_data_per_num_of_sequences(file, data_path)
        df = pd.DataFrame(smoothed_data)
        smoothed_data_files.update({get_name(file): df})
    return smoothed_data_files
