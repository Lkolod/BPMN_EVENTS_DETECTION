from datetime import datetime, timedelta
from typing import List, Dict


def load_file(file_name: str):
    logs = []
    with open(file_name, 'r') as file:
        for line in file:
            logs.append(line.strip())

    return logs

def get_message_times(logs: List[str]):
    start_message_times = {}
    end_message_times = {}

    for log in logs:
        _, start_time, end_time, text = log.split(',')
        start_timestamp = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_timestamp = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        message = text.strip()

        if message not in start_message_times.keys():
            start_message_times[message] = [start_timestamp]
        else:
            start_message_times[message].append(start_timestamp)

        if message not in end_message_times.keys():
            end_message_times[message] = [end_timestamp]
        else:
            end_message_times[message].append(end_timestamp)

    return start_message_times, end_message_times

def generate_key_by_hour_and_minutes(hour: int, minute: int, delta: int):
    total_minutes = hour * 60 + minute
    rounded_minutes = (total_minutes // delta) * delta

    rounded_hour = rounded_minutes // 60
    rounded_minute = rounded_minutes % 60

    minute_str = '0' + str(rounded_minute) if rounded_minute < 10 else str(rounded_minute)
    return f'{rounded_hour}:{minute_str}'

def generate_key_by_day(day: int, delta: int):
    adjusted_day = day - 1
    key = (adjusted_day // delta) * delta + 1
    return key

def get_message_hours_occurance(message_times: Dict[str, List[datetime]], delta_minutes: int):
    message_repeatability = {}

    for message, times in message_times.items():
        times_occurance = {}
        sorted_times = sorted(times)

        for time in sorted_times:
            key = generate_key_by_hour_and_minutes(time.hour, time.minute, delta_minutes)
            times_occurance[key] = 1 + times_occurance.get(key, 0)

        message_repeatability[message] = times_occurance

    return message_repeatability

def get_message_days_occurance(message_times: Dict[str, List[datetime]], delta_days: int):
    message_repeatability = {}

    for message, times in message_times.items():
        times_occurance = {}
        sorted_times = sorted(times)

        for time in sorted_times:
            key = generate_key_by_day(time.day, delta_days)
            times_occurance[key] = 1 + times_occurance.get(key, 0)

        message_repeatability[message] = times_occurance

    return message_repeatability

def calc_time_between_first_and_last_log(logs: List[str]):
    _, first_log_start_date, _, _ = logs[0].split(",")
    _, _, last_log_end_date, _ = logs[-1].split(",")

    first_timestamp = datetime.strptime(first_log_start_date, "%Y-%m-%d %H:%M")
    last_timestamp = datetime.strptime(last_log_end_date, "%Y-%m-%d %H:%M")
    
    return last_timestamp - first_timestamp

def detect_timer(message_times: Dict[str, Dict[int, int]]):
    for message, hour_occurances in message_times.items():
        occ_values = list(hour_occurances.values())
        response = all(occ == occ_values[0] for occ in occ_values)

        if response:
            print(f'Possible timer event - {message}')
        else:
            print('Timer not possible')
        

if __name__ == '__main__':
    # Set parameters, delta must be > 0
    FILE_PATH = './src/bpmn_event_logs.txt'
    DELTA_FOR_MINUTES = 10
    DELTA_FOR_DAYS = 1

    logs = load_file(FILE_PATH)
    time_window = calc_time_between_first_and_last_log(logs)
    start_message_times, end_massage_times = get_message_times(logs)

    if timedelta(days=365) < time_window:
        pass
    elif timedelta(days=31) < time_window <= timedelta(days=365):
        start_day_result = get_message_days_occurance(start_message_times, DELTA_FOR_DAYS)
        end_day_result = get_message_days_occurance(start_message_times, DELTA_FOR_DAYS)
        # print(start_day_result)
        # print(end_day_result)
        # detect_timer(start_day_result)
    else:
        start_hour_result = get_message_hours_occurance(start_message_times, DELTA_FOR_MINUTES)
        end_hour_result = get_message_hours_occurance(end_massage_times, DELTA_FOR_MINUTES)

        print(start_hour_result)
        detect_timer(start_hour_result)