from discord.ext import commands


class Util(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TODO:ПОФИКСИ МЕНЯ БЛЯТЬ
    @commands.command()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'modules.{extension}')
        self.bot.load_extension(f'modules.{extension}')
        await ctx.send(f'Reloaded {extension}')

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'modules.{extension}')
        await ctx.send(f'Loaded {extension}')


def setup(bot):
    bot.add_cog(Util(bot))
