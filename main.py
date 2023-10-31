import json

from Utils.input_file_formatter import input_file_formatter as format_input
from Utils.auto_determine_logs_format import auto_determine_logs_format as get_log_format
from Utils.initialize_log_dict import initialize_log_dict as initialize_dict
from Utils.capture_taper_options import create_taper_options, apply_taper_options
from Utils.calculate_log_scale import calculate_board_footage, update_day_dict_with_footage
from Utils.create_metadata import calculate_metadata_from_file as create_metadata

# Files
user_supplied_input = "Live/user_supplied_input.txt"
formatted_user_supplied_input = "Live/formatted_user_supplied_input.txt"
storage_dict = "Live/parsed_data.json"
scale_table = "Utils/Scale_table_data.json"


# Format the user supplied input
format_input(user_supplied_input, formatted_user_supplied_input)

# Determine the log format, default is length_by_diameter
log_format = get_log_format(formatted_user_supplied_input,print_result=True)

# Initialize the primary dictionary
day_dict = initialize_dict(formatted_user_supplied_input, log_format, save_to_json=False)

# Apply taper options
''' preset options are:
    'custom' >> arguments = butt_taper, middle_taper, top_taper, short_taper
    'true_taper' >> arguments = butt_taper
    'brett_method' arguments = none
'''

true_taper_options = create_taper_options(preset='true_taper', true_taper_butt='5-6')

# Apply "true taper" options
updated_day_dict = apply_taper_options(day_dict, true_taper_options)

# brettpreset = create_taper_options(preset='brett_method')
# updated_day_dict = apply_taper_options(day_dict, brettpreset)

# Load the scale table
with open(scale_table, "r") as f:
    scale_table = json.load(f)

# Update the day_dict with board footage
updated_day_dict = update_day_dict_with_footage(day_dict, scale_table)

# Create the create_metadata
metadata = create_metadata(storage_dict)
