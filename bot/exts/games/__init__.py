from ._games import Games

def setup(bot):
    bot.add_cog(Games(bot))