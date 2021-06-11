import logging

import discord
from discord.ext import commands

import bot.config as conf

class _Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *args):

        embed = discord.Embed(color=discord.Color.green())
        
        if not args:

            embed.title = 'AMBOT'
            embed.description=f'Use `{conf.Bot.prefix}help <module>` to learn more about it.'
            cogs = ''

            for cog in self.bot.cogs:
                if cog.startswith('_'): continue
                cogs += f'`{cog}` {self.bot.cogs[cog].description}\n'
            
            embed.add_field(name='Modules', value=cogs, inline=False)
        
        if args:

            cog = self.bot.cogs.get(args[0])

            if cog:
                embed.title = args[0]
                embed.description = cog.description if cog.description else "No description"

                for command in cog.walk_commands():

                    parent_name = command.parent.name if command.parent else None

                    command_str = f'{conf.Bot.prefix}{" ".join(filter(None, (parent_name, command.name)))}'

                    if command.usage == None and not type(command) == commands.Group:
                        command.usage = " ".join((command_str, *[f"<{arg}>" for arg in command.clean_params]))

                    description_str = command.description if command.description else "No description"

                    usage_str = f'\nUsage:`{command.usage}`' if command.usage is not None else ""

                    aliases_str = f'\nAliases: `{", ".join(command.aliases)}`' if len(command.aliases) > 0 else ""

                    embed.add_field(name=f'{command_str}',
                                    value=f'{description_str}{usage_str}{aliases_str}',
                                    inline=False)
            else:

                embed.title = "No module found."

        await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(_Help(bot))
