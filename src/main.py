import messages as m
import times as t


def load_file(file_name: str):
    logs = []
    with open(file_name, 'r') as file:
        for line in file:
            logs.append(line.strip())

    return logs


if __name__ == '__main__':
    # Constants
    MINUTES_THRESHOLD = 20
    DAILY_THRESHOLD = 0.85
    MESSAGES_THRESHOLD = 0.85

    # Loading file
    file_name = './data/real/preprocessed/repairExample.txt'
    # test_name = './data/test/project_logs.txt'
    logs = load_file(file_name)

    # Times part
    print('------------ Times part ------------')
    message_times = t.get_message_times(logs)
    results = t.analyze_cyclic_behaviors(message_times, MINUTES_THRESHOLD)
    daily_patterns = t.detect_daily_patterns(results, DAILY_THRESHOLD)
    t.show_detected_daily_patterns(daily_patterns)

    # Messages part
    print('------------ Messages part ------------')
    m.summary_in_intervals_logs(logs, MINUTES_THRESHOLD)
    m.find_messages_dependency(logs, MESSAGES_THRESHOLD)