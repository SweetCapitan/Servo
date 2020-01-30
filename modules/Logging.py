from discord.ext import commands
import sys
sys.path.append()
from Lib import Logger

notification_channel = 531622332859547668


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

def setup(bot):
    bot.add_cog(Logging(bot))