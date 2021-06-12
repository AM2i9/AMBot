import logging
import sys

import bot.log

bot.log.setup_log()

debug = "debug" in sys.argv

log = logging.getLogger()

instance = None