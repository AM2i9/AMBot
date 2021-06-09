import logging
import sys

import bot.log

debug = "debug" in sys.argv

log = logging.getLogger()

instance = None