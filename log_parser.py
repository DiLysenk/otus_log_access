import json
import os
import argparse
import re
from collections import defaultdict

list_of_files = []

parser = argparse.ArgumentParser(description="путь для директории")
parser.add_argument("-f", dest="path", default="logs/", action='store', help="Path to logfile")
args = parser.parse_args()

file_list_of_directory = os.listdir(args.path)


def log_parser(file_list: list):
    dict_ip = defaultdict(
        lambda: {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    )
    for file in file_list:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if ip_match is not None:
                    ip = ip_match.group()
                    method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line)
                    if method is not None:
                        method = method.groups()[0]
                        dict_ip[ip][method] += 1
            return dict_ip


def top_3_log_parser(file_list):
    top_requests = {'#1': {'ip': '', 'url': '', 'time': 0},
                    '#2': {'ip': '', 'url': '', 'time': 0},
                    '#3': {'ip': '', 'url': '', 'time': 0}}
    for file in file_list:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                time_r = re.search(r'\d+$', line)
                if ip_match is not None:
                    ip_match = ip_match.group()
                    if time_r is not None:
                        time_r = int(time_r.group())
                        url = line.split()[6]
                        for i in range(3, 0, -1):
                            if time_r > top_requests[f'#{i}']['time']:
                                if top_requests[f'#{i}']['time'] != ip_match:
                                    top_requests[f'#{i}']['time'] = time_r
                                    top_requests[f'#{i}']['ip'] = ip_match
                                    top_requests[f'#{i}']['url'] = url
                                    break
            return top_requests


def count_request_parser(file_list):
    count_request = 0
    for file in file_list:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if ip_match is not None:
                    count_request += 1
            return count_request



def top_3_ip_cont_request(file_list):
    cont_requests = {}
    top_ip = {"#1": {'ip': '', 'count': 0},
            "#2": {'ip': '', 'count': 0},
            "#3": {'ip': '', 'count': 0}}
    for file in file_list:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if ip_match is not None:
                    ip_match = ip_match.group()
                    try:
                        cont_requests[ip_match] += 1
                    except:
                        cont_requests[ip_match] = 1


            for ip in cont_requests:
                for i in range(3, 0, -1):
                    if top_ip[f'#{i}']['count'] < cont_requests[ip]:
                        top_ip[f'#{i}']['ip'] = ip
                        top_ip[f'#{i}']['count'] = cont_requests[ip]
                        break
            return top_ip



def counter_requests(file_list):
    dict_requests = {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    for file in file_list:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if ip_match is not None:
                    method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line)
                    if method is not None:
                        method = method.groups()[0]
                        dict_requests[method] += 1


            return dict_requests






# print(json.dumps(log_parser(file_list_of_directory), indent=4))
# print(json.dumps(top_3_log_parser(file_list_of_directory), indent=4))
# print(json.dumps(counter_requests(file_list_of_directory), indent=2))
# print(json.dumps(top_3_ip_cont_request(file_list_of_directory), indent=2))
print(json.dumps(top_3_ip_cont_request(file_list_of_directory), indent=2))