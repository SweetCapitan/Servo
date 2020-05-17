import asyncio
import os
import time
import discord
from discord.ext import commands
from colorsys import hls_to_rgb
from discord import Embed
import sys
import psycopg2

sys.path.append('..')
from Lib import Logger, result_embed, pluralize

logger = Logger()

DATABASE_URL = os.environ['DATABASE_URL']
rainbow_role_name = os.environ.get('ROLE_RAINBOW')

start_time = time.time()
# start_time = int(os.environ.get('TIME'))
# response_time = int(os.environ.get('RESPONSE_TIME'))

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# with conn:
#     with conn.cursor() as cur:
#         cur.execute("CREATE TABLE covidtime (time INT)")

with conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO covidtime (time) VALUES (%s)" % '1589684400')
        cur.execute("SELECT time FROM covidtime")
        response_time = cur.fetchone()

class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.status())
        bot.loop.create_task(self.virus())
        # Some Shit
        server_list = self.bot.guilds
        servers = list()
        for server in server_list:
            servers.append(server.id)
        i = 0
        while i < len(servers):
            self.bot.loop.create_task(self.rainbow(servers[i]))
            # asyncio.run_coroutine_threadsafe(self.rainbow_change, self.bot.loop)
            i += 1

    @staticmethod
    def check_status(guild):
        env_val = os.environ
        for _RNB_STAT in env_val:
            if _RNB_STAT == str(guild) + '_RAINBOW_STATUS':
                RAINBOW_STATUS = os.environ.get(_RNB_STAT)
                if RAINBOW_STATUS == 'True':
                    return True
                if RAINBOW_STATUS == 'False':
                    return False
        return False

    async def rainbow(self, server_id):
        hue = 0
        while True:
            while self.check_status(server_id):
                for role in self.bot.get_guild(int(server_id)).roles:
                    if str(role) == str('Rainbow'):
                        hue = (hue + 7) % 360
                        rgb = [int(x * 255) for x in hls_to_rgb(hue / 360, 0.5, 1)]
                        clr = discord.Color(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
                        try:
                            await role.edit(color=clr)
                        except Exception as e:
                            logger.error('ERROR: ' + str(e))
                        await asyncio.sleep(5)
            await asyncio.sleep(5)

    @staticmethod
    def get_uptime():
        t = round(time.time() - start_time)
        t_min = round((t - (t // 86400) * 86400 - ((t - (t // 86400) * 86400) // 3600) * 3600) // 60)
        t_sec = round(t - (t // 86400) * 86400 - ((t - (t // 86400) * 86400) // 3600) * 3600 - t_min * 60)
        t_hour = round((t - (t // 86400) * 86400) // 3600)
        t_day = round(t // 86400)
        return t_sec, t_min, t_hour, t_day

    async def status(self):
        while not self.bot.is_closed():
            try:
                uptime_sec, uptime_min, uptime_hour, uptime_day = self.get_uptime()
                uptime_name = 'Без падений уже: %s {}, %s {}, %s {}, %s {}'.format(
                    pluralize(uptime_day, 'день', 'дня', 'дней'),
                    pluralize(uptime_hour, 'час', 'часа', 'часов'),
                    pluralize(uptime_min, 'минуту', 'минуты', 'минут'),
                    pluralize(uptime_sec, 'секунду', 'секунды', 'секунд')
                ) % (uptime_day, uptime_hour, uptime_min, uptime_sec)

                await self.bot.change_presence(
                    activity=discord.Streaming(name=uptime_name, url='https://www.twitch.tv/dancho67'))
            except Exception as e:
                print(e)
            await asyncio.sleep(5)

    async def virus(self, response_time=response_time):
        from bs4 import BeautifulSoup
        import requests
        resp = requests.get('https://www.interfax.ru/chronicle/novyj-koronavirus-v-kitae.html')
        result = BeautifulSoup(resp.text, 'html.parser')
        info = result.findAll('span', {'class': 'c19_statistic_num'})
        world = f'Случаев SARS2-COV в Мире: {info[3].getText().split("+")[0]} \n' \
                f'+{info[3].getText().split("+")[1]} за текущие сутки,' \
                f'Из них везучие бастарды: {info[4].getText()}, ded inside-ов: {info[5].getText()}'
        russia = f'Случаев SARS2-COV в России: {info[0].getText().split("+")[0]} +{info[0].getText().split("+")[1]} ' \
                 f'новых за сутки. \n' \
                 f'Из них везучие бастарды: {info[1].getText()}, ded inside-ов: {info[2].getText()}\n' \
                 f'Статистику по каждому городу можно посмотреть тут -> ' \
                 f'https://www.interfax.ru/chronicle/novyj-koronavirus-v-kitae.html#map'
        embed = Embed(title='Статистика по SARS2-COV', color=0xfa0000)
        embed.set_author(name='Источник по статистике',
                         url='https://www.interfax.ru/chronicle/novyj-koronavirus-v-kitae.html')
        embed.add_field(name='В мире', value=world, inline=True)
        embed.add_field(name='В России', value=russia, inline=True)
        chan = self.bot.get_channel(672091108666376193)

        while True:
            time_embed = time.time()
            if time_embed >= int(response_time[0]):
                await chan.send(embed=embed)
                response_time += 86400
                with conn:
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO covidtime (time) VALUES (%s)", response_time)
            else:
                await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(Tasks(bot))
