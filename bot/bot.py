import asyncio
import logging
import discord
from discord.ext import commands

from bot import exts
import bot.config as conf

log = logging.getLogger('bot')

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.ready = False
        
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            log.info(f'Bot logged in as {self.user}')
        else:
            log.info('Bot reconnected')
    
    @classmethod
    def create(cls):
        loop = asyncio.get_event_loop()
        
        intents = discord.Intents.all()
        return cls(
            command_prefix=commands.when_mentioned_or(conf.Bot.prefix),
            loop=loop,
            intents=intents
        )

    def load_extensions(self):
        log.info("Loading extensions...")
        for ext in exts.walk():
            try:
                self.load_extension(ext)
                log.info(f"Loaded extension {ext}")
            except Exception as e:
                log.warn(e)