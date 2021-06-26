import json
import os
import argparse
import re
from collections import defaultdict
count_request = 0
list_of_files = []
parser = argparse.ArgumentParser(description="путь для директории")

parser.add_argument("-f", dest="path", default="logs/", action='store', help="Path to logfile")
args = parser.parse_args()

dict_ip = defaultdict(
    lambda: {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
)

list_files_of_directory = os.listdir(args.path)

for file in list_files_of_directory:
    with open(args.path + f'{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                ip = ip_match.group()
                try:
                    method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line).groups()[0]
                    count_request += 1
                except AttributeError:
                    break
                dict_ip[ip][method] += 1





def counter_type_of_request(type_of_request: str):
    counter = 0
    for file in list_files_of_directory:
        with open(args.path + f'{file}') as log:
            for line in log:
                request = re.search(rf'\] \"({type_of_request})', line)
                if request is not None:
                    counter += 1
                    request.group()

    return counter


def counter_ip_adresse():
    counter = 0
    for file in list_files_of_directory:
        with open(args.path + f'{file}') as log:
            for line in log:
                request = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                if request is not None:
                    counter += 1
                    request.group()

    return counter




print(counter_type_of_request("GET"))
print(counter_type_of_request("POST"))
print(counter_type_of_request("PUT"))
print(counter_type_of_request("DELETE"))
print(counter_type_of_request("HEAD"))



print(json.dumps(dict_ip, indent=4))
print(f"количетство запросов равно {counter_ip_adresse()}")

