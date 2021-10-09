import os
import random
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandOptionType
import configparser
import asyncio
import sys
sys.path.append('..')
from Lib import Logger, embed_generator, pluralize, perms

notification_channel = 738855014377848943
config = configparser.ConfigParser()

logger = Logger()
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
        self.channel = bot.get_channel(notification_channel)

        config.read('setting.ini')
        self.KGB_MODE = bool(config.get('Setting', 'kgb_mode'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await result_embed('Зашел на сервер!', choice_phrase(member, 'join'), self.channel)
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await result_embed('Вышел с сервера!', choice_phrase(member, 'leave'), self.channel)
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        await result_embed('Забанен!', choice_phrase(member, 'ban'), self.channel)
        self.logger.log(f'[Ban] Guild: {guild} User: {member}')

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        await result_embed('Разбанен!', choice_phrase(member, 'unban'), self.channel)
        self.logger.log(f'[Unban] Guild: {guild} User: {member}')

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
            config.set('Setting', 'kgb_mode', 'True')
            with open('setting.ini', 'w', encoding='utf-8') as configFile:
                config.write(configFile)
            config.read('setting.ini')
            self.KGB_MODE = config.get('Setting', 'kgb_mode')
            await ctx.send(embed=embed_generator('Успешно!', 'Режим доностчика активен!'))
        elif not state:
            config.set('Setting', 'kgb_mode', 'False')
            with open('setting.ini', 'w', encoding='utf-8') as configFile:
                config.write(configFile)
            config.read('setting.ini')
            self.KGB_MODE = config.get('Setting', 'kgb_mode')
            await ctx.send(embed=embed_generator('Успешно!', 'Режим доностчика деактивирован!'))

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
