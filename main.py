import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl

bot = commands.Bot(command_prefix='?')
'''
Когда-нибудь я удалю этот блок кода ...
'''
# @client.event
# async def on_ready():
#     print('{0.user.id} вошел в систему под именем {0.user}\n'.format(client,client))
#
# @client.event
# async def on_message(message):
#     print('Сообщение: {0.content} от {0.author}'.format(message))
#
# async def on_message(message):
#     if message.author == client.user:
#         if message.content.startwith('?play'):

@bot.event
async def on_ready():
    print('Готово. Зашел под именем: %s'%bot.user.name)

'''
Недо логер, которые ломает все к хуям. TODO: переписать это в адекватный логгер сообщений
'''
# @bot.event
# async def on_message(message):
#     print('Сообщение: {0.content} от {0.author}'.format(message))

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

    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print('Удален сарый файл музыки')
    except PermissionError:
        print('Попытка удаления файла, но похоже он сейчас играет')
        await ctx.send('Error: Music playing')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)

    await ctx.send('Downloading audio from YouTube')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '120',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Скачивается аудио с YouTube')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('Переименовыван файл: %s' % file)
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print('%s закончил воиспроизведение' % name))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit('-', 2)
    await ctx.send('Playing: %s' % nname[0])
    print('Воиспроизведение аудио стартовало!')


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


bot.run(os.environ.get('BOT_TOKEN'))
