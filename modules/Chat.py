import datetime
import discord
from discord.ext import commands
import os
<<<<<<< HEAD
from Utilities import logger
from Utilities.embeds import pluralize, ResultEmbeds
from Utilities.webhook import send_webhook
from Utilities.perms import perms
from Utilities.servomysql.servo_mysql import ServoMySQL
=======
from Utilities.embeds import pluralize, perms, ResultEmbeds
import Utilities.logger as logger
from Utilities.servomysql.mysql import ServoMySQL
>>>>>>> 084e3eb ([Update] Many small updates code to work with db and new functions)

re = ResultEmbeds()
db = ServoMySQL()
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

    server_ids = [int(os.environ.get('SERVER_ID'))]

    @cog_ext.cog_slash(name='clear', description='Очистка сообщений',
                       permissions=perms,
                       options=[
                           create_option(
                               name='num_messages',
                               description='Введите число сообщений, которое хотите удалить',
                               option_type=SlashCommandOptionType.INTEGER,
                               required=True),
                           create_option(
                               name='user',
                               description='Если хотите удалить сообщения определенного пользователя, укажите его',
                               option_type=SlashCommandOptionType.USER,
                               required=False)],
                       guild_ids=server_ids)
    async def clear(self, ctx: SlashContext, num_messages: int, *user: discord.User):
        chan = ctx.channel
        if not user:
            deleted = await chan.purge(limit=num_messages)
        elif user[0]:
            def check(msg):
                return msg.author == user[0]

            deleted = await chan.purge(limit=num_messages, check=check)
        await ctx.send(embed=re.done(f'Удалено {len(deleted)} сообщений.'))
        logger.comm(f'CLEAR. Author: {ctx.author}')

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
