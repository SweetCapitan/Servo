import datetime
import discord
from discord import Option
from discord.commands import SlashCommandGroup, slash_command
from discord.ext import commands, pages
import os
from Utilities import logger
from Utilities.webhook import send_webhook
from Utilities.servomysql.servo_mysql import ServoMySQL
from Utilities.embeds import pluralize, ResultEmbeds

re = ResultEmbeds()
db = ServoMySQL()
text = '''        \                           /\n' \
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
       '        /                           \ \n'''


class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    server_ids = [530374773612478475]

    @slash_command(name='clear', description='Очистка сообщений', guild_ids=server_ids)
    async def clear(self, ctx,
                    num_messages: Option(int, min_value=1, max_value=200, description='кол-во сообщений для удаления'),
                    *user: Option(discord.User, description="укажите, чьи сообщения удалить", required=False)):
        if not ctx.author.guild_permissions.manage_messages:
            return ctx.respond("Прав не завезли!", ephemeral=True)
        chan = ctx.channel
        if not user:
            deleted = await chan.purge(limit=num_messages)
        elif user[0]:
            def check(msg):
                return msg.author == user[0]

            deleted = await chan.purge(limit=num_messages, check=check)
        logger.comm(f'CLEAR. Author: {ctx.author}')
        await ctx.respond(embed=re.done(f'Удалено {len(deleted)} сообщений.'))

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
