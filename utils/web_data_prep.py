import os
import re

import streamlit as st
import pandas as pd

from data_collection.data_collection import collect_data
from utils.smoothing_data import smooth_data_per_num_of_sequences, smooth_data_per_days
from utils.name_conversion import get_name, get_position, get_aa_name


@st.cache_data
def data_preparation(by_days=False):
    print("Data preparation:")
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


def get_total_proportion(data):
    total_count = data['total-count'].sum()
    total_mutation_count = (data['total-count'] * data['avg-proportion']).sum()
    return total_mutation_count/total_count


def get_potential_residues(data):
    potential_residues = {}
    for residue in data:
        position = get_position(residue)
        aa_name = get_aa_name(residue)
        if aa_name == "":
            continue
        total_proportion = get_total_proportion(data[residue])
        if total_proportion < 0.001:
            continue
        if position not in potential_residues:
            potential_residues[position] = []
        potential_residues[position].append((aa_name, total_proportion))

        # iteriraj po svima, izracunaj postotak i onda spremi u dict di svejedno sve imas po pozicijama
        # ostale pozicije nece bit spremljene, bit ce samo empty value u dictu
        # total - imam u fileu?, brijem da da
        # i onda postotak je zapravo, all time proportion
        # i onda to strpam ko string u dict
    potential_residues_string = {}
    for position in potential_residues:
        potential_residues[position].sort(key=lambda x: x[1], reverse=True)
        tmp_string = ""
        for pair in potential_residues[position]:
            tmp_string += f"{pair[0]}={pair[1]*100:.2f}%, "
        potential_residues_string[position] = tmp_string[:-2]
    print(potential_residues)
    return potential_residues_string

def sort_by_residue_number(residue_list):
    sorted_residues = sorted(residue_list, key=lambda x: int(re.search(r'\d+', x).group()))
    return sorted_residues