def auto_determine_logs_format(filepath,default="length_by_diameter",print_result=False):
    # Valid lengths are even numbers between 8 and 42
    detected_format = default
    valid_lengths = set(str(x) for x in range(8, 43, 2))
    format_counts = {"length_by_diameter": 0, "diameter_by_length": 0}

    with open(filepath, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        logs = line.split()

        for log in logs:
            parts = log.split('/')

            # Skip if log doesn't have both parts
            if len(parts) != 2:
                continue

            # Check which part is the length (must be an even number between 8 and 42)
            if parts[0] in valid_lengths:
                format_counts["length_by_diameter"] += 1
            elif parts[1] in valid_lengths:
                format_counts["diameter_by_length"] += 1

    # Determine the most frequent format in the logs
    detected_format = max(format_counts, key=format_counts.get)

    if format_counts[detected_format] > 0:
        if print_result:
            print(
                f"The log format in the file is {detected_format.replace('_', ' ')}.\n")
        return detected_format
    else:
        if print_result:
            print("Could not determine the log format. Please check the input file.")
        return None
