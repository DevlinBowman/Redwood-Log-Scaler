import json


#
def print_json_data_to_file(input_file_path, output_file_path, metadata):
    # Load data from the JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    header_groups = {
        "overview": ["log_format", "total_board_footage"],
        "average": ["average_footage_per_day", "average_tree_footage",
                    "average_logs_per_tree"],
        "totals": ["total_days", "total_trees", "total_logs"],
        "counts": ["logs_exceeding_table", "max_log_diameter",
                   "greatest_tree_footage", "total_count_of_each_log_length", "taper_usage_rates"]
    }

    with open(output_file_path, 'w') as output_file:
        output_file.write("Metadata Summary:\n")
        max_key_length = max((len(key) for key in metadata.keys()), default=0)

        for group, items in header_groups.items():
            output_file.write(f"\n{group.title()}:\n")
            for item in items:
                value = metadata.get(item)
                if isinstance(value, dict):

                    output_file.write("\n")
                    output_file.write(f"{item}:\n")

                    if item in ["total_count_of_each_log_length", "taper_usage_rates"]:
                        items = [f"{k}: {v}" for k, v in value.items()]
                        output_file.write("  " + " | ".join(items) + "\n")

                    else:
                        sub_max_key_length = max(
                            (len(k) for k in value.keys()), default=0)
                        for sub_key, sub_value in value.items():
                            formatted_sub_key = f"{sub_key}:".ljust(
                                sub_max_key_length + 2)
                            output_file.write(
                                f"  {formatted_sub_key} {sub_value}\n")
                else:
                    formatted_key = f"{item}:".ljust(max_key_length + 2)
                    output_file.write(f"{formatted_key} {value}\n")

        # Four empty lines before detailed log data
        output_file.write("\n" * 4)
        output_file.write("\f")

        for day, day_info in data.items():
            output_file.write(
                f"Day {day} | Date: {day_info['date']} | BoardFeet: {day_info['total_day_footage']}\n")
            output_file.write("_" * 60 + "\n")
            output_file.write("-" * 60 + "\n")
            for tree, tree_info in day_info['trees'].items():
                total_tree_footage = tree_info['total_footage']
                total_footage_str = f" | Board Feet: >> {total_tree_footage} <<"
                tree_header = f"{tree.upper()}: [{', '.join([str(log) for log in tree_info['original_logs']])}]{total_footage_str}"
                output_file.write(f"\n{tree_header}\n")
                # Thinner line for tree header
                output_file.write(" " + "-" * (len(tree_header) // 2) + "\n")
                for log, log_info in tree_info['logs_info'].items():
                    output_file.write(
                        f"{log}: Diameter: {log_info['diameter']:>3}\" | Length: {log_info['length']:>2}' | Taper: {log_info['taper']:<4} ->   {log_info['footage']} BF\n")
                # Regular line for logs
                output_file.write(" " + "-" * 60 + "\n")
            output_file.write("\n" * 2)  # Two empty lines between each day
            output_file.write("=" * 60 + "\n")  # Thick line between days
            output_file.write("\f")


# File paths
input_file_path = 'Live/parsed_data.json'
output_file_path = 'Live/output.txt'
