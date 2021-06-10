from ._tic_tac_toe import TicTacToe

def setup(bot):
    bot.add_cog(TicTacToe(bot))