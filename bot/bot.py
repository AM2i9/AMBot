import asyncio
import logging
import discord
from discord.ext import commands

import bot.config as conf

log = logging.getLogger('bot')

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.ready = False
        
        super().__init__(*args, **kwargs)
    
    @classmethod
    def create(cls):
        loop = asyncio.get_event_loop()
        
        intents = discord.Intents.all()
        return cls(
            command_prefix=commands.when_mentioned_or(conf.Bot.prefix),
            loop=loop,
            intents=intents
        )

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            log.info(f'Bot logged in as {self.user}')
        else:
            log.info('Bot reconnected')