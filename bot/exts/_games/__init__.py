from ._tic_tac_toe import TicTacToe

__name__ = "Games"
__doc__ = "Fun games to play"

def setup(bot):
    bot.add_cog(TicTacToe(bot))