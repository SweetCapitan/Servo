import sys
# import cyrtranslit
import os
import discord
import requests
from discord.ext import commands
sys.path.append('..')
from Lib import Logger, pluralize

BRIDGE_URL = os.environ.get('BRIDGE_URL')


class Bridge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    logger = Logger()

    @commands.command(usage='Использование', description='Описание', brief='Название', help='Помощь')
    @commands.has_permissions(administrator=True)
    async def m(self, ctx):
        member_name = ctx.message.guild.get_member(ctx.message.author.id).nick
        data = {'message': (f'{member_name}: {cyrtranslit.to_latin(ctx.message.content[3:])}', 'ru')}
        # print(data)
        requests.put(BRIDGE_URL, data=data)


def setup(bot):
    bot.add_cog(Bridge(bot))
