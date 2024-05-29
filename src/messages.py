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
            print(f'Log "{inner_log}" occurs {v} times in log "{outer_log}". Regulary nested events.')

def summary_in_intervals_logs(logs: List[str], delta_minutes: int):
    intervals = check_intervals_logs(logs, delta_minutes)
    N = len(list(intervals.keys()))

    if N != 0:
        for key, arr in intervals.items():
            prev_log, next_log = key.split("-")
            avg_time = round(sum(arr) / len(arr), 0)

            print(f"Possible timer between {prev_log} & {next_log}. One follows the other regulary after {avg_time} minutes")
    else:
        print('No timer detected between ending time and starting time in any events.')

def check_intervals_logs(logs: List[str], delta_minutes: int):
    parsed_logs = [parse_log(log) for log in logs]
    wrong_patterns = set()
    intervals = {}

    
    for i in range(len(parsed_logs) - 1):
        prev_id, _, prev_end_time, prev_message = parsed_logs[i]
        curr_id, curr_start_time, _, curr_message = parsed_logs[i + 1]

        if prev_message != curr_message and prev_id == curr_id and curr_start_time > prev_end_time:
            interval = int((curr_start_time - prev_end_time).total_seconds() / 60)
            key = f"{curr_message}-{prev_message}"

            if key not in intervals.keys():
                intervals[key] = [interval]
            else:
                valid_interval = intervals[key][0]
                if abs(interval - valid_interval) <= delta_minutes:
                    intervals[key].append(interval)
                else:
                    wrong_patterns.add(key)
                
    for key in list(intervals.keys()):
        if key in wrong_patterns:
            del intervals[key]

    return intervals

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