# Backend Integration Test

import sys
from datetime import datetime

#defining extract data function

def parse_log_data(string):
    line = string.split()

    date = line[0]
    time = line[1]
    client_ip = line[6].split("#")[0]
    host = line[7].strip("():")

    time_stamp = f"{date}T{time}Z"
    parsed_time_stamp = datetime.strptime(time_stamp, '%d-%b-%YT%H:%M:%S.%fZ')

    return {
        "timestamp": parsed_time_stamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "client_ip": client_ip,
        "host": host
    }

#Read file and extract data.

def print_logs(rute):
    with open(rute, "r") as f:
        for line in f:
            print(parse_log_data(line))

file = sys.argv[1]
print_logs(file)

