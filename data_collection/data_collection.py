import csv
import time

import requests

from utils.confidence_interval import confidence_interval
from utils.name_conversion import is_unknown, get_unknown_name, get_file_name


def is_data_up_to_date(latest_data_id):
    url = "https://lapis.cov-spectrum.org/open/v2/sample/aggregated"
    response = requests.get(url)
    if response.status_code == 200:
        dataVersion = response.json()['info']['dataVersion']
        return dataVersion == latest_data_id


def get_all_mutations(min_sequences=1000):
    all_mutations_url = "https://lapis.cov-spectrum.org/open/v2/sample/aminoAcidMutations?minProportion=0&orderBy=mutation"
    data = requests.get(all_mutations_url).json()['data']
    filtered_mutations = []
    for mutation in data:
        if mutation['sequenceName'] == 'S' and int(mutation['count']) >= min_sequences:
            filtered_mutations.append("S:" + str(mutation['position']) + mutation['mutationTo'])
            if "S:" + str(mutation['position']) not in filtered_mutations:
                filtered_mutations.append("S:" + str(mutation['position']))
            if "S:" + str(mutation['position']) + "X" not in filtered_mutations:
                filtered_mutations.append("S:" + str(mutation['position']) + "X")
    mutations = {}
    start_time = time.time()
    base_url = 'https://lapis.cov-spectrum.org/open/v2/sample/aggregated?'
    i = 0
    for mutation in filtered_mutations:
        start_time_mutation = time.time()
        if i % 100 == 0:
            print(f"{i} out of {len(filtered_mutations)}")
        i += 1
        mutation_url = mutation.replace(':', '%3A')
        url = f"{base_url}aminoAcidMutations={mutation_url}&fields=date&orderBy=date"
        response = requests.get(url).json()
        mutations['dataVersion'] = response['info']['dataVersion']
        mutations[mutation] = response['data']
        end_time_mutation = time.time()
        print('for mutation: ', end_time_mutation - start_time_mutation)
    print(mutations)
    end_time = time.time()
    print('total time: ', end_time - start_time)
    return mutations


def get_all_insertions(min_sequences=1000):
    all_insertions_url = "https://lapis.cov-spectrum.org/open/v2/sample/aminoAcidInsertions?minProportion=0"
    data = requests.get(all_insertions_url).json()['data']
    filtered_insertions = []
    for insertion in data:
        if insertion['sequenceName'] == 'S' and int(insertion['count']) >= min_sequences:
            filtered_insertions.append(f"ins_S:{str(insertion['position'])}:{insertion['insertedSymbols']}")
            if "ins_S:" + str(insertion['position']) + "X" not in filtered_insertions:
                filtered_insertions.append(f"ins_S:{str(insertion['position'])}:X")
    insertions = {}
    start_time = time.time()
    base_url = 'https://lapis.cov-spectrum.org/open/v2/sample/aggregated?'
    for insertion in filtered_insertions:
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
    data_version = data.pop('dataVersion')
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
                ci_lower, ci_upper = confidence_interval(count, date_count) # ????
            csv_data.append({'date': date,
                             'total_count': total_count,
                             'proportion': proportion,
                             'ci_lower': ci_lower,
                             'ci_upper': ci_upper})
        csv_file = open('../data/' + get_file_name(mutation), 'w', newline='')
        field_names = ['date', 'total_count', 'proportion', 'ci_lower', 'ci_upper']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(csv_data)
        csv_file.close()


def collect_data():
    print("Collecting mutation data...")
    mutations = get_all_mutations()
    json_to_csv(mutations)
    print("Finished collecting mutations.")
    print("Collecting insertion data...")
    insertions = get_all_insertions()
    json_to_csv(insertions)
    print("Finished collecting insertions.")


collect_data()