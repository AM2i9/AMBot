import logging
from logging import handlers
from pathlib import Path

format_str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
log_format = logging.Formatter(format_str)

log_file = Path("logs", "bot.log")
log_file.parent.mkdir(exist_ok=True)
logging.getLogger("discord").setLevel(logging.INFO)
file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=7, encoding="utf8")
file_handler.setFormatter(log_format)

root = logging.getLogger()
root.addHandler(file_handler)

root.setLevel(logging.INFO)

logging.getLogger('discord').setLevel(logging.WARNING)