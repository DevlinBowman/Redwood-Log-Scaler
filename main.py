# Main script to run when user clicks "Calculate" on the webpage
import json

from Utils.mk_txt import print_json_data_to_file, input_file_path, output_file_path

from Utils.initialize_live_dir import initialize_live_dir
from Utils.calculate_log_scale import update_day_dict_with_footage
from Utils.capture_taper_options import apply_taper_options, create_taper_options
from Utils.create_metadata import calculate_metadata_from_file as create_metadata
from Utils.initialize_log_dict import initialize_log_dict as initialize_dict
from Utils.input_file_formatter import input_file_formatter as format_input
# from Utils.output_pdf import json_to_pdf

# Example of the fields that will be passed from the webpage
webpage_fields = {
    "user_supplied_input": "Live/user_supplied_input.txt",
    # "log_format": "length_by_diameter",
    "log_format": "diameter_by_length",
    "options": create_taper_options(preset='true_taper', true_taper_butt='5-6')
}

# displays the fields inputted by the user
print(webpage_fields["options"])


# Main script to run when user clicks "Calculate" on the webpage
def main(webpage_fields):
    initialize_live_dir()

    user_supplied_input = webpage_fields["user_supplied_input"]
    formatted_user_supplied_input = "Live/formatted_user_supplied_input.txt"
    storage_dict = "Live/parsed_data.json"
    scale_table = "Utils/Scale_table_data.json"
    log_format = webpage_fields["log_format"]
    options = webpage_fields["options"]

    # Format the user-supplied input file
    format_input(user_supplied_input, formatted_user_supplied_input)

    # Initialize the day_dict with the user-supplied input
    day_dict = initialize_dict(
        formatted_user_supplied_input, log_format, save_to_json=False)

    # Initialize the day_dict with the taper options
    updated_day_dict = apply_taper_options(day_dict, options)

    with open(scale_table, "r") as f:
        scale_table = json.load(f)

    # Update the day_dict with footage
    updated_day_dict = update_day_dict_with_footage(day_dict, scale_table)

    # calculates & prints output information
    metadata = create_metadata(storage_dict, log_format)

    return metadata


metadata = main(webpage_fields)

# creates an output.txt file of the data for user to download
print_json_data_to_file(input_file_path, output_file_path, metadata)
print("Done")
