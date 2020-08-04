import os
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
import sys
sys.path.append('..')
from Lib import Logger, result_embed, pluralize

name_song = None


class Voice(commands.Cog, name='Полностью переписанная версия Voice'):

    def __init__(self, bot):
        self.bot = bot

    voice = None
    voice_state = None
    voice_channel = None

    logger = Logger()

    def check_file(self):
        pass

    async def check_voice(self, context):
        self.voice_channel = context.message.author.voice.channel
        self.voice = get(self.bot.voice_clients, guild=context.guild)
        try:
            if self.voice and self.voice.is_connected():
                await self.voice.move_to(self.voice_channel)
                self.voice_state = True
            else:
                await self.voice_channel.connect()
                self.voice_state = True
        except Exception():
            context.send('Произошла непредвиденная ошибка: ```' + str(Exception) + '```')
            self.voice_state = False



    @commands.command(aliases=['j'],
                      description='По этой команде бот зайдет в голосовой канал, в котором вы находитесь',
                      brief='Зайти в голосовой чат')
    @commands.has_guild_permissions(speak=True)
    async def join(self, ctx):
        await self.check_voice(ctx)
        if self.voice_state:
            await result_embed('Успешно', 'Бот подключился к голосовому каналу `' + str(self.voice_channel) + '`', ctx)
            self.logger.comm(f'VOICE_JOIN. Author: {ctx.message.author}')


    @commands.command(aliases=['l'],
                      description='По этой команде бот зайдет в голосовой канал, в котором вы находитесь',
                      brief='Зайти в голосовой чат')
    @commands.has_guild_permissions(speak=True)
    async def leave(self, ctx):
        await self.check_voice(ctx)
        if self.voice_state:
            await self.voice.disconnect()
            await result_embed('Успешно', 'Бот покинул голосовой канал `' + str(self.voice_channel) + '`', ctx)
            self.voice_state = False
            self.voice = None
            self.logger.comm(f'VOICE_LEAVE. Author: {ctx.message.author}')
        else:
            await result_embed('Ошибка!', 'Братан, бот не в голосовом канале', ctx)





def setup(bot):
    bot.add_cog(Voice(bot))
