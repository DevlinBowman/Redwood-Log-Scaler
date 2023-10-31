import re
import json


def initialize_log_dict(Formatted_User_Supplied_File, log_format, save_to_json=True):

    with open(Formatted_User_Supplied_File, 'r') as file:
        lines = file.readlines()

    first_line_is_date = False
    first_line = lines[0].strip() if lines else ""
    if re.match(r"\d{1,2}\/\d{1,2}", first_line) or re.match(r"\/\d{1,2}\/\d{1,2}", first_line):
        first_line_is_date = True

    day_count = 0 if first_line_is_date else 1
    tree_count = 1
    day_dict = {}

    if not first_line_is_date:
        day_dict[day_count] = {"date": "",
                               "total_day_footage": None, "trees": {}}

    for line in lines:
        line = line.strip()

        if line == '/' or re.match(r"\d{1,2}\/\d{1,2}", line) or re.match(r"\/\d{1,2}\/\d{1,2}", line):
            day_count += 1
            tree_count = 1
            day_dict[day_count] = {"date": "",
                                   "total_day_footage": None, "trees": {}}

            if re.match(r"\d{1,2}\/\d{1,2}", line) or re.match(r"\/\d{1,2}\/\d{1,2}", line):
                day_dict[day_count]['date'] = line
        else:
            logs_temp = line.split()
            logs = [str(log) for log in logs_temp]

            tree_key = f"tree_{tree_count}"
            day_dict[day_count]['trees'][tree_key] = {"original_logs": logs,
                                                      "total_footage": None,
                                                      "logs_info": {}}

            log_entries = []
            for i, log in enumerate(logs, start=1):
                diameter, length = None, None

                if log_format == "length_by_diameter":
                    for len_value in range(8, 43, 2):
                        if str(len_value) == log[:len(str(len_value))]:
                            diameter = log[len(str(len_value)):]
                            if 6 <= int(diameter) <= 200:
                                length = str(len_value)
                                break

                    if length is None:
                        continue

                elif log_format == "diameter_by_length":
                    for len_value in range(8, 43, 2):
                        if str(len_value) == log[-len(str(len_value)):]:
                            diameter = log[:-len(str(len_value))]
                            if 6 <= int(diameter) <= 200:
                                length = str(len_value)
                                break

                    if length is None:
                        continue

                log_entries.append({
                    'log_key': f"log_{i}",
                    'diameter': int(diameter),
                    'length': int(length),
                    'notes': []
                })

            # Sort by diameter in descending order
            log_entries.sort(key=lambda x: x['diameter'], reverse=True)

            # Populate day_dict and calculate delta
            prev_diameter = None
            log_count = len(log_entries)
            for i, entry in enumerate(log_entries):
                if i == 0:
                    entry['notes'].append('is_butt')
                elif i == log_count - 1:
                    entry['notes'].append('is_top')
                else:
                    entry['notes'].append('is_middle')

                if entry['length'] >= 22:
                    entry['notes'].append('is_long')
                elif entry['length'] <= 20:
                    entry['notes'].append('is_short')

                delta = entry['diameter'] - \
                    prev_diameter if prev_diameter is not None else None
                # absolute value of delta
                delta = abs(delta) if delta is not None else None

                day_dict[day_count]['trees'][tree_key]['logs_info'][entry['log_key']] = {
                    'diameter': entry['diameter'],
                    'length': entry['length'],
                    'delta': delta,
                    'taper': None,
                    'footage': None,
                    'notes': entry['notes']
                }

                prev_diameter = entry['diameter']

            tree_count += 1

    if save_to_json:
        with open('Live/parsed_data.json', 'w') as f:
            json.dump(day_dict, f, indent=4)

    return day_dict
