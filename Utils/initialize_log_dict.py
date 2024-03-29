
import re
import json


def initialize_log_dict(Formatted_User_Supplied_File, log_format, save_to_json=True):
    with open(Formatted_User_Supplied_File, 'r') as file:
        lines = file.readlines()

    first_line_is_date = False
    first_line = lines[0].strip() if lines else ""
    if re.match(r"\d{1,2}/\d{1,2}", first_line) or re.match(r"/\d{1,2}/\d{1,2}", first_line):
        first_line_is_date = True

    day_count = 0 if first_line_is_date else 1
    tree_count = 1
    day_dict = {}

    if not first_line_is_date:
        day_dict[day_count] = {"date": "",
                               "total_day_footage": None, "trees": {}}

    odd_lengths = set([9, 11, 13, 15, 17, 19, 21, 23, 25,
                      27, 29, 31, 33, 35, 37, 39, 41, 43])

    for line in lines:
        line = line.strip()

        if line == '/' or re.match(r"\d{1,2}/\d{1,2}", line) or re.match(r"/\d{1,2}/\d{1,2}", line):
            day_count += 1
            tree_count = 1
            day_dict[day_count] = {"date": "",
                                   "total_day_footage": None, "trees": {}}

            if re.match(r"\d{1,2}/\d{1,2}", line) or re.match(r"/\d{1,2}/\d{1,2}", line):
                day_dict[day_count]['date'] = line
        else:
            logs_temp = line.split()
            logs = [str(log) for log in logs_temp]

            tree_key = f"tree_{tree_count}"
            day_dict[day_count]['trees'][tree_key] = {
                "original_logs": logs, "total_footage": None, "logs_info": {}}

            log_entries = []
            for i, log in enumerate(logs, start=1):
                diameter, length = None, None
                misinput_detected = False

                if log_format == "length_by_diameter":
                    first_two_digits = int(
                        log[:2]) if log[:2].isdigit() else None
                    if first_two_digits in odd_lengths:
                        misinput_detected = True
                        # print(f"ODD LEN:{log} | DAY: {day_count}, TREE: {tree_count}, LOG: {i}")
                    else:
                        for len_value in range(8, 43, 2):
                            if str(len_value) == log[:len(str(len_value))]:
                                diameter = int(log[len(str(len_value)):]) if log[len(
                                    str(len_value)):].isdigit() else None
                                if diameter and 6 <= diameter <= 200:
                                    length = len_value
                                    break

                elif log_format == "diameter_by_length":
                    # Correctly identify the length and diameter
                    misinput_detected = False
                    length_identified = False

                    # Iterate through possible lengths in reverse order to match the longest possible first
                    for len_value in sorted(range(8, 43, 2), reverse=True):
                        if log.endswith(str(len_value)):
                            # Extract diameter and length
                            diameter_part = log[:-len(str(len_value))]
                            length_part = log[-len(str(len_value)):]
                            
                            if diameter_part.isdigit() and length_part.isdigit():
                                diameter = int(diameter_part)
                                length = int(length_part)
                                
                                # Validate the diameter and length
                                if 6 <= diameter <= 200 and length in range(8, 43, 2):
                                    length_identified = True
                                    break  # Valid length and diameter found

                    # If length was not identified correctly or it falls into odd_lengths, mark as misinput
                    if not length_identified or length in odd_lengths:
                        misinput_detected = True



                log_entry = {
                    'log_key': f"log_{i}",
                    'original_log': log,
                    'diameter': diameter,
                    'length': length,
                    'notes': ['misinput'] if misinput_detected else []
                }

                log_entries.append(log_entry)

                # Sorting log entries by diameter in descending order, handling None values gracefully
            log_entries.sort(key=lambda x: (
                x['diameter'] is not None, x['diameter']), reverse=True)

            prev_diameter = None
            for i, entry in enumerate(log_entries):
                # Adding position notes (butt, top, middle)
                if i == 0:
                    entry['notes'].append('is_butt')
                elif i == len(log_entries) - 1:
                    entry['notes'].append('is_top')
                else:
                    entry['notes'].append('is_middle')

                # Checking for long or short logs
                if entry['length'] is not None:
                    if entry['length'] >= 22:
                        entry['notes'].append('is_long')
                    elif entry['length'] <= 20:
                        entry['notes'].append('is_short')

                # Calculating delta and handling None values
                if prev_diameter is not None and entry['diameter'] is not None:
                    delta = abs(entry['diameter'] - prev_diameter)
                else:
                    delta = None

                day_dict[day_count]['trees'][tree_key]['logs_info'][entry['log_key']] = {
                    'original_log': entry['original_log'],
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
