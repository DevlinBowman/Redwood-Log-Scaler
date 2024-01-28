import json
import math


def calculate_board_footage(log_info, scale_table):
    length = str(log_info['length'])
    diameter = str(log_info['diameter'])
    taper = log_info['taper']
    log_identifier = None

    try:
        # Try to use the scale table first
        footage = scale_table[length][diameter][taper]
    except KeyError:
        # Custom calculation for logs outside the scale table parameters
        custom_footage = int(diameter) ** 2 * int(length) * 0.05
        footage = math.floor(custom_footage / 10) * \
            10  # Round down to nearest 10

        # Append relevant notes if dimensions exceed certain thresholds
        if int(length) > 40:
            log_info['notes'].append('exceeds_max_len')
        if int(diameter) > 50:
            log_info['notes'].append('exceeds_max_diam')

        # Use the custom footage directly
        # Safely get log_key to avoid KeyError
        log_identifier = log_info.get('log_key')

    # Handle cases where footage is calculated as 0
    if footage == 0:
        # Safely get log_key to avoid KeyError
        log_identifier = log_info.get('log_key')

    return footage, log_identifier


def update_day_dict_with_footage(day_dict, scale_table, overwrite_json=True):
    total_logs_with_issues = []
    problematic_logs = []

    for day_key, day_info in day_dict.items():
        total_day_footage = 0
        for tree_key, tree_info in day_info['trees'].items():
            total_tree_footage = 0
            for log_key, log_info in tree_info['logs_info'].items():
                footage, log_identifier = calculate_board_footage(
                    log_info, scale_table)

                if footage == 0:
                    problematic_log_identifier = f"Day {day_key}, Tree {tree_key}, Log {log_key}"
                    problematic_logs.append(problematic_log_identifier)

                log_info['footage'] = footage
                total_tree_footage += footage

                if log_identifier:
                    total_logs_with_issues.append(log_identifier)

            tree_info['total_footage'] = total_tree_footage
            if total_tree_footage == 0:
                problematic_tree_identifier = f"Day {day_key}, Tree {tree_key}"
                problematic_logs.append(problematic_tree_identifier)

            total_day_footage += total_tree_footage

        day_info['total_day_footage'] = total_day_footage

    if overwrite_json:
        with open('Live/parsed_data.json', 'w') as f:
            json.dump(day_dict, f, indent=4)

    return day_dict, problematic_logs
