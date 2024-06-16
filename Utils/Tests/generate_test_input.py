# create a file in the live directory with the name user_supplied_input.txt:

def generate_test_input():
    filepath = "Live/user_supplied_input.txt"
    test_input = """
    1/16/3612 1410 3615/3622 3618 3810/208/3626 3420 1417/2018 3614 368/3624 3620 4011
    /1/17/1219 3614 368/3616 3613 268/3621 4016 408/3619 2416/2034 4026 2419///3612 3618
    """
    with open(filepath, "w") as f:
        f.write(test_input)

def generate_test_webpage_fields():
    webpage_fields = {
    "user_supplied_input": "Live/user_supplied_input.txt",
    "log_format": "length_by_diameter",
    "options": create_taper_options(preset='true_taper', true_taper_butt='5-6')
}
    return webpage_fields

def run_pseudo_inputs():
    generate_test_input()
    return generate_test_webpage_fields()
