import bot
import bot.log
from bot.bot import Bot

import bot.config as conf

bot.instance = Bot.create()
bot.instance.load_extensions()
bot.instance.run(conf.Bot.token)