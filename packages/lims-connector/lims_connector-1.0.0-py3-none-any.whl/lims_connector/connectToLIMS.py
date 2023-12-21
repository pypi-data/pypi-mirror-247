import yaml
import configparser
import sqlalchemy
from urllib.parse import quote_plus
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from cmhlims.setConfig import get_config
from pymysql.connections import Connection
Base = declarative_base()

def read_config(file_path='config.ini')-> Connection:
    config = configparser.ConfigParser()

    try:
        with open(file_path) as f:
            config.read_file(f)

        if 'shared' in config:
            config_file = config.get('shared', 'config_file', fallback=None)
            environment = config.get('shared', 'environment', fallback=None)

            return {
                'config_file': config_file,
                'environment': environment
            }
        else:
            return None
    except Exception as e:
        print(f"Error reading configuration: {e}")
        return None

def connect_to_lims(config=None, environment=None):
    config_file = get_config()['config_file']
    environment = get_config()['environment']

    if config_file is None or environment is None:
        raise ValueError(
            "Options cmhlims.lims_config_yaml and cmhlims.lims_environment must be set before using cmhlims functions.")

    with open(config_file, 'r') as file:
        lims_config = yaml.safe_load(file)

    if environment not in lims_config:
        raise ValueError("LIMS environment not found in configuration YAML: " + environment)

    lims_config = lims_config[environment]

    username = lims_config['username']
    password = quote_plus(lims_config['password'])
    hostname = lims_config['host']
    database = lims_config['database']

    ssl_args = {
        'ssl_ca': lims_config['sslca']
    }

    engine = sqlalchemy.create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{database}",
                                      connect_args={'ssl': ssl_args})
    return engine

db_engine=connect_to_lims()
