import json
import math

# Update the calculate_board_footage function to handle logs that exceed max size


def calculate_board_footage(log_info, scale_table):
    """
    Calculate the board footage for a log using the scale table.

    Parameters:
    - log_info: Dictionary containing information about the log.
    - scale_table: Dictionary containing the scale table data.

    Returns:
    - footage: The board footage for the log.
    """

    length = str(log_info['length'])
    diameter = str(log_info['diameter'])
    taper = log_info['taper']

    try:
        # Try to get the footage from the scale table
        footage = scale_table[length][diameter][taper]
    except KeyError:
        # If combination is not found in the scale table, apply custom calculation
        exceeds_len = int(length) > 40
        exceeds_diam = int(diameter) > 50

        if exceeds_len:
            log_info['notes'].append('exceeds_max_len')
        if exceeds_diam:
            log_info['notes'].append('exceeds_max_diam')

        # Apply custom calculation: diameter^2 * length * 0.05, rounded down to nearest 10s place
        custom_footage = int(diameter) ** 2 * int(length) * 0.05
        footage = math.floor(custom_footage / 10) * 10

    return footage

# Function to update the day_dict with the calculated board footage


def update_day_dict_with_footage(day_dict, scale_table, overwrite_json=True):
    """
    Update the day_dict with the calculated board footage for each log, tree, and day.

    Parameters:
    - day_dict: Dictionary containing the logging information.
    - scale_table: Dictionary containing the scale table data.
    - overwrite_json: Flag to indicate whether to overwrite the existing JSON file.

    Returns:
    - day_dict: Updated dictionary with the board footage calculated and added.
    """

    for day, day_info in day_dict.items():
        total_day_footage = 0
        for tree, tree_info in day_info['trees'].items():
            total_tree_footage = 0
            for log, log_info in tree_info['logs_info'].items():
                footage = calculate_board_footage(log_info, scale_table)
                log_info['footage'] = footage
                total_tree_footage += footage

            tree_info['total_footage'] = total_tree_footage
            total_day_footage += total_tree_footage

        day_info['total_day_footage'] = total_day_footage

    if overwrite_json:
        with open('Live/parsed_data.json', 'w') as f:
            json.dump(day_dict, f, indent=4)

    return day_dict
