# Redwood Log Scale Calculator User Guide

** To be served at Trashtools.org/Redwood-Log-Scale-Calculator ** 

## Intro 
This project takes in a pre-formatted input and calculates fellers log scale based off if a pre-defined metric.
The user will input their scale list (in the proper format) collected during felling and the app will calculate the scale of the logs and trees within it by day.

## CRUD Flow

**Collect data from Live/user_supplied_input.txt**
>**Input File format requirements**
    - Day/Tree/Log/
    - "Dates" can be specified with "MM/DD/" and will be parsed into a day object
    - "Days" without a date can be represented by "///" and will be parsed into a day object
    - Trees are seperated by "/" delimeters within a "Day" and the groups of numbers within them are "Logs"
    - "Logs are seperated by " " (a single whitespace) and consist of 3 to 6 digits (usually 4) denoting a length and a diameter
    - Example input (log format length X Diameter); 12/14/3618 3614 3210/1630 3624 4019/... 

> Parse Live/user_supplied_input.txt into Live/formatted_user_supplied_input.txt
    - The creation of this file is for preliminary debugging purposes at this time.
    - It may later be removed from the project and its contents accessed and stored via runtime specific object


> Collect input file format for log representation (Length X Diameter | Diameter X Length)

> Initialize the "day_dict"
    - the "day_dict" is the primary data structure which contains all basic information about the inputted file
        - day_#
            -"date"
            -"total_day_footage"
            -"trees_#"
                - "original_logs"
                - "total_footage"
                - "logs_info"
                    - "log_#"
                        - "original_log"
                        - "diameter"
                        - "length"
                        - "delta"
                        - "taper"
                        - "footage"
                        - "notes"
 
                    
> Capture "taper_options"
    - The "taper_options" determine which values are pulled from the Scale data sheets for determining the scale of each Log

> Create the Live/parsed_data.json file with the values from the formatted "day_dict"

> Create, calculate, and display metadata about the Live/parsed_data.json


