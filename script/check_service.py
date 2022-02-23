import psutil

stop_sv = [
    'SERVER-25802',
    'SERVER-44501',
    'SERVER-05402',
    'SERVER-03502',
    'SERVER-47301',
    'SERVER-08702',
    'SERVER-41901',
    'SERVER-29001',
    'SERVER-42001',
    'SERVER-34202',
    'SERVER-47101',
    'SERVER-55302',
    'SERVER-13401',
    'SERVER-38501',
    'SERVER-38502',
    'SERVER-55102',
    'SERVER-49801',
    'SERVER-07301',
    'SERVER-34701'
]

services = list(psutil.win_service_iter())
service = []

for i in services:
    service_name = i.name()
    s = psutil.win_service_get(service_name)
    if s.as_dict()['description'] == 'PS Game Server':
        service.append(s.as_dict()['name'])

for s in service:
    for ss in stop_sv:
        if s == ss:
            print(s)