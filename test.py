from discord.ext import commands
from dislash import *

bot = commands.Bot(command_prefix="!")
slash = SlashClient(bot)

@bot.command()
async def test(ctx):
    row = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Click me!",
            custom_id="test_button"
        )
    )
    msg = await ctx.send("I have a button!", components=[row])
    def check(inter):
        return inter.author == ctx.author
    inter = await msg.wait_for_button_click(check=check)
    await inter.reply(f"Button: {inter.clicked_button.label}", type=7)

bot.run("ODUyMjYwNDE2NTgyNDUxMjcw.YMEPXQ.NpU-C75Hg781dQDuwkPerwE_MDE")