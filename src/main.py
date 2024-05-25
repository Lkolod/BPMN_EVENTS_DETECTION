from datetime import datetime
from collections import defaultdict

file_name = '../data/bpmn_event_logs.txt'

logs = []
with open(file_name,'r') as file:
    for line in file:
        logs.append(line.strip())


for log in logs:
    id_log,time,text = log.split(',')
    timestamp = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    print(timestamp)

