from datetime import datetime
from typing import List, Dict


def load_file(file_name: str):
    logs = []
    with open(file_name, 'r') as file:
        for line in file:
            logs.append(line.strip())

    return logs

def get_message_times(logs: List[str]):
    message_times = {}

    for log in logs:
        _, time, text = log.split(',')
        timestamp = datetime.strptime(time, "%Y-%m-%d %H:%M")
        message = text.strip()

        if message not in message_times.keys():
            message_times[message] = [timestamp]
        else:
            message_times[message].append(timestamp)

    return message_times

def get_message_hours_occurance(message_times: Dict[str, List[datetime]], delta_minutes: int):
    message_repeatability = {}

    for message, times in message_times.items():
        times_occurance = {}
        for time in times:
            hour = time.hour
            times_occurance[hour] = 1 + times_occurance.get(hour, 0)

        message_repeatability[message] = times_occurance

    return message_repeatability

def detect_timer(message_times: Dict[str, Dict[int, int]]):
    for message, hour_occurances in message_times.items():
        occ_values = list(hour_occurances.values())
        response = all(occ == occ_values[0] for occ in occ_values)

        if response:
            print(f'Possible timer for {message} event')
        else:
            print('Timer not possible')
        

if __name__ == '__main__':
    file_name = './src/bpmn_event_logs.txt'
    logs = load_file(file_name)

    message_times = get_message_times(logs)
    result = get_message_hours_occurance(message_times, 2)

    print(result)
    detect_timer(result)