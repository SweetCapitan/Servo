import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os
import youtube_dl
import random
import requests
import time
from contextlib import redirect_stdout
import io

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

start_time = time.time()


def check():
    for file in os.listdir('../'):
        if file.endswith('.mp3'):
            global name_song
            name_song = file
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
    print('Готово. Зашел под именами: %s' % bot.user.name)
    bot.loop.create_task(rainbow())
    bot.loop.create_task(status())


# TODO: Написать нормальный логгер сообщений, так и всех событий в целом.


@bot.command(pass_context=True, aliases=['j'], description='Join voice channel', brief='Join in voice')
async def join(ctx):
    print('Command: %s' % join)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
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


@bot.command(pass_context=True, aliases=['l'], description='Leave voice channel', brief='Leave voice')
async def leave(ctx):
    print('Command: %s' % leave)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print('Diconnected from %s' % channel + ' at %s' % ctx.guild)
        await ctx.send('Left %s ' % channel)
    else:
        await ctx.send('Невозможно выполнить комманду "leave" т.к. бот не находится не в каком голосовом канале')
        print('Error: Bot not in voice channel')


@bot.command(pass_context=True, aliases=['pl', 'start'],
             description='This command initiates the playback of\n'
                         'sound from url in the voice channel in \n'
                         'which the bot is located.',
             brief='СОЗДАТЕЛЯЭТОГОБЛЯДСКОГОAPIТОЛПАЧЕЧЕНОВЕБАЛАВЖОПУКОГДАОНПИСАЛЕГО')
async def play(ctx, url: str):
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
            os.system(
                'youtube-dl ' + '"ytsearch:' + "'ytsearch:'%s" % url + '"' + ' --extract-audio --audio-format mp3')

        check()

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


@bot.command(pass_context=True, aliases=['p'], description='This command pauses and unpauses audio playback.',
             brief='Pause/Unpause Audio')
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


@bot.command(pass_context=True, aliases=['st', 's'], description='This command stops audio playback.',
             brief='Stop audio')
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send('Stopped play audio')
        print('Аудио остановленно')
    else:
        await ctx.send('Audio already stoped')
        print('Ну как бы была попытка остановки, но чет пошло не так ...')


@bot.command(pass_context=True, aliases=['spot', 'spf'],
             description='This command downloads and plays a track from the Spotify library in the voice channel',
             brief='Audio from the Spotify')
async def spotify(ctx, url: str):
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
            await ctx.send('Downloading audio from Spotify')
            c_path = os.path.dirname(os.path.realpath(__file__))
            os.system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

            check()

            voice.play(discord.FFmpegPCMAudio('song.mp3'),
                       after=lambda e: print('%s закончил воиспроизведение' % name_song))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
    else:
        await ctx.send('Go into the voice channel and enter the command "join"')
        print('Error:Бот не в голосовом канале')


@bot.command(pass_context=True, aliases=['btc'],
             description='This command sends you the current value of bitcoin in rubles and dollars.'
                         '\nЗачем боту эта функция ? А хуй ее знает ¯\_(ツ)_/¯'
                         '\n args: <7d,1d,1h,None>',
             brief='Bitcoin price')
async def btcprice(ctx, *args: str):
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


# TODO: Переписать эту поебень нахуй, т.к. я не очень горю быть зависимым от чужого кода
# -----------------------------------------Start of IteratorW Code -----------------------------------------------------
class MyGlobals(dict):
    def __init__(self, globs, locs):
        super().__init__()
        self.globals = globs
        self.locals = locs

    def __getitem__(self, name):
        try:
            return self.locals[name]
        except KeyError:
            return self.globals[name]

    def __setitem__(self, name, value):
        self.globals[name] = value

    def __delitem__(self, name):
        del self.globals[name]


