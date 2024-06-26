import re
import json
from collections import Counter, OrderedDict


def calculate_metadata_from_file(output_file, log_format, print_result=True):
    with open(output_file, 'r') as file:
        data = json.load(file)

    misinputs = []

    # Check for null values in log lengths
    for day_key, day in data.items():
        # Get the date if available, otherwise use "NoDate"
        # date = day.get("date", "NoDate")
        for tree_key, tree in day["trees"].items():
            tree_num = ''.join(re.findall(r'\d+', tree_key))
            for log_key, log in tree["logs_info"].items():
                log_num = ''.join(re.findall(r'\d+', log_key))
                if log.get("length") is None:
                    # Formatting the misinput string to include detailed information
                    misinput_str = f"INVALID INPUT:  >> {log['original_log']} <<  -- AT:  DAY:{day_key}, TREE:{tree_num},  LOG:{log_num}"
                    misinputs.append(misinput_str)

    if misinputs:
        # If any null values are found, print the error and misinput data, then return
        print('\n-----------------------------------------------------------')
        print("MISINPUT ERROR - Please update the following data:\n")
        for misinput in misinputs:
            print(misinput)
        print('-----------------------------------------------------------')
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

                max_log_diameter = max(
                    max_log_diameter, log.get("diameter", 0))
                taper_usage_counter[log.get("taper", "0-0")] += 1

    total_days = len(data)
    total_trees = sum(len(day["trees"]) for day in data.values())
    sorted_log_lengths_counter = OrderedDict(sorted(
        log_lengths_counter.items(), key=lambda x: int(x[0]) if x[0] is not None else 0))

    header = {
        "log_format": log_format,
        "total_board_footage": total_tree_footage,
        "average_footage_per_day": round(total_tree_footage / total_days, 2) if total_days > 0 else 0,
        "total_days": total_days,
        "average_tree_footage": round(total_tree_footage / total_trees, 2) if total_trees > 0 else 0,
        "total_trees": total_trees,
        "total_logs": total_logs,
        "average_logs_per_tree": round(total_logs / total_trees, 2) if total_trees > 0 else 0,
        "logs_exceeding_table": logs_exceeding_table,
        "max_log_diameter": max_log_diameter,
        "greatest_tree_footage": max((tree.get("total_footage", 0) for day in data.values() for tree in day["trees"].values()), default=0),
        "total_count_of_each_log_length": dict(sorted_log_lengths_counter),
        "taper_usage_rates": dict(taper_usage_counter),
    }
    header_groups = {
        "overview": ["log_format", "total_board_footage"],
        "average": ["average_footage_per_day", "average_tree_footage",
                    "average_logs_per_tree"],
        "totals": ["total_days", "total_trees", "total_logs"],
        "counts": ["logs_exceeding_table", "max_log_diameter",
                   "greatest_tree_footage", "total_count_of_each_log_length", "taper_usage_rates"]
    }

    # def print_header():
    #
    #     if print_result:
    #         # for item in header:
    #         #     print(f"{item}: {header[item]}")
    #         #     # print a formatted version of the header items
    #         print("Summary Report")
    #         for item, value in header.items():
    #             print(f"{item.replace('_', ' ').title():<30}: {value}")

    def print_header_groups():

        if print_result:
            for group in header_groups:
                print()
                for item in header_groups[group]:
                    print(
                        f"{item.replace('_', ' ').title():<30}: {header[item]}")
    print_header_groups()

    return header

# Note: This function reads from a file and calculates metadata, handling null log lengths early on.
