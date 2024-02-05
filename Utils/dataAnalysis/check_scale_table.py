import json
import matplotlib.pyplot as plt


def check_large_jumps(file_path, threshold=120):
    with open(file_path, 'r') as file:
        data = json.load(file)
        file.seek(0)  # Reset file pointer to the beginning
        lines = file.readlines()  # Read the file line by line

    differences = []  # List to store differences and their context

    # Function to approximate line number (very rough approximation)
    def approximate_line_number(search_term, start_line=0):
        for i, line in enumerate(lines[start_line:], start=start_line):
            if search_term in line:
                return i + 1  # Line numbers are 1-based
        return -1  # If not found

    # Iterate through the outer dictionary (length)
    for length, diameter_data in data.items():
        # Iterate through each diameter in the length
        for diameter, taper_data in diameter_data.items():
            previous_value = None  # Initialize the previous value
            previous_key = None  # Initialize the previous key
            previous_line_number = 0  # Initialize previous line number

            # Sort the (number-number) taper keys to ensure sequential comparison
            sorted_keys = sorted(taper_data.keys(), key=lambda x: [
                                 int(y) for y in x.split('-')])

            # Iterate through the sorted (number-number) taper keys
            for taper_key in sorted_keys:
                scale = taper_data[taper_key]
                current_line_number = approximate_line_number(
                    f'"{taper_key}": {scale}', previous_line_number)

                # If there's a previous value, compare it with the current value
                if previous_value is not None:
                    difference = abs(scale - previous_value)
                    if difference >= threshold:
                        differences.append({
                            "difference": difference,
                            "detail": f"Diff: {difference} in Values:\n     -- LEN {length} X DIA {diameter}:\n     > Taper '{previous_key}' : {previous_value} (Line: {previous_line_number})\n     > Taper '{taper_key}' : {scale} (Line: {current_line_number})"
                        })

                previous_value = scale  # Update the previous value
                previous_key = taper_key  # Update the previous key
                previous_line_number = current_line_number  # Update the previous line number

    # Sort the differences by magnitude
    sorted_differences = sorted(
        differences, key=lambda x: x["difference"], reverse=True)

    # Print sorted differences
    for diff in sorted_differences:
        print(diff["detail"])


# Example usage
# file_path = 'Utils/Scale_table_data.json'
# check_large_jumps(file_path)
