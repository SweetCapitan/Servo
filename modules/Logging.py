from discord.ext import commands
from ..main import Logger

logger = Logger()

notification_channel = 531622332859547668


class Logging(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} присоеденился к нам. Земля ему говном.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(notification_channel)
        await channel.send(f'{member} покинул нас. Земля ему говном.')

def setup(bot):
    bot.add_cog(Logging(bot))