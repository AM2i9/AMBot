import logging

import discord
from discord.ext import commands

log = logging.getLogger('bot')

class _Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True, description="Owner utils")
    async def utils(self,ctx):
        await ctx.invoke(self.bot.get_command("help"), "_Utils")

    @utils.command(description="List all loaded extensions")
    @commands.is_owner()
    async def listexts(self, ctx):
        await ctx.reply("The following extensions are loaded: ```%s```" % ('\n'.join(self.bot.extensions)))

    @utils.command(description="Reload extensions")
    @commands.is_owner()
    async def reload(self,ctx, *exts):

        if not exts:
            await ctx.reply("Please specify which extensions to reload")
            return

        msg = await ctx.reply("Reloading extensions...")
        log.info(f'Reload called in channel {ctx.channel.id}')
        
        if 'all' in [e.lower() for e in exts]:
            exts = [*self.bot.extensions]
        
        final_exts = [*exts]

        for ext in exts:
            
            if ext not in self.bot.extensions:
                log.info(f"Could not find extension {ext}, so it was not reloaded")
                final_exts[final_exts.index(ext)] = f"{ext} (not found)"
                continue

            self.bot.reload_extension(ext)
            log.info(f"Reloaded extension {ext}")
        
        log.info("Reload finished.")
        await msg.edit(content="The following extensions have been reloaded: ```%s```" % ('\n'.join(final_exts)))