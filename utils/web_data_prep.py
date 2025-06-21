import os
import re

import streamlit as st
import pandas as pd

from utils.name_conversion import get_name, get_position, get_aa_name


@st.cache_resource
def load_data():
    files = os.listdir('data/smoothed_protein_data')
    smoothed_by_days = {}
    smoothed_by_seq = {}
    for file in files:
        protein = file.split('_')[0]
        df = pd.read_csv('data/smoothed_protein_data/' + file)
        dict_of_dfs = {get_name(key): group for key, group in df.groupby('name')}
        if 'days' in file:
            smoothed_by_days[protein] = dict_of_dfs
        elif 'seq' in file:
            smoothed_by_seq[protein] = dict_of_dfs
    with open("data/metadata/last_date.txt", 'r') as f:
        last_date = f.read()
        st.session_state.last_date = last_date
    return smoothed_by_days, smoothed_by_seq


def get_total_proportion(data):
    total_count = data['total-count'].sum()
    total_mutation_count = (data['total-count'] * data['avg-proportion']).sum()
    return total_mutation_count / total_count


def get_potential_residues(data):
    potential_residues = {}
    potential_residues_string = {}
    for protein in data:
        potential_residues[protein] = {}
        for residue in data[protein]:
            position = get_position(residue)
            aa_name = get_aa_name(residue)
            if aa_name == "" or aa_name == '.':
                continue
            total_proportion = get_total_proportion(data[protein][residue])
            if total_proportion < 0.001:
                continue
            if position not in potential_residues[protein]:
                potential_residues[protein][position] = []
            potential_residues[protein][position].append((aa_name, total_proportion))
        potential_residues_string[protein] = {}
        for position in potential_residues[protein]:
            potential_residues[protein][position].sort(key=lambda x: x[1], reverse=True)
            tmp_string = ""
            for pair in potential_residues[protein][position]:
                tmp_string += f"{pair[0]}={pair[1] * 100:.2f}%, "
            potential_residues_string[protein][position] = tmp_string[:-2]
    return potential_residues_string


def sort_by_residue_number(residue_list):
    sorted_residues = sorted(residue_list, key=lambda x: int(re.search(r'\d+', x).group()))
    return sorted_residues
