from ..blacklist import Blacklist


async def setup(bot):
    bot.add_cog(Blacklist(bot))
