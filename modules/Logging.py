import os
from discord.ext import commands
import sys
sys.path.append('..')
from Lib import Logger, result_embed, pluralize

notification_channel = 531622332859547668
KGB_MODE = bool(os.environ.get('KGB_MODE'))

class Logging(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    logger = Logger()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} присоеденился к нам. Земля ему говном.')
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} покинул нас. Земля ему говном.')
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_ban(self,guild,member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} получил Банхаммером по лицу. Земля ему говном.')
        self.logger.log(f'[Ban] Guild: {guild} User: {member}')

    @commands.Cog.listener()
    async def on_member_unban(self,guild,member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} получил помилование. Земля ему говном.')
        self.logger.log(f'[Unban] Guild: {guild} User: {member}')

    @commands.command()
    async def kgb(self, ctx, state):
        if state.lower() == 'true' or state.lower() == 'on':
            os.environ['KGB_MODE'] = 'True'
            await ctx.send('Включен режим слежки')
        elif state.lower() == 'false' or state.lower() == 'off':
            os.environ['KGB_MODE'] = 'False'
            await ctx.send('Выключен режим слежки')

    if KGB_MODE:
        @commands.Cog.listener()
        async def on_message_delete(self, message):
            self.logger.log(f'[Deleted Message] Text: {message.content} Author: {message.author}')

        @commands.Cog.listener()
        async def on_message_edit(self,before,after):
            self.logger.log(f'[Edited Message] Before: {before.content} After: {after.content} Author: {before.author}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        await ctx.send(f'{ctx.message.author.mention} {ex}')

def setup(bot):
    bot.add_cog(Logging(bot))