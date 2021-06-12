import discord
from discord.ext import commands, tasks
from dislash import Button, auto_rows, ButtonStyle

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll.invoke_without_command = True

    @commands.group(aliases=["vote", "ask", "ballot"])
    async def poll(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), "Poll")

    @poll.command()
    async def create(self, ctx, prompt,  *options):
        
        poll_emb = discord.Embed(title=prompt)
        poll_emb.set_author(name=f"Poll created by {ctx.author}")
        poll_emb.set_footer(text="Poll closes 10 minutes after creation")

        option_components = []

        def pick_button_style(text):
            if text.lower() == "no":
                return ButtonStyle.red
            
        
        for option in options:
            option_components.append(Button(label=option, custom_id=f"ambot_poll_{ctx.author.id}_{options.index(option)}", style=ButtonStyle.blurple))

        msg = await ctx.send(embed=poll_emb, components = auto_rows(*option_components))

        on_option_click = msg.create_click_listener(timeout=600)

        @on_option_click.not_from_user(ctx.author)
        async def choose_option():
            pass

    @tasks.loop(minutes=5, count=1)
    async def end_poll(self,ctx):
        await self.end(self,ctx)

def setup(bot):
    bot.add_cog(Poll(bot))
