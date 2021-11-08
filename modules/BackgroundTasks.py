import asyncio
import os
import time
import discord
from discord.ext import commands
from colorsys import hls_to_rgb
from discord import Embed
import sys
import configparser

sys.path.append('..')
from Lib import Logger, result_embed, pluralize

logger = Logger()
start_time = time.time()
config = configparser.ConfigParser()
config.read('setting.ini')
response_time = config.get('Setting', 'covid_time')
rainbow_role_name = config.get('Setting', 'role_rainbow')
rainbow_role_status = bool(config.get('Setting', 'role_rainbow_status'))


class BackgroundTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.status())
        bot.loop.create_task(self.virus())
        # Some Shit
        if rainbow_role_status:
            bot.loop.create_task(self.rainbow(530374773612478475))
        # asyncio.run_coroutine_threadsafe(self.rainbow_change, self.bot.loop)

    async def rainbow(self, server_id):
        hue = 0
        role = discord.utils.get(self.bot.get_guild(server_id).roles, name=rainbow_role_name)
        while True:
            hue = (hue + 7) % 360
            rgb = [int(x * 255) for x in hls_to_rgb(hue / 360, 0.5, 1)]
            clr = discord.Color(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
            try:
                await role.edit(color=clr)
            except Exception as e:
                logger.error(str(e))
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
            config.read('setting.ini', encoding='utf-8')
            streaming_status_text = config.get('Setting', 'streaming_status_text')
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
                await asyncio.sleep(5)
                if streaming_status_text != '':
                    await self.bot.change_presence(
                        activity=discord.Streaming(name=streaming_status_text, url='https://www.twitch.tv/dancho67'))
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(e)

    async def virus(self, response_time=response_time):
        from bs4 import BeautifulSoup
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.interfax.ru/chronicle/novyj-koronavirus-v-kitae.html') as resp:
                result = BeautifulSoup(await resp.text(), 'html.parser')
                info = result.findAll('span', {'class': 'c19_statistic_num'})
                world = f'Случаев SARS2-COV в Мире: {info[3].getText().split("+")[0]} \n' \
                        f'+{info[3].getText().split("+")[1]} за текущие сутки,' \
                        f' Из них везучие бастарды: {info[2].getText()}, ded inside-ов: {info[4].getText()}'
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

                if response_time:
                    _response_time = int(response_time)
                    while True:
                        time_embed = time.time()
                        if time_embed >= _response_time:
                            _response_time += 86400
                            config.set('Setting', 'covid_time', str(_response_time))
                            with open('setting.ini', 'w') as configFile:
                                config.write(configFile)
                            await chan.send(embed=embed)
                        else:
                            await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(BackgroundTasks(bot))
