import json
import os
import argparse
import re
from collections import defaultdict

list_of_files = []

parser = argparse.ArgumentParser(description="путь для директории")
parser.add_argument("-f", dest="path", default="logs/", action='store', help="Path to logfile")
args = parser.parse_args()




list_files_of_directory = os.listdir(args.path)



def log_parser(list_files_of_directory):
    dict_ip = defaultdict(
        lambda: {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    )
    count_request = 0
    for file in list_files_of_directory:
        with open(args.path + f'{file}') as log:
            for line in log:
                ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                time_1 = re.search(r'\d+$', line)
                if ip_match is not None:
                    ip = ip_match.group()
                    method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line)
                    url = line.split()[6]
                    if method is not None:
                        method = method.groups()[0]
                        count_request += 1
                        dict_ip[ip][method] += 1
                        if time_1 is not None:
                            time_1 = time_1.group()
                            dict_ip[ip]['time'] = int(time_1)
                            dict_ip[ip]['url'] = url
            return dict_ip




print(json.dumps(log_parser(list_files_of_directory), indent=4))


