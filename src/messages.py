from typing import Dict, List, Tuple
from datetime import datetime


def find_messages_dependency(logs: List[str], threshold: float):
    parsed_logs = [parse_log(log) for log in logs]

    dependency_count = count_inside_logs(logs)
    occ = count_logname_occurancy(parsed_logs)

    for k, v in dependency_count.items():
        inner_log, outer_log = k.split('-')
        inner_occ, outer_occ = occ[inner_log], occ[outer_log]

        if (inner_occ / outer_occ) >= threshold:
            print(f'Log "{inner_log}" occurs {v} times in log "{outer_log}"')
            print('It can be possible message boundary item.')
            print('----------------------------------------------')

        
def parse_log(log: str):
    id, start, end, text = log.split(',')
    start_timestamp = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_timestamp = datetime.strptime(end, "%Y-%m-%d %H:%M")
    message = text.strip()

    return id, start_timestamp, end_timestamp, message

def count_logname_occurancy(parsed_logs: List[Tuple[str, datetime, datetime, str]]):
    occ = {}

    for _, _, _, message in parsed_logs:
        occ[message] = 1 + occ.get(message, 0)

    return occ

def count_inside_logs(logs: List[str]) -> Dict[str, int]:
    parsed_logs = [parse_log(log) for log in logs]
    dependency_count = {}
    l = 0

    for r in range(1, len(parsed_logs)):
        _, start_l, end_l, text_l = parsed_logs[l]
        _, start_r, end_r, text_r = parsed_logs[r]

        if start_l <= start_r <= end_r <= end_l:
            key = f"{text_r}-{text_l}"
            dependency_count[key] = 1 + dependency_count.get(key, 0)
        else:
            l = r

    return dependency_count