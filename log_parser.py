import json
import os
import argparse
import re

parser = argparse.ArgumentParser(description="путь для директории")
parser.add_argument("-f", dest="path", default="logs/", action='store', help="Path to logfile")
args = parser.parse_args()


def top_3_log_parser(agr_path, file_of_log: str, kostil='/'):
    """топ 3 самых долгих запросов, url, ip, время запроса """
    top_requests = {'#1': {'request': '', 'ip': '', 'url': '', 'time': 0},
                    '#2': {'request': '', 'ip': '', 'url': '', 'time': 0},
                    '#3': {'request': '', 'ip': '', 'url': '', 'time': 0}}
    with open(agr_path + kostil + file_of_log) as log:
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


def count_request_parser(agr_path, file_of_log: str, kostil='/'):
    """общее количество выполненных запросов"""
    count_request = 0
    with open(agr_path + kostil + file_of_log) as log:
        for line in log:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                count_request += 1
        print("----------count_request_parser общее количество выполненных запросов-------\n",
              json.dumps(count_request, indent=4, sort_keys=True))
        return count_request


def top_3_ip_cont_request(agr_path, file_of_log: str, kostil='/'):
    '''топ 3 IP адресов, с которых были сделаны запросы'''
    cont_requests = {}
    top_ip = {"#1": {'ip': '', 'count': 0},
              "#2": {'ip': '', 'count': 0},
              "#3": {'ip': '', 'count': 0}}
    with open(agr_path + kostil + file_of_log) as log:
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


def counter_requests(agr_path, file_of_log: str, kostil='/'):
    """количество запросов по типу: GET - 20, POST - 10 и т.п."""
    dict_requests = {'GET': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0, 'DELETE': 0, 'HEAD': 0}
    with open(agr_path + kostil + file_of_log) as log:
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


if os.path.isfile(args.path):
    file = ""
    name = args.path.split("/")[:0:-1]
    with open(f"result/log_parser--{name[0]}.json", 'w') as result_file:
        json.dump(top_3_log_parser(args.path, file, kostil=''), result_file, indent=4)
        result_file.write(",\r\n")
        json.dump(counter_requests(args.path, file, kostil=''), result_file, indent=4)
        result_file.write(",\r\n")
        json.dump(top_3_ip_cont_request(args.path, file, kostil=''), result_file, indent=4)
        result_file.write(",\r\n")
        json.dump(count_request_parser(args.path, file, kostil=''), result_file, indent=2)
else:
    for file in os.listdir(args.path):
        with open(f"result/log_parser--{file}.json", 'w') as result_file:
            json.dump(top_3_log_parser(args.path, file), result_file, indent=4)
            result_file.write(",\r\n")
            json.dump(counter_requests(args.path, file), result_file, indent=4)
            result_file.write(",\r\n")
            json.dump(top_3_ip_cont_request(args.path, file), result_file, indent=4)
            result_file.write(",\r\n")
            json.dump(count_request_parser(args.path, file), result_file, indent=2)
