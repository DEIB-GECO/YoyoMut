import csv
import os
import time

import requests

from utils.confidence_interval import confidence_interval
from utils.name_conversion import is_unknown, get_unknown_name, get_file_name, get_protein_name


# Special characters used:
# - = deletion
# X = unknown destination amino acid
# *, replaced with Z = stop codon
# . = any destination amino acid


def is_data_up_to_date(latest_data_id):
    url = "https://lapis.cov-spectrum.org/open/v2/sample/aggregated"
    response = requests.get(url)
    if response.status_code == 200:
        dataVersion = response.json()['info']['dataVersion']
        return dataVersion == latest_data_id


def get_all_mutations(min_sequences=1000):
    all_mutations_url = "https://lapis.cov-spectrum.org/open/v2/sample/aminoAcidMutations?minProportion=0&orderBy=mutation"
    data = requests.get(all_mutations_url).json()['data']
    proteins = ['E', 'M', 'N', 'ORF1a', 'ORF1b', 'ORF3a', 'ORF6', 'ORF7a', 'ORF7b', 'ORF8', 'ORF9b', 'S']
    # proteins = ['S']
    filtered_mutations = {}
    for p in proteins:
        filtered_mutations[p] = []
    for mutation in data:
        if mutation['sequenceName'] in proteins and int(mutation['count']) >= min_sequences:
            protein = mutation['sequenceName']
            filtered_mutations[protein].append(protein + ":" + str(mutation['position']) + mutation['mutationTo'])
            if f"{protein}:" + str(mutation['position']) not in filtered_mutations[protein]:
                filtered_mutations[protein].append(f"{protein}:" + str(mutation['position']))
            if f"{protein}:" + str(mutation['position']) + "X" not in filtered_mutations[protein]:
                filtered_mutations[protein].append(f"{protein}:" + str(mutation['position']) + "X")
            if f"{protein}:" + str(mutation['position']) + "." not in filtered_mutations[protein]:
                filtered_mutations[protein].append(f"{protein}:" + str(mutation['position']) + ".")
    mutations = {}
    start_time = time.time()
    base_url = 'https://lapis.cov-spectrum.org/open/v2/sample/aggregated?'
    for protein in proteins:
        i = 0
        for mutation in filtered_mutations[protein]:
            start_time_mutation = time.time()
            if i % 10 == 0:
                print(f"{i} out of {len(filtered_mutations[protein])}")
            i += 1
            mutation_url = mutation.replace(':', '%3A')
            url = f"{base_url}aminoAcidMutations={mutation_url}&fields=date&orderBy=date"
            response = requests.get(url).json()
            mutations['dataVersion'] = response['info']['dataVersion']
            mutations[mutation] = response['data']
            end_time_mutation = time.time()
            print('for mutation: ', end_time_mutation - start_time_mutation)
    end_time = time.time()
    print('total time: ', end_time - start_time)
    return mutations


def get_all_insertions(min_sequences=1000):
    all_insertions_url = "https://lapis.cov-spectrum.org/open/v2/sample/aminoAcidInsertions?minProportion=0"
    data = requests.get(all_insertions_url).json()['data']
    proteins = ['S']

    filtered_insertions = {}
    for p in proteins:
        filtered_insertions[p] = []

    for insertion in data:
        if insertion['sequenceName'] in proteins and int(insertion['count']) >= min_sequences:
            protein = insertion['sequenceName']
            filtered_insertions[protein].append(
                f"ins_{protein}:{str(insertion['position'])}:{insertion['insertedSymbols']}")
            if f"ins_{protein}:" + str(insertion['position']) + "X" not in filtered_insertions[protein]:
                filtered_insertions[protein].append(f"ins_{protein}:{str(insertion['position'])}:X")
    insertions = {}
    start_time = time.time()
    base_url = 'https://lapis.cov-spectrum.org/open/v2/sample/aggregated?'
    for protein in proteins:
        for insertion in filtered_insertions[protein]:
            insertion_url = insertion.replace(':', '%3A')
            url = f"{base_url}aminoAcidInsertions={insertion_url}&fields=date&orderBy=date"
            response = requests.get(url).json()
            insertions['dataVersion'] = response['info']['dataVersion']
            insertions[insertion] = response['data']
    end_time = time.time()
    print('total time: ', end_time - start_time)
    return insertions


def json_to_csv(data):
    total_per_day_url = "https://lapis.cov-spectrum.org/open/v2/sample/aggregated?fields=date&orderBy=date"
    total_per_day = requests.get(total_per_day_url).json()
    if 'dataVersion' in data:
        data_version = data.pop('dataVersion')
    else:
        print(data)
        print("WARNING! No 'dataVersion' in data!")
        return
    if total_per_day['info']['dataVersion'] != data_version:
        print("WARNING! The data does not belong to the same version!")
        return

    for mutation in data:
        if is_unknown(mutation):
            continue

        mutation_dict = {}
        for d in data[mutation]:
            mutation_dict.update({d['date']: d['count']})

        unknown_name = get_unknown_name(mutation)
        unknown_dict = {}
        for d in data[unknown_name]:
            unknown_dict.update({d['date']: d['count']})

        csv_data = []
        for entry in total_per_day['data']:
            date = entry['date']
            date_count = entry['count']
            if date is None:
                continue
            if date not in unknown_dict:
                unknown_count = 0
            else:
                unknown_count = unknown_dict[date]
            total_count = date_count - unknown_count
            if date not in mutation_dict:
                count = 0
                proportion = 0
                ci_lower = 0
                ci_upper = 0
            else:
                count = mutation_dict[date]
                proportion = count / total_count
                ci_lower, ci_upper = confidence_interval(count, date_count)
            csv_data.append({'date': date,
                             'total_count': total_count,
                             'proportion': proportion,
                             'ci_lower': ci_lower,
                             'ci_upper': ci_upper})
        folder_name = get_protein_name(mutation)
        path = f'../data/all_protein_data/{folder_name}'
        os.makedirs(path, exist_ok=True)
        csv_file = open(f'{path}/{get_file_name(mutation)}', 'w', newline='')
        field_names = ['date', 'total_count', 'proportion', 'ci_lower', 'ci_upper']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(csv_data)
        csv_file.close()

    last_date = total_per_day['data'][-1]['date']
    with open('metadata/last_date.txt', 'w') as f:
        f.write(last_date)


def collect_data():
    print("Collecting mutation data...")
    mutations = get_all_mutations()
    json_to_csv(mutations)
    print("Finished collecting mutations.")
    print("Collecting insertion data...")
    insertions = get_all_insertions()
    json_to_csv(insertions)
    print("Finished collecting insertions.")


# collect_data()

def count_mutations_per_protein():
    all_mutations_url = "https://lapis.cov-spectrum.org/open/v2/sample/aminoAcidMutations?minProportion=0&orderBy=mutation"
    data = requests.get(all_mutations_url).json()['data']
    # proteins = ['E', 'M', 'N', 'ORF1a', 'ORF1b', 'ORF3a', 'ORF6', 'ORF7a', 'ORF7b', 'ORF8', 'ORF9b', 'S']
    counts = {}
    for mutation in data:
        protein = mutation['sequenceName']
        if int(mutation['count']) < 1000:
            continue
        if protein not in counts:
            counts[protein] = 1
        else:
            counts[protein] += 1

    for p in counts:
        print(p, counts[p])
