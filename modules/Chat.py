import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandOptionType
import os
import sys

sys.path.append('..')
from Lib import Logger, embed_generator, pluralize, perms

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

    @cog_ext.cog_slash(name='clear', description='Очистка сообщений',
                       permissions=perms,
                       options=[
                           create_option(
                               name='число_сообщений',
                               description='Введите число сообщений, которое хотите удалить',
                               option_type=SlashCommandOptionType.INTEGER,
                               required=True),
                           create_option(
                               name='пользователь',
                               description='Если хотите удалить сообщения определенного пользователя, укажите его',
                               option_type=6,
                               required=False)])
    async def clear(self, ctx: SlashContext, num_mes: int, *user: discord.User):
        chan = ctx.channel
        if not user:
            deleted = await chan.purge(limit=num_mes)
        elif user[0]:
            def check(msg):
                return msg.author == user[0]

            deleted = await chan.purge(limit=num_mes, check=check)

        await ctx.send(embed=embed_generator('Успешно!', f'Удалено {len(deleted)} сообщений.'))
        self.logger.comm(f'CLEAR. Author: {ctx.author}')

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
