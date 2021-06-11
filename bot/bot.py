import asyncio
import logging
import discord
from discord.ext import commands

from bot import exts
import bot.config as conf
from bot.utils import _Utils

log = logging.getLogger('bot')

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.ready = False
        
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        if not self.ready:
            self.ready = True

            # The print statement is here for the sole reason of satisfying my server's "running" conditions
            print("Logged in")
            
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

        self.add_cog(_Utils(self))
        log.info("Loading utils module")

        for ext in exts.walk():
            try:
                self.load_extension(ext)
                log.info(f"Loaded extension {ext}")
            except Exception as e:
                log.warn(e)