def _exec(code, g, l):
    out = io.StringIO()
    d = MyGlobals(g, l)
    try:
        error = False
        with redirect_stdout(out):
            exec(code, d)
    except Exception as ex:
        error = True
        out.write(str(ex))

    return out.getvalue(), error


def _await(coro):  # це костыль для выполнения асинхронных функций в exec
    asyncio.ensure_future(coro)


async def result_embed(result_state, description, message):
    embed = discord.Embed(title=result_state, description=description, color=0xd5de21)
    await message.send(embed=embed)


@bot.command(pass_context=True, aliases=['ex', 'exec'],
             description='This command allows you to execute python code directly from the chat itself.\n'
                         'P.s. Temporarily runs on Iteratorw code\n'
                         'Usage: execute ```code```',
             brief='Execute Python code :execute ```code```')
async def execute(ctx):
    code = ctx.message.content.split("```")
    if len(code) < 3:
        await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', 'Код где блять ?', ctx)
    out, is_error = _exec(code[1].strip().rstrip(), globals(), locals())

    if is_error:
        await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', out, ctx)

    else:
        await result_embed('Код успешно выполнен!', out, ctx)


# # --------------------------------------End of ITERATORW Code---------------------------------------------------------

emoji_react = ['<:jnJ6kEPEBQU:619899647669960714>', '<:image0:641676982651715584>',
               '<:emoji_6:615000140423626754>', '<:OREHUS_YES:666640633502498865>']


@bot.event
async def on_message(message):
    for emo in emoji_react:
        if emo.lower() in message.content.lower():
            emoji = emo
            await message.add_reaction(emoji)


@bot.event
async def on_reaction_add(reaction, _):
    for emo in emoji_react:
        if emo.lower() in str(reaction).lower():
            emoji = emo
            await reaction.message.add_reaction(emoji)


async def rainbow():
    if bool(RAINBOW_STATUS):
        for role in bot.get_guild(int(server_id)).roles:
            if str(role) == str(rainbowrolename):
                print("Rainbow: Role detected")
                while not bot.is_closed():
                    try:
                        await role.edit(color=random.choice(colours))
                    except Exception as e:
                        print('Error: ' + str(e))
                    await asyncio.sleep(5)


def get_uptime():
    t = round(time.time() - start_time)
    t_min = round((t - (t // 86400) * 86400 - ((t - (t // 86400) * 86400) // 3600) * 3600) // 60)
    t_sec = round(t - (t // 86400) * 86400 - ((t - (t // 86400) * 86400) // 3600) * 3600 - t_min * 60)
    t_hour = round((t - (t // 86400) * 86400) // 3600)
    t_day = round(t // 86400)
    return t_sec, t_min, t_hour, t_day


async def status():
    while not bot.is_closed():
        try:
            uptime_sec, uptime_min, uptime_hour, uptime_day = get_uptime()

            def pluralize(source, first, second, third):
                if int(str(source)[-1]) == 0:
                    return third
                elif int(str(source)[-2:]) in range(11, 21):
                    return third
                elif int(str(source)[-1]) == 1:
                    return first
                elif int(str(source)[-1]) in range(2, 5):
                    return second
                elif int(str(source)[-1]) in range(5, 10):
                    return third

            uptime_name = 'Без падений уже: %s {}, %s {}, %s {}, %s {}'.format(
                pluralize(uptime_day, 'день', 'дня', 'дней'),
                pluralize(uptime_hour, 'час', 'часа', 'часов'),
                pluralize(uptime_min, 'минуту', 'минуты', 'минут'),
                pluralize(uptime_sec, 'секунду', 'секунды', 'секунд')) % \
                          (uptime_day, uptime_hour, uptime_min, uptime_sec)

            await bot.change_presence(
                activity=discord.Streaming(name=uptime_name, url='https://www.twitch.tv/dancho67'))
        except Exception as e:
            print(e)
        await asyncio.sleep(5)


bot.run(os.environ.get('BOT_TOKEN'))
# bot.run(BOT_TOKEN)
