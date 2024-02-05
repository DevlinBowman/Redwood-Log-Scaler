# Redwood Log Scale Calculator User Guide

## Intro 
This project takes in a pre-formatted input and calculates fellers log scale based off if a pre-defined metric.

## CRUD Flow
> Collect data from Live/user_supplied_input.txt
 // Input File format requirements
  - Day/Tree/Log/
  - "Dates" can be specified with "MM/DD/" and will be parsed into a day object
  - "Days" without a date can be represented by "///" and will be parsed into a day object
  - Trees are seperated by "/" delimeters within a "Day" and the groups of numbers within them are "Logs"
  - "Logs are seperated by " " (a single whitespace) and consist of 3 to 6 digits (usually 4) denoting a length and a diameter
  - Example input (log format length X Diameter); 12/14/3618 3614 3210/1630 3624 4019/... 



formatted_user_supplied_input.txt
parsed_data.json



