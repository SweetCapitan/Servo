import os
import random
import discord
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandOptionType
import configparser
import asyncio
from Utilities import logger
from Utilities.embeds import pluralize, ResultEmbeds
from Utilities.perms import perms
from Utilities.servomysql.mysql import ServoMySQL

notification_channel = 738855014377848943
re = ResultEmbeds()
db = ServoMySQL()
server_ids = [int(os.environ.get('SERVER_ID'))]


def choice_phrase(member: str, event: str):
    phrases = {
        'join': [
            f'{member} присоеденился к нам. Земля ему говном.',
            f'{member} присоеденился, чтобы рвать жопы и есть мороженное. Как видите мороженное он уже доел ...',
            f'Дружок пирожок {member}, клуб кожевного ремесла на два этажа ниже',
            f'Злой дух по имени {member} вторгся к вам'
        ],
        'leave': [
            f'{member} слился - слабак!',
            f'{member} ушел, но обещал вернуться!',
            f'{member} наелся и спит.\n {member} умер.'
        ],
        'ban': [
            f'Ой ой ой, ну ты даешь {member}. Пойди ка погуляй.',
            f'Либераху порвало. В гулаг тебя {member}.',
            f'{member} вы напугали деда, получай Банхаммером по лицу.',
            f'{member} наказан, гулять он не выйдет.'
        ],
        'unban': [
            f'{member} хорошо себя вел. Он получил помилование.',
            f'{member} ну хорошо. На этот раз я тебя прощаю.',
            f'{member}, а у тебя хорошая попка. На этот раз мы закроем глаза на твои проступки'
        ]
    }
    return random.choice(phrases[event])


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel: discord.TextChannel = bot.get_channel(notification_channel)
        self.KGB_MODE = db.get_setting('kgb_mode', boolean=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.channel.send(embed=re.embed('Зашел на сервер!', choice_phrase(member, 'join')))
        logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.channel.send(embed=re.embed('Вышел с сервера!', choice_phrase(member, 'leave')))
        logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        await self.channel.send(embed=re.embed('Забанен!', choice_phrase(member, 'ban')))
        logger.log(f'[Ban] Guild: {guild} User: {member}')

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        await self.channel.send(embed=re.embed('Разбанен!', choice_phrase(member, 'unban')))
        logger.log(f'[Unban] Guild: {guild} User: {member}')

    @cog_ext.cog_slash(name='KGB', description='Переключение режима прослушки удаленных/измененных сообщений.',
                       permissions=perms,
                       options=[create_option(
                           name='режим',
                           description='Переключить режим',
                           option_type=SlashCommandOptionType.BOOLEAN,
                           required=True
                       )], guild_ids=server_ids)
    async def kgb(self, ctx: SlashContext, state: bool):
        if state:
            db.update_setting('kgb_mode', True)
            self.KGB_MODE = db.get_setting('kgb_mode')
            await ctx.send(embed=re.done('Режим доностчика активен!'))
        elif not state:
            db.update_setting('kgb_mode', 'False')
            self.KGB_MODE = db.get_setting('kgb_mode')
            await ctx.send(embed=re.done('Режим доностчика деактивирован!'))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.KGB_MODE == 'True':
            await message.channel.send(f'[Deleted Message] Text: {message.content} Author: {message.author}')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.KGB_MODE == 'True':
            await before.channel.send(
                f'[Edited Message] Before: {before.content} After: {after.content} Author: {before.author}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        await ctx.send(f'{ctx.message.author.mention} {ex}')

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, ex):
        logger.error(f'[Slash] {ex}\n{ctx}')


def setup(bot):
    bot.add_cog(Logging(bot))
