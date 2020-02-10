import os

import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

name_song = None


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def check():
        for file in os.listdir('../'):
            if file.endswith('.mp3'):
                global name_song
                name_song = file
                print('Переименовыван файл: %s' % file)
                os.rename(file, 'song.mp3')

    @commands.command(aliases=['j'], description='Join voice channel', brief='Join in voice')
    @commands.has_permissions(connect=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        # if voice and voice.is_connected():
        #     #     await voice.move_to(channel)
        #     # else:
        #     #     voice = await channel.connect()
        #     #
        #     # await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()
            print('Joined in %s' % channel + ' at %s' % ctx.guild)

        await ctx.send('Joined at %s' % channel)

    @commands.command(aliases=['l'], description='Leave voice channel', brief='Leave voice')
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            print('Disconnected from %s' % channel + ' at %s' % ctx.guild)
            await ctx.send('Left from %s ' % channel)
        else:
            await ctx.send('Невозможно выполнить комманду "leave", т.к. бот не находится ни в каком голосовом канале')
            print('Error: Bot not in voice channel')

    @commands.command(aliases=['pl', 'start'],
                      description='This command initiates the playback of\n'
                                  'sound from url in the voice channel in \n'
                                  'which the bot is located.',
                      brief='Start playing audio in voice channel')
    async def play(self, ctx, url: str):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
                    print('Удален старый файл музыки')
            except PermissionError:
                print('Попытка удаления файла, но похоже он сейчас играет')
                await ctx.send('Error: Music playing')
                return

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '120',
                }],
            }

            await ctx.send('I am looking for audio on YouTube')
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    await ctx.send('Downloading audio from YouTube')
                    print('Скачивается аудио с YouTube')
            except Exception:
                os.system(
                    'youtube-dl ' + '"ytsearch:' + "'ytsearch:'%s" % url + '"' + ' --extract-audio --audio-format mp3')

            self.check()

            voice.play(discord.FFmpegPCMAudio('song.mp3'),
                       after=lambda e: print('%s закончил воиспроизведение' % name_song))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07

            nname = name_song.rsplit('-', 2)
            await ctx.send('Playing: %s' % nname[0])
            print('Воиспроизведение аудио стартовало!')
        else:
            await ctx.send('Go into the voice channel and enter the command "join"')
            print('Error:Бот не в голосовом канале')

    @commands.command(aliases=['p'], description='This command pauses and unpauses audio playback.',
                      brief='Pause/Unpause Audio')
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.pause()
            print('Пауза воиспроизведения')
            await ctx.send('Playing paused')
        else:
            voice.resume()
            await ctx.send('Resume playing')
            print('Продолжить воиспроизведение')

    @commands.command(aliases=['st', 's'], description='This command stops audio playback.',
                      brief='Stop audio')
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Stopped play audio')
            print('Аудио остановленно')
        else:
            await ctx.send('Audio already stoped')
            print('Ну как бы была попытка остановки, но чет пошло не так ...')

    @commands.command(aliases=['spot', 'spf'],
                      description='This command downloads and plays a track '
                                  'from the Spotify library in the voice channel',
                      brief='Audio from the Spotify')
    async def spotify(self, ctx, url: str):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            self.check()
            song_there = os.path.isfile('song.mp3')
            if song_there:
                try:
                    os.remove('song.mp3')
                    print('Удален трек с прошлого запуска')
                except PermissionError:
                    print('Не удалось удалить файл: нет прав или он занят')
                    await ctx.send('Error: Music playing')
                    return

            if voice and voice.is_connected():
                print("Скачиваю аудио из Spotify")
                await ctx.send('Downloading audio from Spotify')
                c_path = os.path.dirname(os.path.realpath(__file__))
                os.system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

                self.check()

                voice.play(discord.FFmpegPCMAudio('song.mp3'),
                           after=lambda e: print('%s закончил воиспроизведение' % name_song))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
        else:
            await ctx.send('Go into the voice channel and enter the command "join"')
            print('Error:Бот не в голосовом канале')


def setup(bot):
    bot.add_cog(Voice(bot))
