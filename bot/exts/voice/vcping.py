import discord
import discord.utils
from discord.ext import commands

COG_DESCRIPTION = "Voice channel roles."
class VCPing(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.description = COG_DESCRIPTION

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):

        if after.channel != None:
            role = discord.utils.get(member.guild.roles,name=after.channel.name)
            if not role:
                role = await member.guild.create_role(name=after.channel.name)
            await member.add_roles(role)
        if before.channel != None:
            channel_name = before.channel.name
            role = discord.utils.get(member.guild.roles,name=channel_name)
            if role: await member.remove_roles(role)

def setup(bot):
    bot.add_cog(VCPing(bot))
