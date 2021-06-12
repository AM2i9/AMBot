
def setup(bot):
    from ._cog import Poll
    bot.add_cog(Poll(bot))