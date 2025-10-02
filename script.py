# Backend Integration Test

import sys
from datetime import datetime
import requests
import os

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


#Function to count how many times appear a given data

def count_data(data, key):
    if key == "client_ip":
        if data in total_ips:
            total_ips[data] += 1
        else:
            total_ips[data] = 1
    if key == "host":
        if data in total_host:
            total_host[data] += 1
        else:
            total_host[data] = 1


#Ranking Function

def ranking(total_data, n_elements):
    rank_data = []

    for data, count in total_data.items():
        rank_data.append((data, count))

    rank_data.sort(key=lambda x: x[1], reverse = True)

    return rank_data[:n_elements]


#Show info in console

def show_info(rank_data):
    max_data_len = max(len(data) for data, _ in rank_data)
    max_datacount_len = max(len(str(count)) for _, count in rank_data)

    print(f"{'-'*max_data_len}  {'-'*max_datacount_len}  {'-'*6}")

    row_format = f"{{:<{max_data_len}}}  {{:>{max_datacount_len}}}  {{:>5.2f}}%"

    for data, count in rank_data:
        percentage = (count / total_logs_counter) * 100
        print(row_format.format(data, count, percentage))
    
    print(f"{'-'*max_data_len}  {'-'*max_datacount_len}  {'-'*6}\n")

#Send Http request to the API

def send_Request(request_data):
    url = "https://api.lumu.io"
    collector_id = os.getenv("COLLECTOR_ID")
    lumu_client_key = os.getenv("LUMU_CLIENT_KEY")

    response = requests.post(
        f"{url}/collectors/{collector_id}/dns/queries?key={lumu_client_key}",
        json=request_data,
        headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Request sent successfully")
    else:
        print("Error sending request")


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
            count_data(data["client_ip"], "client_ip")
            count_data(data["host"], "host")

            request_body.append(data)

            if len(request_body) >= chunk:
                send_Request(request_body)
                request_body = []

    if request_body:
        send_Request(request_body)
    
    rank_ips = ranking(total_ips, top_n)
    rank_host = ranking(total_host, top_n)

    print(f"\nTotal records {total_logs_counter}\n")
    print("Client IPs Rank")
    show_info(rank_ips)
    print("Client Host Rank")
    show_info(rank_host)

file = sys.argv[1]
read_logs(file)