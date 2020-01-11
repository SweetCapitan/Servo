import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import youtube_dl
import random
import time
from SERVO_BOT.CONFIG import BOT_TOKEN, ROLE_RAINBOW, SERVER_ID, RAINBOW_STATUS

rainbowrolename = ROLE_RAINBOW
server_id = SERVER_ID

colours = [discord.Color.dark_orange(),
           discord.Color.orange(),
           discord.Color.dark_gold(),
           discord.Color.gold(),
           discord.Color.dark_magenta(),
           discord.Color.magenta(),
           discord.Color.red(),
           discord.Color.dark_red(),
           discord.Color.blue(),
           discord.Color.dark_blue(),
           discord.Color.teal(),
           discord.Color.dark_teal(),
           discord.Color.green(),
           discord.Color.dark_green(),
           discord.Color.purple(),
           discord.Color.dark_purple()]

bot = commands.Bot(command_prefix='?')
def check():
    for file in os.listdir('../'):
        if file.endswith('.mp3'):
            global name
            name = file
            print('Переименовыван файл: %s' % file)
            os.rename(file, 'song.mp3')

@bot.event
async def on_ready():
    print('Готово. Зашел под именами: %s'%bot.user.name)
    bot.loop.create_task(rainbow(rainbowrolename))


@bot.event
async def on_message(message):
    mes = message.content
    aut = message.author
    chan = message.channel
    gld = message.guild
    log = ('%s | Message From Server: %s | In the channel : %s | Content : "%s" | From : %s'%(time.ctime(),gld,chan,mes,aut))
    print(log)
    with open('logs.txt','a',encoding='utf-8') as l:
        l.write(str(log)+'\n')

    await bot.process_commands(message)

@bot.command(pass_context=True,aliases=['j'],description='Join voice channel',brief='Join in voice')
async def join(ctx):
    global voice
    print('Command: %s' % join)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients,guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print('Joined in %s'%(channel)+' at %s'%(ctx.guild))

    await ctx.send('Joined at %s'% channel)

@bot.command(pass_context=True,aliases=['l'],description='Leave voice channel',brief='Leave voice')
async def leave(ctx):
    print('Command: %s'% leave)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print('Diconnected from %s'%channel+' at %s'%ctx.guild)
        await ctx.send('Left %s ' % channel)
    else:
        await ctx.send('Невозможно выполнить комманду "leave" т.к. бот не находится не в каком голосовом канале')
        print('Error: Bot not in voice channel')



@bot.command(pass_context=True,aliases=['pl','start'],
             description='This command initiates the playback of\n sound from url in the voice channel in \nwhich the bot is located.',
             brief='СОЗДАТЕЛЯЭТОГОБЛЯДСКОГОAPIТОЛПАЧЕЧЕНОВЕБАЛАВЖОПУКОГДАОНПИСАЛЕГО')
async def play(ctx, url:str):
    voice = get(bot.voice_clients, guild=ctx.guild)
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

        except:
            c_path = os.path.dirname(os.path.realpath(__file__))
            os.system('youtube-dl ' + '"ytsearch:' + "'ytsearch:'%s" % (url) + '"' + ' --extract-audio --audio-format mp3')

        check()

        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('%s закончил воиспроизведение' % name))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit('-', 2)
        await ctx.send('Playing: %s' % nname[0])
        print('Воиспроизведение аудио стартовало!')
    else:
        await ctx.send('Go into the voice channel and enter the command "join"')
        print('Error:Бот не в голосовом канале')



@bot.command(pass_context=True,aliases=['p'],description='This command pauses and unpauses audio playback.',brief='Pause/Unpause Audio')
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        print('Пауза воиспроизведения')
        await ctx.send('Playing paused')
    else:
        voice.resume()
        await ctx.send('Resume playing')
        print('Продолжить воиспроизведение')

@bot.command(pass_context=True,aliases=['st','s'],description='This command stops audio playback.',brief='Stop audio')
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Stopped play audio')
        print('Аудио остановленно')
    else:
        await ctx.send('Audio already stoped')
        print('Ну как бы была попытка остановки, но чет пошло не так ...')

@bot.command(pass_context=True,aliases=['spot','spf'],description='This command downloads and plays a track from the Spotify library in the voice channel',brief='Audio from the Spotify')
async def spotify(ctx,url:str):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        check()
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                print('Удален сарый файл музыки')
        except PermissionError:
            print('Попытка удаления файла, но похоже он сейчас играет')
            await ctx.send('Error: Music playing')
            return

        if voice and voice.is_connected():
            print("Скачиваю аудио из Spotify")
            await ctx.send('Download audio of Spotify')
            c_path = os.path.dirname(os.path.realpath(__file__))
            os.system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

            check()

            voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('%s закончил воиспроизведение' % name))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
    else:
        await ctx.send('Go into the voice channel and enter the command "join"')
        print('Error:Бот не в голосовом канале')

async def rainbow(role):
    if RAINBOW_STATUS:
        for role in bot.get_guild(int(server_id)).roles:
            if str(role) == str(rainbowrolename):
                print("Rainbow: Role detected")
                while not bot.is_closed():
                    try:
                        await role.edit(color=random.choice(colours))
                    except Exception as e:
                        print('Error: ' + e)
                    await asyncio.sleep(5)

bot.run(BOT_TOKEN)