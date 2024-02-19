# Redwood Log Scale Calculator User Guide

This guide is intended to explain the use of the Redwood Log Scale Calculator, accessible at Trashtools.org/Redwood-Log-Scale-Calculator.

## Introduction
The Redwood Log Scale Calculator is designed to process pre-formatted input to calculate the log scale based on a predefined metric. Users will input their scale list, collected during felling, in the specified format. The application will then compute the scale of logs and trees for each day.

## Web Development Startup
- currently, the only dependency is Python - Flask
- start the server by running python3 run.py

## Overview of Operations (CRUD Flow)

### Data Collection
- **Source:** Live/user_supplied_input.txt
- **Format Requirements:**
  - Structure: Day/Tree/Log
  - Dates: Specified as "MM/DD/", parsed into a day object.
  - Non-dated Days: Represented by "///", parsed into a day object.
  - Trees: Separated by "/" within a Day, containing groups of Logs.
  - Logs: Separated by a single whitespace, with 3 to 6 digits indicating length and diameter.
  - Example: "12/14/3618 3614 3210/1630 3624 4019/..."

### Environment Setup and Input Formatting
- **Initialize Directories:** The environment, including necessary directories, is set up for processing.
- **Format User Input:** The `Utils.input_file_formatter` function standardizes the user-supplied input, ensuring it adheres to the application's format requirements. This file is not necessary for the fundamental function of the project but rather exists for debugging issues with the initial user input. (It is currently a dependency based on project structure)

### Log Format Determination and Data Structure Initialization
- **Log Format:** The format for log representation (Length X Diameter or Diameter X Length) is crucial for calculations. The default is set to 'length_by_diameter' but the option to choose either should be presented to the user in the client page.
- **Initialize Data Structure:** The `day_dict` is initialized to organize the formatted input data for processing. This includes storing information about each day, tree, and log, including measurements and calculated values. It was originally named the day dict because "day" is the primary key for elements in the file, however it is more appropriate to consider it as "parsed_data" 

### Taper Options and Board Footage Calculation
- **Taper Options:** Taper options are applied to adjust the calculations according to log characteristics. Options include 'custom', 'true_taper', and 'brett_method'.
    - Taper options for "true_taper" are calculated dynamically by using the deltas between logs with only a butt taper being captured (as there is no previous log from which to derive a delta)
    - Taper options for "brett_method" are a hard preset and will not be modifiable by the user at this time.
    - Taper options for "custom" are available for all "long_log" types (butt, middle, & top) but short logs are hard mapped to "0-0" as is industry standard.
- **Calculate Board Footage:** The application calculates the board footage for each log using the selected taper options and updates the `day_dict` accordingly.
    - Scale Table: A scale table loaded from `Utils/Scale_table_data.json` provides necessary values for calculating the board footage based on log measurements.
    - The board footage table is a file located in Utils/ which contains all acceptable and common length, diameter, and taper combination with a pre calculated numeric values applied to each as board footage. The table only contains values for diameters up to 50" so any log with a diameter above this has its board footage calculated using an encoded equation further ignoring taper options for that item.

### Scale Table Utilization and Metadata Generation
- **Metadata:** Metadata about the processed logs, including total volume and log count, is generated to provide insights into the calculated scales.
    - This information is calculated after the rest of the program and is used to supply the user with useful information about the output.

### Output Generation
- The process culminates in the creation of `Live/parsed_data.json`, containing all calculated data and metadata. The structured output facilitates further analysis and reporting.
- When completed, the program should generate a .pdf, .txt, or .md file which contains a well structured and human readable document containing useful information about the scale. This file serves as the target object to be served to the user and is intended to meet the needs of the user thus completing its function.
