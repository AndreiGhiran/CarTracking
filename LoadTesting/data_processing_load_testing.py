import os
import requests

from configparser import ConfigParser
from time import sleep


CLIENTS_NUM = 10

WAIT_TIME = 5

SUCCESS_CONDITIONS = lambda response: response.status_code == 200 and response.json()['load'] == 'pong'

class TERMINAL_FONT:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def setup(clients_num):
    print('Instantiating a server instance and {} clients...'.format(clients_num))
    print()

    os.system('start cmd /k "cd ../DataProcessing/Dispatcher/src && python3 main.py"')
    print('Instantiated server')

    for i in range(CLIENTS_NUM):
        os.system('start cmd /k "cd ../Camera/src && python3 main.py test1.mp4 0 0 0 0"')
        print('Instantiated client #{}'.format(i + 1))
    print()

def wait(wait_time):
    print('Waiting for {} seconds...'.format(wait_time))
    sleep(wait_time)
    print()

def test(success_conditions):
    print('Testing success conditions...')
    print()

    config_parser = ConfigParser()
    config_parser.read('configuration/data_processing_authority.config')
    data_processing_authority_dispatcher_data = {
        'ip': config_parser.get('dispatcher', 'ip'),
        'port': config_parser.get('dispatcher', 'port')
    }

    url = '{}:{}/ping'.format(data_processing_authority_dispatcher_data['ip'], data_processing_authority_dispatcher_data['port'])
    response = requests.get(url)

    success = success_conditions(response)
    if success:
        print(f'{TERMINAL_FONT.UNDERLINE}{TERMINAL_FONT.BOLD}{TERMINAL_FONT.OKGREEN}Success!{TERMINAL_FONT.ENDC}')
    else:
        print(f'{TERMINAL_FONT.UNDERLINE}{TERMINAL_FONT.BOLD}{TERMINAL_FONT.FAIL}Failure!{TERMINAL_FONT.ENDC}')


if __name__ == "__main__":
    setup(CLIENTS_NUM)
    wait(WAIT_TIME)
    test(SUCCESS_CONDITIONS)
