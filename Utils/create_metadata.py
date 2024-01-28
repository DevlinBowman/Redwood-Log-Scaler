
import json
from collections import Counter, OrderedDict

def calculate_metadata_from_file(output_file, print_result=True):
    with open(output_file, 'r') as file:
        data = json.load(file)

    misinputs = []

    # Check for null values in log lengths
    for day_key, day in data.items():
        date = day.get("date", "NoDate")  # Get the date if available, otherwise use "NoDate"
        for tree_key, tree in day["trees"].items():
            for log_key, log in tree["logs_info"].items():
                if log.get("length") is None:
                    # Formatting the misinput string to include detailed information
                    misinput_str = f">>> {date} | Day {day_key} | Tree {tree_key} | Log {log_key} | "
                    misinputs.append(misinput_str)


    if misinputs:
        # If any null values are found, print the error and misinput data, then return
        print("MISINPUT ERROR - Please update the following data:")
        for misinput in misinputs:
            print(misinput)
        return None  # Exit the function early

    # Metadata calculation continues if no misinput errors are found
    total_tree_footage = 0
    total_logs = 0
    log_lengths_counter = Counter()
    logs_exceeding_table = 0
    max_log_diameter = 0
    taper_usage_counter = Counter()

    for day in data.values():
        for tree in day["trees"].values():
            total_tree_footage += tree.get("total_footage", 0)
            total_logs += len(tree["logs_info"])
            for log in tree["logs_info"].values():
                log_length = log.get("length")
                if log_length is not None:
                    log_lengths_counter[log_length] += 1

                if 'exceeds_max_len' in log['notes'] or 'exceeds_max_diam' in log['notes']:
                    logs_exceeding_table += 1

                max_log_diameter = max(max_log_diameter, log.get("diameter", 0))
                taper_usage_counter[log.get("taper", "0-0")] += 1

    total_days = len(data)
    total_trees = sum(len(day["trees"]) for day in data.values())
    sorted_log_lengths_counter = OrderedDict(sorted(log_lengths_counter.items(), key=lambda x: int(x[0]) if x[0] is not None else 0))

    header = {
        "total_days": total_days,
        "total_trees": total_trees,
        "total_logs": total_logs,
        "total_board_footage": total_tree_footage,
        "average_footage_per_day": round(total_tree_footage / total_days, 2) if total_days > 0 else 0,
        "average_tree_footage": round(total_tree_footage / total_trees, 2) if total_trees > 0 else 0,
        "average_logs_per_tree": round(total_logs / total_trees, 2) if total_trees > 0 else 0,
        "total_count_of_each_log_length": dict(sorted_log_lengths_counter),
        "logs_exceeding_table": logs_exceeding_table,
        "max_log_diameter": max_log_diameter,
        "greatest_tree_footage": max((tree.get("total_footage", 0) for day in data.values() for tree in day["trees"].values()), default=0),
        "taper_usage_rates": dict(taper_usage_counter)
    }

    if print_result:
        for item in header:
            print(f"{item}: {header[item]}")

    return header

# Note: This function reads from a file and calculates metadata, handling null log lengths early on.
# Make sure to run this in your local environment to verify its functionality with your specific data.
