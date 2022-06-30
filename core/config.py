# Local libraries
from core.uncolor import uncolor

# Internal python libraries
from configparser import ConfigParser
from os.path import isfile
from sys import exit

config = ConfigParser()

if not isfile('config.ini'):
    print(uncolor('WARNING: Config file not detected, fill config.ini and run the program again', ['yellow']))
    # Server section
    config['peerfinder'] = {}
    config['peerfinder']['server'] = 'https://cojin-peerfinder.glitch.me'
    # RPC section
    config['RPC'] = {}
    config['RPC']['wait'] = '1'
    # Ngrok section
    config['ngrok'] = {}
    config['ngrok']['enabled'] = 'true'
    with open('config.ini', 'w') as file:
        config.write(file)
        file.close()
    exit()
else:
    config.read('config.ini')
