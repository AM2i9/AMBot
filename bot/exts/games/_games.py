import discord
from discord.ext import commands
from dislash import *
from ._tic_tac_toe import TicTacToe

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games.invoke_without_command = True

        self.description = "Games"

    @commands.group(name="games", description="Base Games command. Will show this message.")
    async def games(self, ctx):
        self.bot.invoke_help(ctx, "Games")

    @games.command(aliases=['ttt','tic-tac-toe'], description = "A game of Tic-Tac-Toe")
    async def tictactoe(self, ctx, user: discord.Member = None):
        await TicTacToe(self.bot).run_game(ctx, user)