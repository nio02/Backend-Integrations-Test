# Backend Integration Test

import sys
from datetime import datetime

top_n = 5
total_logs_counter = 0
total_ips = {}
total_host = {}

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


#Function to count how many times appear an id

def count_ips(data):
    ip_list = [d["client_ip"] for d in data]

    for ip in ip_list:
        if ip in total_ips:
            total_ips[ip] += 1
        else:
            total_ips[ip] = 1

def count_hosts(data):
    host_list = [d["host"] for d in data]

    for host in host_list:
        if host in total_host:
            total_host[host] += 1
        else:
            total_host[host] = 1

#Read file and use data.

def read_logs(rute):
    global total_logs_counter
    global top_n
    chunk = 500
    request_body = []

    with open(rute, "r") as f:
        for line in f:
            total_logs_counter += 1
            data = parse_log_data(line)
            request_body.append(data)
            if len(request_body) >= chunk:
                count_ips(request_body)
                count_hosts(request_body)
                
                #SendToApi

                request_body = []
    
    print(total_logs_counter)


file = sys.argv[1]
read_logs(file)

