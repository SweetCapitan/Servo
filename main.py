import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import youtube_dl
import random
import requests
# from SERVO_BOT.CONFIG import BOT_TOKEN

bot = commands.Bot(command_prefix='?')

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

BTC_PRICE_URL_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'

rainbowrolename = os.environ.get('ROLE_RAINBOW')
server_id = os.environ.get('SERVER_ID')
RAINBOW_STATUS = os.environ.get('RAINBOW_STATUS')

def check():
    for file in os.listdir('../'):
        if file.endswith('.mp3'):
            global name
            name = file
            print('Переименовыван файл: %s' % file)
            os.rename(file, 'song.mp3')

def get_btc_price():
    r = requests.get(BTC_PRICE_URL_coinmarketcap)
    response_json = r.json()
    usd_price = response_json[0]['price_usd']
    rub_rpice = response_json[0]['price_rub']
    percent_change_1h = response_json[0]['percent_change_1h']
    percent_change_24h = response_json[0]['percent_change_24h']
    percent_change_7d = response_json[0]['percent_change_7d']
    return usd_price, rub_rpice, percent_change_1h, percent_change_24h, percent_change_7d

@bot.event
async def on_ready():
    print('Готово. Зашел под именами: %s'%bot.user.name)
    bot.loop.create_task(rainbow(rainbowrolename))

# TODO: Написать нормальный логгер сообщений, так и всех событий в целом.

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

@bot.command(pass_context=True,aliases=['btc'],
             description='This command sends you the current value of bitcoin in rubles and dollars.'
                         '\nЗачем боту эта функция ? А хуй ее знает ¯\_(ツ)_/¯'
                         '\n args: <7d,1d,1h,None>',
             brief='Bitcoin price')
async def btcprice(ctx,*args:str):
    btc_price_usd, btc_price_rub, percent1, percent24, percent7 = get_btc_price()
    btc_price_old = os.environ.get('BTC_PR_OLD').split(',')
    btc_price_changes_rub = int(float(btc_price_rub)) - int(float(btc_price_old[0]))
    btc_price_changes_usd = int(float(btc_price_usd)) - int(float(btc_price_old[1]))
    btc_price_changes = 'RUB: ' + str(btc_price_changes_rub) + ' | USD: ' + str(btc_price_changes_usd)
    embed = discord.Embed(title="BITCOIN price",
                          description="The cost of btc at the moment according to the coinmarketcap exchange.",
                          color=0xd5de21)
    embed.add_field(name="RUB", value=str(btc_price_rub).split('.')[0], inline=True)
    embed.add_field(name="USD", value=str(btc_price_usd).split('.')[0], inline=True)
    if not args:
        embed.add_field(name='Changes', value=btc_price_changes, inline=True)
        os.environ['BTC_PR_OLD'] = '%s,%s' % (btc_price_rub, btc_price_usd)
    elif args[0] == '7d':
        btc_price_changes_rub = ((int(float(btc_price_rub)) / 100) * int(float(percent7)))
        btc_price_changes_usd = ((int(float(btc_price_usd)) / 100) * int(float(percent7)))
        btc_price_changes = 'RUB : ' + str(btc_price_changes_rub) + ' | USD: ' + str(btc_price_changes_usd)
        embed.add_field(name='Changes in 7 days', value=btc_price_changes, inline=True)
    elif args[0] == '1d':
        btc_price_changes_rub = ((int(float(btc_price_rub)) / 100) * int(float(percent24)))
        btc_price_changes_usd = ((int(float(btc_price_usd)) / 100) * int(float(percent24)))
        btc_price_changes = 'RUB : ' + str(btc_price_changes_rub) + ' | USD: ' + str(btc_price_changes_usd)
        embed.add_field(name='Changes in 1 days', value=btc_price_changes, inline=True)
    elif args[0] == '1h':
        btc_price_changes_rub = ((int(float(btc_price_rub)) / 100) * int(float(percent1)))
        btc_price_changes_usd = ((int(float(btc_price_usd)) / 100) * int(float(percent1)))
        btc_price_changes = 'RUB : ' + str(btc_price_changes_rub) + ' | USD: ' + str(btc_price_changes_usd)
        embed.add_field(name='Changes in 1 hour', value=btc_price_changes, inline=True)

    await ctx.send(embed=embed)



async def rainbow(role):
    if bool(RAINBOW_STATUS):
        for role in bot.get_guild(int(server_id)).roles:
            if str(role) == str(rainbowrolename):
                print("Rainbow: Role detected")
                while not bot.is_closed():
                    try:
                        await role.edit(color=random.choice(colours))
                    except Exception as e:
                        print('Error: ' + e)
                    await asyncio.sleep(5)

bot.run(os.environ.get('BOT_TOKEN'))
# bot.run(BOT_TOKEN)