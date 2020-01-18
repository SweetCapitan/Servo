from discord.ext import commands


class Util(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'extensions.{extension}')
        self.bot.load_extension(f'extensions.{extension}')
        await ctx.send(f'Reloaded {extension}')

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'extensions.{extension}')
        await ctx.send(f'Loaded {extension}')


def setup(bot):
    bot.add_cog(Util(bot))
