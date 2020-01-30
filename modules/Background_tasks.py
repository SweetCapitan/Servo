import asyncio
import os
import random
import time

import discord
from discord.ext import commands

# from main import pluralize

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


rainbow_role_name = os.environ.get('ROLE_RAINBOW')
server_id = os.environ.get('SERVER_ID')
RAINBOW_STATUS = os.environ.get('RAINBOW_STATUS')

# start_time = time.time()
start_time = int(os.environ.get('TIME'))
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


class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.rainbow())
        bot.loop.create_task(self.status())
        bot.loop.create_task(self.virus())

    async def rainbow(self):
        if bool(RAINBOW_STATUS):
            for role in self.bot.get_guild(int(server_id)).roles:
                if str(role) == str(rainbow_role_name):
                    print("Rainbow: Role detected")
                    while not self.bot.is_closed():
                        try:
                            await role.edit(color=random.choice(colours))
                        except Exception as e:
                            print('Error: ' + str(e))
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

    async def virus(self):
        from bs4 import BeautifulSoup
        import requests
        url = 'https://bnonews.com/index.php/2020/01/the-latest-coronavirus-cases/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.find('strong')
        chan = self.bot.get_channel(672091108666376193)
        await chan.send(text.getText())
        await asyncio.sleep(21600)
        # print(text.getText())


def setup(bot):
    bot.add_cog(Tasks(bot))
