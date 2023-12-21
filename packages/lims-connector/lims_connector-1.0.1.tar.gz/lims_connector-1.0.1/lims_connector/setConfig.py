import argparse
import configparser
import os

CONFIG_FILE = 'config.ini'

def set_config(_config_file, _environment):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Create 'shared' section if it doesn't exist
    if 'shared' not in config:
        config['shared'] = {}

    config['shared']['config_file'] = _config_file
    config['shared']['environment'] = _environment

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    return {
        "config_file": config.get('shared', 'config_file', fallback=None),
        "environment": config.get('shared', 'environment', fallback=None)
    }

def main():
    parser = argparse.ArgumentParser(description='Update configuration options')
    parser.add_argument('--config-file', '-c', type=str, help='New value for config_file option')
    parser.add_argument('--environment', '-e', type=str, help='New value for environment option')
    args = parser.parse_args()

    if args.config_file and args.environment:
        set_config(args.config_file, args.environment)
        print('Configuration set up successfully.')
    else:
        print('Please provide values for both --config-file and --environment options.')

    print("After setting config:")
    print(get_config())

if __name__ == '__main__':
    main()
