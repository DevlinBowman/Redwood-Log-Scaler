import json

from Utils.auto_determine_logs_format import (
    auto_determine_logs_format as get_log_format,
)
from Utils.calculate_log_scale import (
    calculate_board_footage,
    update_day_dict_with_footage,
)
from Utils.capture_taper_options import apply_taper_options, create_taper_options
from Utils.create_metadata import calculate_metadata_from_file as create_metadata
from Utils.initialize_log_dict import initialize_log_dict as initialize_dict
from Utils.input_file_formatter import input_file_formatter as format_input
# from Utils.output_pdf import json_to_pdf

# STEP 0: Constants > Files
user_supplied_input = "Live/user_supplied_input.txt"
formatted_user_supplied_input = "Live/formatted_user_supplied_input.txt"
storage_dict = "Live/parsed_data.json"
scale_table = "Utils/Scale_table_data.json"
print(
    f"0- Files loaded: \n\tuser_supplied_input: {user_supplied_input}\n\tformatted_user_supplied_input: {formatted_user_supplied_input}\n\tstorage_dict: {storage_dict}\n\tscale_table: {scale_table}\n")

# STEP 1:  Format the user supplied input to a standard formattes file
format_input(user_supplied_input, formatted_user_supplied_input)

# ---------------------------------
# STEP 2: Determine the log format
# Determine the log format, default is length_by_diameter
# log_format = get_log_format(formatted_user_supplied_input,print_result=True)
# log_format = 'diameter_by_length'
log_format = 'length_by_diameter'
print(f"2- Log format determined to be:{log_format}\n")
# ---------------------------------

# STEP 3: Initialize the primary dictionary which will be used to store all the data
day_dict = initialize_dict(
    formatted_user_supplied_input, log_format, save_to_json=False)

# STEP 4: Capture the taper options for calculating board footage
# Apply taper options
''' preset options are:
    'custom' >> arguments = butt_taper, middle_taper, top_taper, short_taper
    'true_taper' >> arguments = butt_taper
    'brett_method' arguments = none
'''

true_taper_options = create_taper_options(
    preset='true_taper', true_taper_butt='5-6')
brett_taper_options = create_taper_options(preset='brett_method')

# **************************
options = true_taper_options
# **************************
print(f"4- Taper options determined to be:{options}\n")


# STEP 5: Calculate the board footage using the initialized dictionary and taper options
updated_day_dict = apply_taper_options(day_dict, options)


# Load the scale table
with open(scale_table, "r") as f:
    scale_table = json.load(f)

# Update the day_dict with board footage
updated_day_dict = update_day_dict_with_footage(day_dict, scale_table)

# Create the create_metadata
metadata = create_metadata(storage_dict)

# generate the Final.pdf File
# json_to_pdf(storage_dict, 'Live/final_output.pdf', metadata)
