import json
import os
import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser(description="путь для директории")
parser.add_argument("-f", dest="path", default="logs", action='store', help="Path to logfile")

args = parser.parse_args()

def files_in_derectory(path):
    j = 1
    file_list_of_directory = os.listdir(path)
    for i in file_list_of_directory:
        print(j, ". ", i)
        j += 1
    try:
        choose_number = int(input('введите номер файла для анализа логов:'))
    except:
        "нет такого номера"
    try:
        choose_file = file_list_of_directory[choose_number - 1]
        print(f"выбран файл {choose_file}, обработка может занять некоторое время")
    except:
        choose_file = None
        print("вы не выбрали файл или нет файла с таким номером")
        exit()
    return choose_file


file = files_in_derectory(args.path)


def log_parser(file: str):
    dict_ip = defaultdict(
        lambda: {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    )
    with open(args.path + f'/{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                ip = ip_match.group()
                method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line)
                if method is not None:
                    method = method.groups()[0]
                    dict_ip[ip][method] += 1
        return dict_ip


def top_3_log_parser(file: str):
    """топ 3 самых долгих запросов, url, ip, время запроса """
    top_requests = {'#1': {'request': '', 'ip': '', 'url': '', 'time': 0},
                    '#2': {'request': '', 'ip': '', 'url': '', 'time': 0},
                    '#3': {'request': '', 'ip': '', 'url': '', 'time': 0}}
    with open(args.path + f'/{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            time_r = re.search(r'\d+$', line)
            if ip_match is not None:
                ip_match = ip_match.group()
                if time_r is not None:
                    time_r = int(time_r.group())
                    url = line.split()[6]
                    request = line.split()[5]
                    for i in range(1, 4):
                        if time_r > top_requests[f'#{i}']['time']:
                            if top_requests[f'#{i}']['time'] != ip_match:
                                top_requests[f'#{i}']['request'] = request[1:]
                                top_requests[f'#{i}']['time'] = time_r
                                top_requests[f'#{i}']['ip'] = ip_match
                                top_requests[f'#{i}']['url'] = url
                                break
        print("---------top_requests топ 3 самых долгих запроса-------\n",
              json.dumps(top_requests, indent=4, sort_keys=True))
        return top_requests


def count_request_parser(file: str):
    """общее количество выполненных запросов"""
    count_request = 0
    with open(args.path + f'/{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                count_request += 1
        print("----------count_request_parser общее количество выполненных запросов-------\n",
              json.dumps(count_request, indent=4, sort_keys=True))
        return count_request


def top_3_ip_cont_request(file: str):
    '''топ 3 IP адресов, с которых были сделаны запросы'''
    cont_requests = {}
    top_ip = {"#1": {'ip': '', 'count': 0},
              "#2": {'ip': '', 'count': 0},
              "#3": {'ip': '', 'count': 0}}
    with open(args.path + f'/{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                ip_match = ip_match.group()
                try:
                    cont_requests[ip_match] += 1
                except:
                    cont_requests[ip_match] = 1
        for i in range(3):
            ip = max(cont_requests, key=cont_requests.get)  # находит максимум из из словаря
            count = cont_requests.pop(ip)
            top_ip[f'#{i + 1}']['ip'] = ip
            top_ip[f'#{i + 1}']['count'] = count
        print("--------top_3_ip_cont_request топ 3 IP адресов, с которых были сделаны запросы--------\n",
              json.dumps(top_ip, indent=4, sort_keys=True))
        return top_ip


def counter_requests(file: str):
    """количество запросов по типу: GET - 20, POST - 10 и т.п."""
    dict_requests = {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    with open(args.path + f'/{file}') as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                method = re.search(r'\] \"(POST|GET|PUT|PATCH|DELETE|HEAD)', line)
                if method is not None:
                    method = method.groups()[0]
                    dict_requests[method] += 1
        print("--------counter_requests количество запросов по типу: GET - 20, POST - 10 и т.п.-------\n",
              json.dumps(dict_requests, indent=4, sort_keys=True))
        return dict_requests

try:
    os.mkdir("result")
except:
    pass

with open(f"result/top_3_log_parser--{file}.json", 'w') as result_file:
    json.dump(top_3_log_parser(file), result_file, indent=4)

with open(f"result/counter_requests--{file}.json", 'w') as result_file_1:
    json.dump(counter_requests(file), result_file_1, indent=4)

with open(f"result/top_3_ip_cont_request--{file}.json", 'w') as result_file_2:
    json.dump(top_3_ip_cont_request(file), result_file_2, indent=4)

with open(f"result/count_request_parser--{file}.json", 'w') as result_file_3:
    json.dump(count_request_parser(file), result_file_3, indent=2)
