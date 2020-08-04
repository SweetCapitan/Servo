import os
import shutil

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
        try:
            await self.check_voice(ctx)
            if self.voice_state:
                await result_embed('Успешно', 'Бот подключился к голосовому каналу `' + str(self.voice_channel) + '`',
                                   ctx)
                self.logger.comm(f'VOICE_JOIN. Author: {ctx.message.author}')
        except Exception:
            list_voice_channels = ''
            for e in ctx.guild.voice_channels:
                list_voice_channels += str(e) + ', '
            await result_embed('Ашыбка!',
                               ctx.message.author.mention + ' вы не находитесь в голосовом канале, '
                                                         'пожалуйста зайдите на один из каналов ``' +
                               list_voice_channels + '``',
                               ctx)

    @commands.command(aliases=['l'],
                      description='По этой команде бот выйдет из голосового канала, в котором вы находитесь',
                      brief='Выйти из голосового чата')
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

    queues = {}

    @commands.command(aliases=['pl'],
                      description='По этой команде бот начнет воипроизводить аудио файл, который он скачает по вашему '
                                  'запросу, из ютуба',
                      brief='Начать воиспроизведение аудио')
    @commands.has_guild_permissions(speak=True)
    async def play(self, ctx, url):

        Guild_Queue_folder = 'Queue_' + str(ctx.guild.id)

        def check_queue():
            Queue_infile = os.path.isdir("./Songs/" + Guild_Queue_folder)
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Songs/" + Guild_Queue_folder))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued song(s)\n")
                    self.queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Songs/" + Guild_Queue_folder) + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next queued\n")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
                    self.voice.source.volume = 0.07

                else:
                    self.queues.clear()
                    return

            else:
                self.queues.clear()
                print("No songs were queued before the ending of the last song\n")
        await self.check_voice(ctx)
        if self.voice.is_playing():
            await result_embed('Ошибка', 'Бот уже воиспроизводит музыку')
        elif self.voice_state:
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
                    self.queues.clear()
                    self.logger.log('Удален старый аудиофайл.')
            except PermissionError:
                self.logger.error('Неудачная попытка удаления аудиофайла, ошибка прав!')
                return

        Queue_infile = os.path.isdir("./Songs/" + Guild_Queue_folder)
        try:
            Queue_folder = "./Songs/" + Guild_Queue_folder
            if Queue_infile is True:
                print("Removed old Queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")

        await ctx.send("Getting everything ready now")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
            c_path = '.Songs/' + Guild_Queue_folder
            os.system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

        for file in os.listdir('.Songs/' + Guild_Queue_folder):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        self.voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("playing\n")

    @commands.command(aliases=['q', 'que'],
                      description='ОЧЕРЕДЬ',
                      brief='ОЧЕРЕДЬ')
    @commands.has_guild_permissions(speak=True)
    async def queue(self, ctx, url):

        Guild_Queue_folder = 'Queue_' + str(ctx.guild.id)

        Queue_infile = os.path.isdir("./Songs" + Guild_Queue_folder)
        if Queue_infile is False:
            os.mkdir("Songs/" + Guild_Queue_folder)
        DIR = os.path.abspath(os.path.realpath("Songs/" + Guild_Queue_folder))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in self.queues:
                q_num += 1
            else:
                add_queue = False
                self.queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Songs/" + Guild_Queue_folder) + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
            q_path = os.path.abspath(os.path.realpath("Songs/" + Guild_Queue_folder))
            os.system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

        await ctx.send("Adding song " + str(q_num) + " to the queue")

        print("Song added to queue\n")

def setup(bot):
    bot.add_cog(Voice(bot))
