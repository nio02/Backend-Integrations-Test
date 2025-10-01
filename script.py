# Backend Integration Test

import sys

#defining extract data function

def parse_log_data(string):
    line = string.split()

    date = line[0]
    time = line[1]
    client_ip = line[6].split("#")[0]
    host = line[7].strip("():")

    return {
        "date": date,
        "time": time,
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

