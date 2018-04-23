'''
Utility function to write logs to json for reading by telegraf
'''

import json

def write_json_log(data, log_file):
    '''
    Write log data to csv
    :param value: <int> Value (count)
    :param log_file: <str> Location of log file
    '''

    try:
        with open(log_file, "a") as lf:
            json.dump(data, lf)
            lf.write("\n")
    except Exception as e:
        print("write_json_log: Failed to log data to log")
        print(e)
