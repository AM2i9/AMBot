import os
from pathlib import Path

from configparser import ConfigParser

try:
    import dotenv
    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass

CONFIG_PATH = 'bot.conf'

_parser = ConfigParser()

_parser.read(CONFIG_PATH)

class ConfigLoader(type):

    def __getattr__(cls, name):
        name = name.lower()

        try:
            config_value = _parser[cls.section][name]
        except KeyError as e:
            raise AttributeError(repr(name)) from e

        if str(config_value).lower().startswith('!env.'):
            
            try:
                env_name = str(config_value).split('.', maxsplit=1)[1]
                return os.environ.get(env_name)
            except KeyError as e:
                raise AttributeError(repr(name)) from e

        else:
            
            return config_value
    
    def __getitem__(cls, name):
        return cls.__getattr__(name)

class Bot(metaclass=ConfigLoader):
    section = "bot"

    token: str
    prefix: str