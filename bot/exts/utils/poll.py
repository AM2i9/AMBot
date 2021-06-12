import discord
from discord.ext import commands

import dateparser
import datetime

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll.invoke_without_command = True

    @commands.group(aliases=["vote", "ask", "ballot"])
    async def poll(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), "Poll")

    @poll.command()
    async def create(self, ctx, prompt, expiration, *options):

        expiration_date = dateparser.parse(expiration)

        # We can't do TIME TRAVEL?!?!?
        if expiration_date < datetime.datetime.now():
            expiration_date = "... What? Really though you could do time travel, did ya?"
        else:
            expiration_date = expiration_date.strftime('%c')
        
        poll_emb = discord.Embed(title=prompt)
        poll_emb.set_author(name=f"Poll created by {ctx.author}")

        if expiration_date:
            poll_emb.set_footer(text=f"Poll ends on {expiration_date}")
        
        for option in options:
            print(option)
            poll_emb.add_field(name=option, value="percent", inline=False)

        await ctx.send(embed=poll_emb)
        
    async def end(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Poll(bot))
