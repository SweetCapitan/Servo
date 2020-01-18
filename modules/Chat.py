import discord
from discord.ext import commands
import datetime
from .main import result_embed, pluralize


# async def result_embed(result_state, description, message):
#     embed = discord.Embed(title=result_state, description=description, color=0xd5de21)
#     await message.send(embed=embed)
#
#
# def pluralize(source, first, second, third):
#     if int(str(source)[-1]) == 0:
#         return third
#     elif int(str(source)[-2:]) in range(11, 21):
#         return third
#     elif int(str(source)[-1]) == 1:
#         return first
#     elif int(str(source)[-1]) in range(2, 5):
#         return second
#     elif int(str(source)[-1]) in range(5, 10):
#         return third


class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cl'],
                      description='This command allows you to delete messages '
                                  'from the channel in which the command was called.\n'
                                  '- Usual variant -\n'
                                  'This option allows to delete n messages. If a user is mentioned at the end,'
                                  'then ONLY messages of the specified user will be deleted.'
                                  ' Example: clear <Messages to search. This is not the number of messages !>'
                                  '<(optional)@ User whose messages you want to delete>.\n'
                                  '- Delete by date and time - \n'
                                  'This option allows you to delete all messages from the channel starting '
                                  'from the specified date and time. If you specify a user at the end,'
                                  ' they will delete ONLY past posts of the user '
                                  'Example: clear <(UTC TIME!)[hour] [min] [sec] [day] [mount] [year]> '
                                  '<(Optional)@User whose posts you want to delete>.',
                      brief='Delete N- number of messages from the channel.')
    async def clear(self, ctx, *args):
        chan = ctx.message.channel
        if len(args) == 7:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(check=check,
                                       after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                                               int(args[0]),int(args[1]), int(args[2])))
        elif len(args) == 6:
            deleted = await chan.purge(
                after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                        int(args[0]), int(args[1]),int(args[2])))
        elif len(args) == 2:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(limit=int(args[0]), check=check)
        else:
            deleted = await chan.purge(limit=int(args[0]))

        # await chan.send('Удалено %s {}'.format(pluralize(len(deleted),
        #                                                  'сообщение', 'сообщения', 'сообщений')) % len(deleted))
        await result_embed('Успешно!', 'Удалено %s {}'
                                .format(pluralize(len(deleted), 'сообщение', 'сообщения', 'сообщений')) % len(
            deleted), ctx)

    emoji_react = ['<:jnJ6kEPEBQU:619899647669960714>', '<:image0:641676982651715584>',
                   '<:emoji_6:615000140423626754>', '<:OREHUS_YES:666640633502498865>']

    @commands.Cog.listener()
    async def on_message(self,message):
        for emo in self.emoji_react:
            if emo.lower() in message.content.lower():
                emoji = emo
                await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, _):
        for emo in self.emoji_react:
            if emo.lower() in str(reaction).lower():
                emoji = emo
                await reaction.message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Chat(bot))
