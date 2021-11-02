import configparser
import os

beserver = ''


def beserveradd():
    global beserver

    path_current_directory = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config_path = os.path.join(path_current_directory, 'beserver.ini')

    config.read(config_path)
    beserver = config['DEFAULT']['serveradd']
