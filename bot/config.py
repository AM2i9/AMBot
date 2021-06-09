from pathlib import Path

from configparser import ConfigParser

CONFIG_PATH = 'bot.conf'

_parser = ConfigParser()

if Path(CONFIG_PATH).exists():    
    _parser.read(CONFIG_PATH)
else:
    raise FileNotFoundError(f"No such config file: '{CONFIG_PATH}'")

class ConfigLoader(type):

    def __getattr__(cls, name):
        name = name.lower()

        try:
            return _parser[cls.section][name]
        except KeyError as e:
            raise AttributeError(repr(name)) from e
    
    def __getitem__(cls, name):
        return cls.__getattr__(name)

class Bot(metaclass=ConfigLoader):
    section = "bot"

    token: str
    prefix: str