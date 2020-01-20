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
    @commands.group(brief='ЩЫГ!',
                    description='ТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫКТЫК')
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Еблан, ты не указал действие')

    @osu.command(aliases=['getuser', 'gU'], brief='ЩЫГ!',
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

    @osu.command()
    async def get_user_resent(self,ctx, *username):
        url = 'https://osu.ppy.sh/api/get_user_recent?k=' + API_KEY + '&u=' + str(username[0])
        r = requests.get(url, verify=True)
        user_data = r.json()
        url_map = 'https://osu.ppy.sh/api/get_beatmaps?k=' + API_KEY + '&b=' + user_data[0]['beatmap_id']
        rr = requests.get(url_map,verify=True)
        map_data = rr.json()
        # "artist":"SakiZ","title":"osu!memories","creator":"DeRandom Otaku"
        embed = discord.Embed(title=map_data[0]['creator'] + ' ' + map_data[0]['artist'] + ' ' + map_data[0]['title'],url='https://osu.ppy.sh/beatmapsets/'+ map_data[0]['beatmapset_id'] + '#osu/' + map_data[0]['beatmap_id'],
                              color=0xe95be9)
        embed.set_author(name='Информация о последней сыгранной карте пользователя: ' + str(username[0]), url='https://osu.ppy.sh/users/'+user_data[0]['user_id'], icon_url=ctx.author.avatar_url)
        embed.add_field(name='Score', value=user_data[0]['score'], inline=True)
        embed.add_field(name='C-c-combo', value=user_data[0]['maxcombo'], inline=True)
        embed.add_field(name='FC', value= 'False' if user_data[0]['perfect'] == '0' else 'True')
        embed.add_field(name='Rank', value=user_data[0]['rank'], inline=True)
        embed.set_image(url=f'https://assets.ppy.sh/beatmaps/{map_data[0]["beatmapset_id"]}/covers/cover.jpg')
        embed.set_footer(text=user_data[0]['date'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OSU(bot))
