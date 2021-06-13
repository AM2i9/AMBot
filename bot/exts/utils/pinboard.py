import discord
from discord.ext import commands


class Pinboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, message: discord.Message = None):
            
        if not message and ctx.message.reference:
            message = await commands.MessageConverter().convert(ctx, str(ctx.message.reference.message_id)) 
        elif not message and not ctx.message.reference:
            await ctx.reply("Please reference a message or include a message id or link in the command.")
            return

        if ctx.guild:
            pinboard = discord.utils.get(ctx.guild.channels, name="pinboard")
            if not pinboard:
                pinboard = await ctx.guild.create_text_channel("pinboard")

        with pinboard.typing():
            webhook = discord.utils.get(await pinboard.webhooks(), name="AMBOT")
            if not webhook:
                webhook = await pinboard.create_webhook(name="AMBOT", reason="Pin message")
            
            view_link = discord.Embed(title="View Original Message", url=message.jump_url)

            attachments = []
            for att in message.attachments:
                attachments.append(att.url)

            await webhook.send(content=message.content + "\n\n{}".format('\n'.join(attachments)) ,
                                embeds=(*message.embeds, view_link),
                                username=message.author.name,
                                avatar_url=message.author.avatar_url)

def setup(bot):
    bot.add_cog(Pinboard(bot))
