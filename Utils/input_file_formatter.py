import re


def input_file_formatter(infile, outfile):

    with open(infile, 'r') as file:
        raw_data = file.read()

    raw_data = re.sub(r'[,|-]', '/', raw_data)

    # Replace multiple spaces with a single space
    raw_data = re.sub(r'\s{2,}', ' ', raw_data)

    # Remove spaces next to slashes
    raw_data = re.sub(r'/\s+|/\s+', '/', raw_data)

    # Limit consecutive slashes to three
    raw_data = re.sub(r'/{4,}', '///', raw_data)

    # Clean the input and check for invalid characters
    cleaned_data = re.sub('[^0-9/ ]', '', raw_data)

    # Ensure that the cleaned data starts and ends with a slash
    if not cleaned_data.startswith('/'):
        cleaned_data = '/' + cleaned_data
    if not cleaned_data.endswith('/'):
        cleaned_data += '/'

    # re captures all types of patterns (logs, trees, dates, and separators)
    pattern_re = re.compile(r'(?:\/(\d{1,2}\/\d{1,2})\/)|(\/\/\/)|([^/]+)')

    # Initialize the list that will hold the final output lines
    output_lines = []

    # Find all object matches and process them one by one
    for match in pattern_re.finditer(cleaned_data):
        if match.group(1):  # This is a date
            output_lines.append(match.group(1))
        elif match.group(2):  # This is a day separator
            output_lines.append('/')
        elif match.group(3):  # This is a tree or a log
            output_lines.append(match.group(3).strip())

    # Step 3: Write the patterns to the output file
    with open(outfile, 'w') as file:
        for line in output_lines:
            file.write(f"{line}\n")

    print(f"1- Formatted input file written to:\n {outfile}\n")
