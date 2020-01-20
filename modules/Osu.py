import os
import discord
from discord.ext import commands
import requests

API_KEY = os.environ.get('API_KEY')


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


class OSU(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # TODO:Привести эту хуйню в божеский вид
    @commands.command(aliases=['osu'], brief='ЩЫГ!',
                      description='ТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫК')
    async def get_user_osu(self, ctx, *username):
        if username:
            url = 'https://osu.ppy.sh/api/get_user?&k=' + API_KEY + '&u=' + str(username[0])
            r = requests.get(url, verify=True)
            user_data = r.json()
            embed = discord.Embed(title='Информация о пользователе ЩЫГ!', color=0xe95be9)
            embed.add_field(name='Username', value=user_data[0]['username'], inline=True)
            embed.add_field(name='UserID', value=user_data[0]['user_id'], inline=True)
            embed.add_field(name='Играет в кружки уже с: ', value=user_data[0]['join_date'], inline=True)
            embed.add_field(name='Всего игр:', value=user_data[0]['playcount'], inline=True)
            embed.add_field(name='Уровень: ', value=user_data[0]['level'], inline=True)
            embed.add_field(name='ПЭПЭ: ', value=user_data[0]['pp_raw'], inline=True)
            embed.add_field(name='Кантри: ', value=user_data[0]['country'], inline=True)
            embed.add_field(name='Акка: ', value=round(float(user_data[0]['accuracy']), 2), inline=True)
            time_osu = int(user_data[0]['total_seconds_played'])
            t_min = round(
                (time_osu - (time_osu // 86400) * 86400 - (
                        (time_osu - (time_osu // 86400) * 86400) // 3600) * 3600) // 60)
            t_sec = round(time_osu - (time_osu // 86400) * 86400 - (
                    (time_osu - (time_osu // 86400) * 86400) // 3600) * 3600 - t_min * 60)
            t_hour = round((time_osu - (time_osu // 86400) * 86400) // 3600)
            t_day = round(time_osu // 86400)
            t_osu = ' %s {}, %s {}, %s {}, %s {}'.format(
                pluralize(t_day, 'день', 'дня', 'дней'),
                pluralize(t_hour, 'час', 'часа', 'часов'),
                pluralize(t_min, 'минуту', 'минуты', 'минут'),
                pluralize(t_sec, 'секунду', 'секунды', 'секунд')
            ) % (t_day, t_hour, t_min, t_sec)
            embed.add_field(name='Наигранно уже: ', value=t_osu, inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send('Еблан, ты никнейм не ввел !')


def setup(bot):
    bot.add_cog(OSU(bot))
