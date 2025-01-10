import configparser
import os.path

from TM1py.Services import TM1Service

class ConfigConnector:
    @staticmethod
    def connect_to_standard_objects():
        return ConfigConnector.__connect_to_tm1('Standard Objects')

    @staticmethod
    def connect_to_blank_training():
        return ConfigConnector.__connect_to_tm1('Blank Training')

    @staticmethod
    def __connect_to_tm1(server_config_name : str):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config_path = os.path.abspath(config_path)
        config.read(config_path)

        standard_objects_params = config[server_config_name]
        with TM1Service(**standard_objects_params) as tm1:
            print('connected to ' + tm1.server.get_server_name())
        return tm1

# Repurposed this file to use for other tasks.

def __connect_to_tm1(server_config_name):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config_path = os.path.abspath(config_path)
    config.read(config_path)

    standard_objects_params = config[server_config_name]
    with TM1Service(**standard_objects_params) as tm1:
        print('connected to ' + tm1.server.get_server_name())
    return tm1

def connect_to_standard_objects():
    return __connect_to_tm1('Standard Objects')

def connect_to_blank_training():
    return __connect_to_tm1('Blank Training')