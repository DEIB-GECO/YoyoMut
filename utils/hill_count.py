from datetime import datetime

import numpy as np
import pandas as pd
from utils.yo_yo_check import classify_mutation
import streamlit as st
from scipy.stats import linregress


@st.cache_data
def count_hills_threshold(df, threshold, min_length):
    date_format = '%Y-%m-%d'
    df['above-threshold'] = df['avg-proportion'] > threshold
    current_value = 0
    num_of_changes = 0
    curr_start = ''
    curr_end = ''
    hills_found = []
    above_threshold = df['above-threshold'].tolist()
    for i in range(len(above_threshold)):
        if above_threshold[i] != current_value:
            num_of_changes += 1
            current_value = 1 - current_value
            if num_of_changes % 2 == 1:
                curr_start = df.iloc[i]['start-date']
            else:
                curr_end = df.iloc[i]['end-date']
                date_diff = datetime.strptime(curr_end, date_format) - datetime.strptime(curr_start, date_format)
                if date_diff.days >= min_length:
                    hills_found.append({
                        'start-date': curr_start,
                        'end-date': curr_end,
                        'length-days': date_diff.days
                    })
    if num_of_changes % 2 == 1:
        curr_end = df.iloc[-1]['end-date']
        date_diff = datetime.strptime(curr_end, date_format) - datetime.strptime(curr_start, date_format)
        hills_found.append({
            'start-date': curr_start,
            'end-date': None,
            'length-days': date_diff.days
        })

    hills_found_df = pd.DataFrame(hills_found)
    return hills_found_df


@st.cache_data
def classify_mutations_threshold(df_dict, threshold, min_length):
    print('running all_mutation_classification function')
    hills_per_mutation = {}
    for mutation in df_dict:
        hills_df = count_hills_threshold(df_dict.get(mutation), threshold, min_length)
        hills_per_mutation.update({mutation: hills_df})

    classified_mutations = {}
    for mutation in hills_per_mutation:
        classified_mutations.update({mutation: {'data': df_dict[mutation],
                                                'hills': hills_per_mutation[mutation],
                                                'class': classify_mutation(hills_per_mutation[mutation], min_length)
                                                }
                                     })
    return classified_mutations


def get_slope(values):
    x = np.arange(len(values))  # use relative position (0, 1, ..., n-1) as x
    slope, _, _, _, _ = linregress(x, values)
    return slope


def count_hills_slope(df):
    started = False
    ended = True
    curr_start = None
    curr_end = None

    hills_found = []
    slopes = df["Slope"].tolist()

    i = 0
    while i < len(slopes):
        if not started and ended and slopes[i] >= 0.01:
            started = True
            ended = False
            curr_start = df.iloc[i]['start-date']
            while slopes[i] >= 0.01 and i < len(slopes) - 1:
                i += 1
        elif started and not ended and slopes[i] < -0.01:
            while slopes[i] <= -0.01 and i < len(slopes) - 1:
                i += 1
            started = False
            ended = True
            curr_end = df.iloc[i]['end-date']
            date_format = '%Y-%m-%d'
            date_diff = datetime.strptime(curr_end, date_format) - datetime.strptime(curr_start, date_format)
            hills_found.append({'start-date': curr_start,
                                'end-date': curr_end,
                                'length-days': date_diff.days
                                })
        i += 1

    if started and not ended:
        date_format = '%Y-%m-%d'
        date_diff = datetime.strptime('2025-03-30', date_format) - datetime.strptime(curr_start, date_format)
        hills_found.append({'start-date': curr_start,
                            'end-date': None,
                            'length-days': date_diff.days
                            })
    hills_found = pd.DataFrame(hills_found)
    return hills_found


@st.cache_data
def slope_algorithm(df, n):
    df['Slope'] = df['avg-proportion'].rolling(window=n).apply(get_slope, raw=True)
    hills = count_hills_slope(df)
    return hills


@st.cache_data
def classify_mutations_slope(mutations_data, n):
    hills_per_mutation = {}
    for mutation in mutations_data:
        hills_found = slope_algorithm(mutations_data[mutation], n)
        hills_per_mutation.update({mutation: hills_found})

    classified_mutations = {}
    for mutation in hills_per_mutation:
        classified_mutations.update({mutation: {'data': mutations_data[mutation],
                                                'hills': hills_per_mutation[mutation],
                                                'class': classify_mutation(hills_per_mutation[mutation], min_length=30)
                                                }
                                     })
    return classified_mutations