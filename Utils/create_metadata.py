from collections import defaultdict, Counter, OrderedDict
import json


def calculate_metadata_from_file(output_file, print_result=True):
    with open(output_file, 'r') as file:
        data = json.load(file)

    total_tree_footage = 0
    total_logs = 0
    log_lengths_counter = Counter()
    logs_exceeding_table = 0
    max_log_diameter = 0
    taper_usage_counter = Counter()

    # Counting total number of trees and logs, and summing up the footage
    for day in data.values():
        for tree in day["trees"].values():
            total_tree_footage += tree["total_footage"]
            total_logs += len(tree["logs_info"])
            for log in tree["logs_info"].values():
                log_lengths_counter[log["length"]] += 1

                # Count the number of logs exceeding table length or diameter
                if 'exceeds_max_len' in log['notes'] or 'exceeds_max_diam' in log['notes']:
                    logs_exceeding_table += 1

                # Update the maximum log diameter
                max_log_diameter = max(max_log_diameter, log["diameter"])

                # Count the usage of each taper
                taper_usage_counter[log["taper"]] += 1

    total_days = len(data)
    total_trees = sum(len(day["trees"]) for day in data.values())

    # Sort log_lengths_counter by log length (shortest to longest)
    sorted_log_lengths_counter = OrderedDict(
        sorted(log_lengths_counter.items(), key=lambda x: int(x[0])))

    header = {
        "total_days": total_days,
        "total_trees": total_trees,
        "total_logs": total_logs,
        "total_board_footage": sum(tree["total_footage"] for day in data.values() for tree in day["trees"].values()),
        "average_footage_per_day": round(sum(tree["total_footage"] for day in data.values() for tree in day["trees"].values()) / total_days, 2) if total_days > 0 else 0,
        "average_tree_footage": round(total_tree_footage / total_trees, 2) if total_trees > 0 else 0,
        "average_logs_per_tree": round(total_logs / total_trees, 2) if total_trees > 0 else 0,
        "total_count_of_each_log_length": dict(sorted_log_lengths_counter),
        "logs_exceeding_table": logs_exceeding_table,
        "max_log_diameter": max_log_diameter,
        "greatest_tree_footage": max(tree["total_footage"] for day in data.values() for tree in day["trees"].values()),
        "taper_usage_rates": dict(taper_usage_counter)
    }

    if print_result:
        for item in header:
            print(f"{item}: {header[item]}")
    return header

# The function should work as intended, but since it reads a file, I can't execute it here.
# You can run this updated version of the function in your local environment.
