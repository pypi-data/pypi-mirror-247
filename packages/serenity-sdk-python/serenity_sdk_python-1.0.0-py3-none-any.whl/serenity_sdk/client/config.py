import json
import os.path

from enum import Enum
from typing import Any, Optional


class Environment(Enum):
    """
    The operational environment (e.g. test vs. production) to use for connection purposes.
    """
    DEV = 'dev'
    """
    Serenity's development environment
    """

    TEST = 'test'
    """
    Serenity's UAT (QA) environment
    """

    PROD = ''
    """
    Serenity's production environment
    """


class Region(Enum):
    """
    The regional installation of Serenity to use for connection purposes. Not currently used.
    """
    GLOBAL = ''
    EASTUS = 'eastus'
    EASTUS_2 = 'eastus2'


class ConnectionConfig:
    """
    Internal class that handles interpreting the JSON config file generated
    by the Serenity UX API Management function. This class is for internal
    use and normally you should not need to instantiate it.

    .. seealso:: :func:`load_local_config`: utility function to load configs from local files
    """
    def __init__(self, config: Any, config_path: str):
        """
        Builds a connection configuration from a parsed JSON object.

        :param config: a parsed JSON object containing a Serenity API configuration
        :param config_path: for error messages -- the path from which the JSON was loaded
        """
        # basic validation, extract the schema version
        schema_version = ConnectionConfig._validate_config_json(config, config_path)

        # OK, we have a clean object, extract the core fields
        self.schema_version = schema_version
        self.scope = ""
        self.domain = config['domain']
        self.user_audience = config['userAudience']
        self.user_client_id = config.get('userClientId')
        self.client_id = config.get('clientId')
        self.client_secret = config.get('clientSecret')
        self.url = config['url']

        self.env = Environment[config['environment']]

    def get_url(self) -> str:
        """
        Gets the client-specific URL to use for all API requests
        """
        return self.url

    @staticmethod
    def _validate_config_json(config: Any, config_path: str) -> int:
        """
        Validates a config JSON from Serenity and ensures it matches the schema

        :param config: raw config JSON object
        :param config_path: file path from which the JSON was loaded; for error messages
        :return: the schema version loaded (currently 1 or 2)
        """
        critical_keys = ['schemaVersion']
        if not all(key in config for key in critical_keys):
            raise ValueError(f'{config_path} invalid. Required keys: {critical_keys}; got: {list(config.keys())}')
        schema_version = config['schemaVersion']
        if schema_version != 3:
            raise ValueError(f'At this time only schemaVersion == 3 is supported; '
                             f'{config_path} is version {schema_version}')
        device_code_required_keys = ['domain', 'userClientId', 'userAudience']
        client_cred_required_keys = ['domain', 'clientId', 'clientSecret', 'userAudience']
        if (not all(key in config for key in device_code_required_keys)
                and not all(key in config for key in client_cred_required_keys)):
            raise ValueError(
                f'{config_path} invalid. For Device Code Login Required keys: {device_code_required_keys};'
                f' Or Client Credentials Login Required keys: {client_cred_required_keys};'
                f' got: {list(config.keys())}')
        return schema_version


def load_local_config(config_id: str, config_dir: Optional[str] = None) -> ConnectionConfig:
    """
    Helper function that lets you read a JSON config file with client ID and client secret from
    `$HOME/.serenity/${config_id}.json` on your local machine.

    :param config_id: short name of a configuration to load from `$HOME/.serenity`
    :param config_dir: optional override to load from a directory other than `$HOME/,serenity`
    :return: a populated, validated `ConnectionConfig` object to use with `SerenityClient`
    """

    if not config_dir:
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, '.serenity')
    if not config_id.endswith('.json'):
        config_id += '.json'
    config_path = os.path.join(config_dir, config_id)

    # load and parse
    config_file = open(config_path)
    config = json.load(config_file)

    return ConnectionConfig(config, config_path)
