import csv
from utils.confidence_interval import confidence_interval
import numpy as np


def smooth_data_per_days(file_name, path, time_frame=7, overlap=2):
    # file_name = file name of the current mutation/insertion to smooth
    # path = path to the directory with mutation/insertion data files
    # time frame = number of days over which the data is averaged
    # overlap = number of days that are overlapping between two averaged data
    data = []
    with open(path + file_name) as csv_file:
        reader = csv.reader(csv_file)
        col_names = next(reader)
        # print(col_names)
        data = {}
        for col in col_names:
            data.update({col: []})
        for row in reader:
            for i in range(len(col_names)):
                data[col_names[i]].append(row[i])


    # smoothed data structure:
    # { start-date, end-date, total-count, avg-proportion, ci-lower-avg, ci-upper-avg }
    # smoothed data is the average of 7 days with 'overlap' number of days overlapping between, default=2
    # overlaps for default value=2:
    # 1. value: days 1-7
    # 2. value: days 6-12
    # 3. value: days 11-17

    smoothed_data = []
    for i in range(0, len(data['date']) - time_frame, time_frame - overlap):
        start_date = data['date'][i]
        end_date = data['date'][i + time_frame - 1]

        count_sum = sum([int(x) * float(y) for x, y in zip(data['total_count'][i:i + time_frame], data['proportion'][i:i + time_frame])])
        time_frame_count = sum([int(x) for x in data['total_count'][i:i + time_frame]])

        avg_proportion = int(count_sum) / time_frame_count
        ci_lower_avg, ci_upper_avg = confidence_interval(count_sum, time_frame_count)
        smoothed_data.append({'start-date': start_date,
                              'end-date': end_date,
                              'total-count': time_frame_count,
                              'avg-proportion': avg_proportion,
                              'ci-lower-avg': ci_lower_avg,
                              'ci-upper-avg': ci_upper_avg
                              })

    return smoothed_data


def smooth_data_per_num_of_sequences(file_name, path):
    # file_name = file name of the current mutation/insertion to smooth
    # path = path to the directory with mutation/insertion data files

    with open(path + file_name) as csv_file:
        reader = csv.reader(csv_file)
        col_names = next(reader)
        # print(col_names)
        data = {}
        for col in col_names:
            data.update({col: []})
        for row in reader:
            for i in range(len(col_names)):
                if col_names[i] == 'date':
                    data[col_names[i]].append(row[i])
                else:
                    data[col_names[i]].append(float(row[i]))

    max_sequenced = max(data['total_count'])

    i = 0
    mutated = 0
    curr_total = 0
    lower_bound = 1 * max_sequenced
    smoothed_data = []
    start_date = data['date'][i]
    while i < len(data['date']):
        curr_total += data['total_count'][i]
        mutated += int(float(data['proportion'][i]) * data['total_count'][i])
        if curr_total >= lower_bound:
            end_date = data['date'][i]
            avg_proportion = mutated / curr_total
            ci_lower_avg, ci_upper_avg = confidence_interval(mutated, curr_total)
            smoothed_data.append({'start-date': start_date,
                                  'end-date': end_date,
                                  'total-count': curr_total,
                                  'avg-proportion': avg_proportion,
                                  'ci-lower-avg': ci_lower_avg,
                                  'ci-upper-avg': ci_upper_avg
                                  })
            if i < len(data['date']):
                start_date = data['date'][i + 1]
            curr_total = 0
            mutated = 0
        i += 1

    if start_date > end_date:
        end_date = data['date'][-1]
        avg_proportion = mutated / curr_total
        ci_lower_avg, ci_upper_avg = confidence_interval(mutated, curr_total)
        smoothed_data.append({'start-date': start_date,
                              'end-date': end_date,
                              'total-count': curr_total,
                              'avg-proportion': avg_proportion,
                              'ci-lower-avg': ci_lower_avg,
                              'ci-upper-avg': ci_upper_avg
                              })

    return smoothed_data
