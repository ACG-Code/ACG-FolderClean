import configparser
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
standard_objects_params = {
    'address' : 'vm-training.acg.local',
    'port' : 14479,
    'user': 'admin',
    'password' : 'apple',
    'ssl' : True,
}

blank_training_params = {
    'address' : 'vm-training.acg.local',
    'port' : 42375,
    'user': 'admin',
    'password' : 'apple',
    'ssl' : True,
}
config['Standard Objects'] = standard_objects_params
config['Blank Training'] = blank_training_params

with open('config.ini', 'w') as configfile:
    config.write(configfile)

with TM1Service(**standard_objects_params) as tm1:
    print(tm1.server.get_server_name())