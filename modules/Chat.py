import datetime
from discord.ext import commands
import os
import sys

sys.path.append('..')
from Lib import Logger, result_embed, pluralize

text = '        \                           /\n' \
       '         \                         /\n' \
       '          \ Видимо кого-то послали/\n' \
       '           ]   на 3 буквы ...    [    ,"|\n' \
       '           ]                     [   /  |\n' \
       '           ]___               ___[ ,"   |\n' \
       '           ]  ]\    нахуй    /[  [ |:   |\n' \
       '           ]  ] \     ||    / [  [ |:   |\n' \
       '           ]  ]  ]    ||   [  [  [ |:   |\n' \
       '           ]  ]  ]__  \/   __[  [  [ |:   |\n' \
       '           ]  ]  ] ]\ _ /[ [  [  [ |:   |\n' \
       '           ]  ]  ] ] (Ты)[ [  [  [ :===="\n' \
       '           ]  ]  ]_].nHn.[_[  [  [\n' \
       '           ]  ]  ]  HHHHH. [  [  [\n' \
       '           ]  ] /   `HH("N  \ [  [\n' \
       '           ]__]/     HHH  "  \[__[\n' \
       '           ]         NNN         [\n' \
       '           ]         N/"         [\n' \
       '           ]         N H         [\n' \
       '          /          N            \ \n' \
       '         /           q,            \ \n' \
       '        /                           \ \n'


class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    logger = Logger()

    @commands.command(aliases=['cl', 'purge'],
                      description='Эта команда позволяет удалять сообщения из канала, в котором была вызвана команда.',
                      brief='Удалить сообщения из канала.',
                      help='- Удаление сообщений указанного пользователя -\n'
                           'Эта опция позволяет удалить n сообщений. Если пользователь упоминается в конце,'
                           'тогда будут удалены ТОЛЬКО сообщения указанного пользователя.',
                      usage='<(UTC TIME!)[hour] [min] [sec] [day] [mount] [year]>\n'
                            f'clear <(UTC TIME!)[hour] [min] [sec] [day] [mount] [year]> @Somebody\n'
                            f'clear 10\n'
                            f'clear 10 @Somebody')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *args):
        if not args:
            await result_embed('ОшибОЧКА!', 'Укажите аргументы и повторите попытку.', ctx)
            return
        chan = ctx.message.channel
        await ctx.message.delete()
        if len(args) == 7:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(check=check,
                                       after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                                               int(args[0]), int(args[1]), int(args[2])))
        elif len(args) == 6:
            deleted = await chan.purge(
                after=datetime.datetime(int(args[5]), int(args[4]), int(args[3]),
                                        int(args[0]), int(args[1]), int(args[2])))
        elif len(args) == 2:
            def check(msg):
                return msg.author == ctx.message.mentions[0]

            deleted = await chan.purge(limit=int(args[0]), check=check)
        else:
            deleted = await chan.purge(limit=int(args[0]))

        # await chan.send('Удалено %s {}'.format(pluralize(len(deleted),
        #                                                  'сообщение', 'сообщения', 'сообщений')) % len(deleted))
        await result_embed('Успешно!', 'Удалено %s {}'
                           .format(pluralize(len(deleted), 'сообщение', 'сообщения', 'сообщений')) % len(deleted), ctx)
        self.logger.comm(f'CLEAR. Author: {ctx.message.author}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == 'пошел нахуй' or message.content.lower() == 'нахуй пошел':
            await message.channel.send(f'```{text}```')
            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, _):
        users = await reaction.users().flatten()
        if len(users) > 1:
            await reaction.message.add_reaction(reaction.emoji)


def setup(bot):
    bot.add_cog(Chat(bot))
