import discord
from discord.ext import commands
from dislash import *
from ._tic_tac_toe import TicTacToe

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games.invoke_without_command = True

    @commands.group(name="games", description="Fun Games")
    async def games(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), "Games")

    @games.command(aliases=['ttt','tic-tac-toe'], description = "Tic-Tac-Toe")
    async def tictactoe(self, ctx, user: discord.Member = None):
        await TicTacToe(self.bot).run_game(ctx, user)