import psutil
import yaml
import shutil
import pymysql
import re, json

services = list(psutil.win_service_iter())
service = []
path = []
no_use_ports = []
update_sve = []
update_path = []

for i in services:
    service_name = i.name()
    s = psutil.win_service_get(service_name)
    if s.as_dict()['description'] == 'Game Server':
        service.append(s.as_dict()['name'])
        path.append(s.as_dict()['binpath'])

for p in path:
    properties_file = p.replace('exe', 'properties')
    with open (properties_file, 'r') as f:
        for line in f:
            if line.find("MySQL.connectionString = host=") != -1:
                hostip = re.split('=|;', line)[2]
            elif line.find("Server.port") != -1:
                sv_port = line.split('=')[1]
    try:
        connection = pymysql.connect(host=hostip, port=3306, user="gm-server", password="password", db="slot-game", connect_timeout=2)
        cur = connection.cursor()
        cur.execute("SELECT server_info FROM `slot-game`.host_id WHERE server_info LIKE '%slot%" + sv_port.strip() + "%';")
        data = cur.fetchone()
        connection.close()
    except:
        print("Can't connect to" + hostip)

    if data != None:
        use_port = ((json.loads(data[0]))['slot'].split(':'))[2]
        if use_port.endswith('1') == True:
            no_use_port = int(use_port) + 1
            no_use_ports.append(str(no_use_port))
        elif use_port.endswith('2') == True:
            no_use_port = int(use_port) - 1
            no_use_ports.append(str(no_use_port))

for nup in set(no_use_ports):
    for p in path:
        if p.find('-' + nup) != -1:
            update_path.append(p.replace('\game-server.exe',''))
    for sve in service:
        if sve.find(nup.zfill(5)) != -1:
            update_sve.append(sve)

dict_file = {'service': update_sve, 'path': update_path}

with open(r'update_info.yml', 'w') as file:
    documents = yaml.dump(dict_file, file)