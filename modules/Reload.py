from discord.ext import commands
import sys
sys.path.append()
from Lib import Logger

class Util(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    logger = Logger()

    @commands.command()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'modules.{extension}')
        self.bot.load_extension(f'modules.{extension}')
        await ctx.send(f'Reloaded {extension}')
        self.logger.comm(f'RELOAD module: {extension}. Author: {ctx.message.author}')

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'modules.{extension}')
        await ctx.send(f'Loaded {extension}')
        self.logger.comm(f'LOAD module: {extension}. Author: {ctx.message.author}')


def setup(bot):
    bot.add_cog(Util(bot))
