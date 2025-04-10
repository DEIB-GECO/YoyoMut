import json
from collections.abc import Hashable

import pandas as pd
import requests
import streamlit as st
from utils.name_conversion import get_aa_parameter
from collections import defaultdict


def rename_lineage(name, aliases):
    base_name = name.split('.')[0]
    if base_name[0] == 'X':
        return name
    if base_name == 'A' or base_name == 'B':
        return name
    if base_name in aliases:
        name = aliases[base_name] + '.' + '.'.join(name.split('.')[1:])
    return name


def add_aliases(lineages, reverse_aliases):
    lin_list = lineages['Lineage'].tolist()
    lineages["Lineages (aliases)"] = lineages['Lineage'].astype(str)
    for lin in lin_list:
        aliases = []
        split_lin = lin.split('.')
        for i in range(1, len(split_lin)):
            prefix = '.'.join(split_lin[:i])
            rest = '.'.join(split_lin[i:])
            if prefix in reverse_aliases:
                print(f"found: ({prefix}:{reverse_aliases[prefix]})")
                print(f"appending: {reverse_aliases[prefix]}.{rest}")
                aliases.append(f"{reverse_aliases[prefix]}.{rest}")
        if len(aliases) > 0:
            lineages.loc[lineages['Lineage'] == lin, "Lineages (aliases)"] = f"{lin} ({', '.join(aliases)})"
    return lineages


def get_top_lineages(mutation, start_date, end_date):
    mutation_url = mutation.replace(':', '%3A')
    aa_param = get_aa_parameter(mutation_url)
    base_url = f"https://lapis.cov-spectrum.org/open/v2/sample/aggregated?{aa_param}&dateFrom={start_date}"  # dateFrom=2024-09-23&aminoAcidMutations=s%3A452&fields=nextcladePangoLineage"
    if end_date is not None:
        base_url += f"&dateTo={end_date}"
    url = base_url + "&fields=nextcladePangoLineage"
    response = requests.get(url).json()
    total = 0
    aggregated_lineages = defaultdict(float)
    if 'data' not in response:
        print(response)
        return

    with open('./utils/alias_key.json') as aliases_file:
        aliases = json.load(aliases_file)
        reverse_aliases = {}
        for key, value in aliases.items():
            if isinstance(value, Hashable):
                reverse_aliases.update({value:key})

    for entry in response['data']:
        key = entry["nextcladePangoLineage"]
        key = rename_lineage(key, aliases)
        value = entry["count"]
        total += value
        parts = key.split('.')
        for i in range(1, len(parts) + 1):
            parent = '.'.join(parts[:i])
            aggregated_lineages[parent] += value

    aggregated_lineages = pd.DataFrame(list(aggregated_lineages.items()), columns=["Lineage", "Count"])
    aggregated_lineages["Proportion"] = aggregated_lineages["Count"] * 100 / total
    if 'min_percentage' not in st.session_state:
        min_percentage = 30
    else:
        min_percentage = st.session_state.min_percentage
    aggregated_lineages = aggregated_lineages[aggregated_lineages["Proportion"] > min_percentage]
    aggregated_lineages["Lineage"] = aggregated_lineages["Lineage"] + '.*'

    aggregated_lineages = add_aliases(aggregated_lineages, reverse_aliases)

    top_lineages = aggregated_lineages.sort_values(by='Proportion', ascending=False).reset_index()

    return top_lineages


def get_lineage_for_hills(mutation, hills):
    found_lineages = {}
    for i in range(len(hills)):
        current_hill = hills.iloc[i]
        lineages = get_top_lineages(mutation, current_hill['start-date'], current_hill['end-date'])
        found_lineages[current_hill['start-date']] = lineages
    return found_lineages


def add_lineages(mutations):
    for mutation in mutations:
        if mutations[mutation]['class'] == 'no mutation':
            continue
        else:
            lineages = get_lineage_for_hills(mutation, mutations[mutation]['hills'])
            mutations[mutation]["lineages"] = lineages
