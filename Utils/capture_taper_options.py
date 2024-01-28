import json

TAPER_TYPES = {
    '0-0': '0-0',
    '1-2': '1-2',
    '3-4': '3-4',
    '5-6': '5-6',
    '7-8': '7-8',
    '9-10': '9-10'
}


# Function to map delta to taper ('true scale')
def map_delta_to_taper(log_info):
    delta = log_info['delta']
    if delta is None:
        return log_info  # No delta available

    if delta >= 9:
        log_info['taper'] = TAPER_TYPES['9-10']
        if delta > 10:
            log_info['notes'].append('exceeds_max_delta')
    elif 7 <= delta <= 8:
        log_info['taper'] = TAPER_TYPES['7-8']
    elif 5 <= delta <= 6:
        log_info['taper'] = TAPER_TYPES['5-6']
    elif 3 <= delta <= 4:
        log_info['taper'] = TAPER_TYPES['3-4']
    elif 1 <= delta <= 2:
        log_info['taper'] = TAPER_TYPES['1-2']
    else:
        log_info['taper'] = TAPER_TYPES['0-0']
    return log_info


# Function to create taper options
def create_taper_options(preset=None, butt_taper=None, middle_taper=None, top_taper=None, short_taper='0-0', true_taper_butt=None):
    options = {}
    if preset == 'custom':
        options['preset'] = 'custom'
        options['butt_taper'] = butt_taper
        options['middle_taper'] = middle_taper
        options['top_taper'] = top_taper
        options['short_taper'] = short_taper
    elif preset == 'true_taper':
        options['preset'] = 'true_taper'
        options['true_taper_butt'] = true_taper_butt
    elif preset == 'brett_method':
        options['preset'] = 'brett_method'
        options['butt_taper'] = '5-6'
        options['middle_taper'] = '3-4'
        options['top_taper'] = '1-2'
        options['short_taper'] = '0-0'
    return options


# Function to apply taper options
def apply_taper_options(day_dict, options, overwrite_json=True):
    for day, day_info in day_dict.items():
        for tree, tree_info in day_info['trees'].items():
            for log, log_info in tree_info['logs_info'].items():
                # Handle short logs first
                if 'is_short' in log_info['notes']:
                    log_info['taper'] = '0-0'
                elif options.get('preset') == 'true_taper':
                    if 'is_butt' in log_info['notes']:
                        log_info['taper'] = options.get(
                            'true_taper_butt', '0-0')
                    else:
                        log_info = map_delta_to_taper(log_info)
                elif options.get('preset') == 'brett_method':
                    if 'is_butt' in log_info['notes']:
                        log_info['taper'] = '5-6'
                    elif 'is_middle' in log_info['notes']:
                        log_info['taper'] = '3-4'
                    elif 'is_top' in log_info['notes']:
                        log_info['taper'] = '1-2'
                else:
                    if 'is_butt' in log_info['notes']:
                        log_info['taper'] = options.get('butt_taper', '0-0')
                    elif 'is_middle' in log_info['notes']:
                        log_info['taper'] = options.get('middle_taper', '0-0')
                    elif 'is_top' in log_info['notes']:
                        log_info['taper'] = options.get('top_taper', '0-0')
    if overwrite_json:
        print(
            f'5- Overwriting parsed_data.json with updated taper options:\n {options}\n')
        with open('Live/parsed_data.json', 'w') as f:
            json.dump(day_dict, f, indent=4)
    return day_dict
