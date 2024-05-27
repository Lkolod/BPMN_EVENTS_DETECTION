from datetime import datetime,timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
from collections import Counter


def load_file(file_name: str):
    logs = []
    with open(file_name, 'r') as file:
        for line in file:
            logs.append(line.strip())

    return logs

def get_message_times(logs: List[str]):
    message_times = {}

    for log in logs:
        id, time_start, time_end, text = log.split(',',3)
        timestamp = datetime.strptime(time_start, "%Y-%m-%d %H:%M")
        message = text.strip()

        if message not in message_times.keys():
            message_times[message] = [timestamp]
        else:
            message_times[message].append(timestamp)

    return message_times


def get_message_hours_occurance(message_times: Dict[str, List[datetime]], delta_minutes):
    message_repeatability = {}

    for message, times in message_times.items():
        times_occurance = {}
        for time in times:
            hour = time.hour
            times_occurance[hour] = 1 + times_occurance.get(hour, 0)

        message_repeatability[message] = times_occurance

    return message_repeatability


def round_time_to_nearest_anchor(dt: datetime, anchor_interval: timedelta, flexibility: timedelta) -> datetime:
    """
    Rounds a datetime object to the nearest time anchor with a specified level of flexibility.

    Args:
    - dt (datetime): The datetime to round.
    - anchor_interval (timedelta): The interval between anchors (e.g., 1 hour).
    - flexibility (timedelta): The flexibility around the anchor (e.g., 15 minutes).

    Returns:
    - datetime: The rounded datetime.
    """
    # Calculate the number of intervals since the minimum datetime
    num_intervals = (dt - datetime.min) // anchor_interval
    closest_anchor = datetime.min + num_intervals * anchor_interval

    # Check if the time falls within the flexibility window around the anchor
    if dt < closest_anchor:
        if closest_anchor - dt > flexibility:
            closest_anchor -= anchor_interval
    else:
        if dt - closest_anchor > flexibility:
            closest_anchor += anchor_interval

    return closest_anchor

def analyze_cyclic_behaviors(message_times: Dict[str, List[datetime]], flexibility_minutes: int) -> Dict[str, Counter]:

    results = defaultdict(lambda: defaultdict(Counter))
    flexibility = timedelta(minutes=flexibility_minutes)
    anchor_interval = timedelta(minutes=30)

    for event, times in message_times.items():
        for time in times:
            rounded_time = round_time_to_nearest_anchor(time, anchor_interval, flexibility)
            hour = rounded_time.hour
            day = rounded_time.day
            results[event][day][hour] += 1

    return results


def detect_daily_patterns(results: Dict[str, Dict[int, Counter]], min_daily_percent: float) -> Dict[str, List[str]]:

    daily_pat = defaultdict(list)
    hourly_pat = defaultdict(list)

    for event, daily_patterns in results.items():
        total_days = len(daily_patterns)
        hourly_counts = Counter(hour for day_counts in daily_patterns.values() for hour in day_counts)
        hourly_percentages = {hour: count / total_days for hour, count in hourly_counts.items() if count / total_days >= min_daily_percent}
        daily_pat[event].append(hourly_percentages)


    return daily_pat

def check_cyclicality(message_times: Dict[str, List[datetime]], common_intervals: Dict[str, timedelta],
                      delta: timedelta) -> Dict[str, bool]:
    """
    Checks if events occur cyclically based on the deduced most common interval.

    Args:
    - message_times (Dict[str, List[datetime]]): Event timestamps.
    - common_intervals (Dict[str, timedelta]): Most common intervals for each message.
    - delta (timedelta): Allowed deviation for each interval check.

    Returns:
    - Dict[str, bool]: Whether each event is cyclic.
    """
    cyclic_results = {}
    for message, common_interval in common_intervals.items():
        times = sorted(message_times[message])
        is_cyclic = True

        for i in range(len(times) - 1):
            actual_interval = times[i + 1] - times[i]
            if not (common_interval - delta <= actual_interval <= common_interval + delta):
                is_cyclic = False
                break

        cyclic_results[message] = is_cyclic

    return cyclic_results

def detect_timer(message_times: Dict[str, Dict[int, int]]):
    for message, hour_occurances in message_times.items():
        occ_values = list(hour_occurances.values())
        response = all(occ == occ_values[0] for occ in occ_values)

        if response:
            print(f'Possible timer for {message} event')
        else:
            print('Timer not possible')


if __name__ == '__main__':
    file_name = '../src/bpmn_event_logs.txt'
    logs = load_file(file_name)

    message_times = get_message_times(logs)
    #result = get_message_hours_occurance(message_times, 2)
    results = analyze_cyclic_behaviors(message_times, 15)  # 15 minutes flexibility
    min_daily_percent = 0.8  # At least 80% of days for considering an event as repeating each day
    daily_patterns = detect_daily_patterns(results, min_daily_percent)

    # Print the detected daily patterns
    for event, event_patterns in daily_patterns.items():
        print(f"Event: {event}")
        for pattern in event_patterns:
            for pat,value in pattern.items():
                value = value *100
                print(f"event occurs at hour: {pat} daily  {value}% of the time")



#TODO rozszerzyc logi
