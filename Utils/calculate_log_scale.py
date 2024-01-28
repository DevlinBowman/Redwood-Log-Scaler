import json
import math


def calculate_board_footage(log_info, scale_table):
    length = log_info.get('length')
    diameter = log_info.get('diameter')
    taper = log_info.get('taper', '0-0')  # Default taper value if not provided
    log_identifier = log_info.get('log_key', None)

    # Check for None values in length and diameter
    if length is None or diameter is None:
        footage = 0  # Default to 0 footage for invalid logs
        note = 'invalid_dimensions'
        if length is None:
            note += '_missing_length'
        if diameter is None:
            note += '_missing_diameter'
        log_info['notes'].append(note)
    else:
        try:
            # Convert length and diameter to strings as scale_table keys are strings
            length_str, diameter_str = str(length), str(diameter)
            # Try to use the scale table
            footage = scale_table[length_str][diameter_str][taper]
        except KeyError:
            # Custom calculation for logs outside the scale table parameters
            custom_footage = diameter ** 2 * length * 0.05
            footage = math.floor(custom_footage / 10) * \
                10  # Round down to nearest 10

            # Append relevant notes if dimensions exceed certain thresholds
            if length > 40:
                log_info['notes'].append('exceeds_max_len')
            if diameter > 50:
                log_info['notes'].append('exceeds_max_diam')

    # Handle cases where footage is calculated as 0
    if footage == 0 and 'invalid_dimensions' not in log_info['notes']:
        log_info['notes'].append('zero_footage_calculated')

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
