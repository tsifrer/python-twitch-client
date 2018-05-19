import os
from configparser import ConfigParser

from twitch.constants import CONFIG_FILE_PATH


def _get_config():
    config = ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE_PATH))
    return config


def credentials_from_config_file():
    client_id = None
    oauth_token = None

    config = _get_config()
    if 'Credentials' in config.sections():
        client_id = config['Credentials'].get('client_id')
        oauth_token = config['Credentials'].get('oauth_token')

    return client_id, oauth_token


def backoff_config():
    initial_backoff = 0.5
    max_retries = 3

    config = _get_config()
    if 'General' in config.sections():
        initial_backoff = float(config['General']['initial_backoff'])
        max_retries = int(config['General']['max_retries'])

    return initial_backoff, max_retries
