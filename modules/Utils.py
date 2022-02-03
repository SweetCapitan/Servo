import asyncio
import io
import json
import os
import urllib
from contextlib import redirect_stdout
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, pages
from discord.ext.commands import slash_command
from discord.commands import Option
import sys
import random
import Utilities.logger as logger
from Utilities.embeds import pluralize, ResultEmbeds
from Utilities.webhook import send_webhook
from Utilities.servomysql.servo_mysql import ServoMySQL

btc_price_url_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'
db = ServoMySQL()
re = ResultEmbeds()
streaming_status_text = db.get_setting('streaming_status_text')


def generate_embed_image(query, index, image) -> discord.Embed:
    embed: discord.Embed = re.done(f'Картинка по запросу:[`{query}`]. Индекс: {index}.')
    embed.set_author(url=image["image"]["contextLink"], icon_url=image["image"]["thumbnailLink"],
                     name=image["title"])
    embed.set_image(url=image["link"])
    return embed


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_pages(self):
        return self.pages

    server_ids = [int(os.environ.get('SERVER_ID'))]

    @slash_command(name='btc', description='Реклама YOBA в описании SERVO-BOT', guild_ids=server_ids)
    async def crypto(self, ctx, money_code: Option(str, description="Желаемая валюта", choices=["RUB", "USD"])):
        limit = 8
        api_key_coinmarket = os.environ.get('API_KEY_COINMARKET')
        url_usd = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/' \
                  f'listings/latest?start=1&limit={limit}&convert={money_code}&CMC_PRO_API_KEY={api_key_coinmarket}'
        req = requests.get(url_usd)
        req_json = req.json()
        embed = discord.Embed(title="Стоимости криптовалют",
                              description="Стоимость криптовалют на данный момент по данным биржи coinmarketcap.",
                              color=0xd5de21)
        for i in req_json['data']:
            price = str(i['quote'][money_code]['price'])
            embed.add_field(name=i['name'], value=price, inline=True)
            embed.add_field(name='Изменения за Сутки',
                            value="[{}]".format(
                                round(((int(float(price)) / 100) * int(float(i['quote'][money_code]
                                                                             ['percent_change_24h']))), 1)),
                            inline=True)
            embed.add_field(name='Неделю',
                            value="[{}]".format(
                                round(((int(float(price)) / 100) * int(float(i['quote'][money_code]
                                                                             ['percent_change_7d']))), 1)), inline=True)
        await ctx.respond(embed=embed)
        logger.comm('crypto_price. Author: ' + ctx.author)

    @slash_command(name='bash',
                   description='Выполнив команду, бот отправит в чат случайную цитату из bash.im',
                   guild_ids=server_ids)
    async def bash(self, ctx):
        from bs4 import BeautifulSoup
        url = 'https://bash.im/random'
        rs = requests.get(url)
        root = BeautifulSoup(rs.text, 'html.parser')
        mydivs = root.find("div", {"class": "quote__body"})
        quote = mydivs.getText('\n', strip=True)
        await ctx.respond(embed=re.done('Рандомная цитата с Bash.im\n' + str(quote)))
        logger.comm(f'BASH. Author: {ctx.author}')

    # -----------------------------------------Start of IteratorW Code -------------------------------------------------
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

    def _exec(self, code, g, l):
        out = io.StringIO()
        d = Utils.MyGlobals(g, l)
        try:
            error = False
            with redirect_stdout(out):
                exec(code, d)
        except Exception as ex:
            error = True
            out.write(str(ex))

        return out.getvalue(), error

    @staticmethod
    def _await(coro):  # це костыль для выполнения асинхронных функций в exec
        asyncio.ensure_future(coro)

    @slash_command(name='exec', description='Эта команда позволяет выполнять код.', guild_ids=server_ids)
    async def execute(self, ctx, code: Option(str, description="Код на питухоне", required=True)):
        if not ctx.author.guild_permissions.manage_messages:
            return ctx.respond("Прав не завезли!", ephemeral=True)
        code = code.replace("```", "")
        out, is_error = self._exec(code.strip().rstrip(), globals(), locals())

        if is_error:
            await ctx.respond(embed=re.error(out))
            logger.error(f'Unsuccessful attempt to execute code. Author: {ctx.author}\n{out}')
        else:
            await ctx.respond(embed=re.done('Код успешно выполнен!\n' + out))
            logger.comm(f'EXECUTE. Author: {ctx.author}')

    #  --------------------------------------End of ITERATORW Code------------------------------------------------------
    @slash_command(name='coub', description='Открывает коуб прямо в чате!', guild_ids=server_ids)
    async def coub(self, ctx, url_to_coub: Option(str, description="Url to Coub", required=True)):
        url = "http://coub.com//api/v2/coubs" + url_to_coub[21:]
        r = requests.get(url)
        coub_data = r.json()
        views = coub_data["views_count"]
        title = coub_data["title"]
        url_to_ass = "https://coubassistant.com/en/web"
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"urlpost\"\r\n\r\n{url_to_coub}\r\n-----011000010111000001101001--\r\n"
        headers = {'content-type': 'multipart/form-data; boundary=---011000010111000001101001'}
        response = requests.request("POST", url_to_ass, data=payload, headers=headers)
        result = BeautifulSoup(response.text, 'html.parser')
        song = coub_data["file_versions"]["html5"]['audio']['high']
        song_name = result.findAll('h3')[0].getText()
        if song_name == 'Easy way to search for music':
            song_name = 'Музыка не найдена!'
        try:
            link = coub_data["file_versions"]["share"]["default"]
        except Exception:
            await ctx.respond(embed=re.warn('Что-то пошло не так, проверьте ссылку'))
            return
        await ctx.respond(
            f'Название: ``{title}``\nПросмотров: ``{views}``\nМузыка из Куба: ``{song_name}``\nСсылка: {link} '
            f'\nАудио: {song["url"]}   {round(song["size"] / 1048576, 2)}mB')
        logger.comm(f'COUB. Author: {ctx.message.author}')

    @slash_command(name='rainbow',
                   description='Реклама YOBA в говнокоде Python', guild_ids=server_ids)
    async def change_rainbow(self, ctx, state: Option(bool, description="Вкл/выкл Rainbow mode on guild")):
        rainbow_role_name = db.get_setting('role_rainbow')
        rainbow_role_status = db.get_setting('role_rainbow_status', boolean=True)
        role = discord.utils.get(ctx.guild.roles, name=rainbow_role_name)
        if role is not None:
            if state and not rainbow_role_status:
                db.update_setting('role_rainbow_status', True)
                await ctx.respond(embed=re.done('Модуль ``RAINBOW`` Включен!'))
                logger.comm(f'[RAINBOW] Turn On! Guild: {ctx.guild.name}')
            elif not state and rainbow_role_status:
                db.update_setting('role_rainbow_status', False)
                await ctx.respond(embed=re.done('Модуль ``RAINBOW`` Выключен!'))
                logger.comm(f'[RAINBOW] Turn Off! Guild: {ctx.guild.name}')
        else:
            try:
                await discord.Guild.create_role(ctx.guild,
                                                name='Rainbow',
                                                hoist=True,
                                                reason='SERVO-BOT Автоматическое добавление роли!')
                await ctx.respond(embed=re.embed('``RAINBOW``',
                                                 'Т.к. роль не была найдена, она была добавлена автоматически!\n'
                                                 'Пожалуйста добавте эту роль, тем кому вы хотите сделать '
                                                 'радужный никнейм :3'))
            except discord.Forbidden:
                await ctx.respond(embed=re.warn('Прав не завезли!\n'
                                                'Добавте боту права "manage_roles" или сами создайте роль '
                                                f'``{rainbow_role_name}``'))

    @slash_command(name='choice',
                   description='Выбирает одно из нескольких значений, указанных через запятую',
                   guild_ids=server_ids)
    async def choice(self, ctx, option: Option(str, description="список значений", required=True)):
        await ctx.respond(embed=re.done(f'Я выбираю: {random.choice(option.split(", "))}'))

    @slash_command(name='status',
                   description='Задает текст, который будет отображаться в статусе бота',
                   guild_ids=server_ids)
    async def set_status(self, ctx, text: Option(str, description="укажите статус бота", required=True)):
        try:
            db.update_setting('streaming_status_text', text)
            await ctx.respond(embed=re.done(f'Статус [{text}] был установлен!'))
        except Exception as e:
            await ctx.respond(embed=re.error(e))
        logger.comm(f'[Status Change] {ctx.author} {text}')

    @slash_command(name='image_search', description='Поиск картинок в Гоголе', guild_ids=server_ids)
    async def image_srh(self, ctx, query: Option(str, description="Поисковой запрос", required=True)):
        url = f'https://customsearch.googleapis.com/customsearch/v1?cx={os.environ.get("GOOGLE_CX")}={query}&safe=off' \
              f'&searchType=image&num=10&start=0&key={os.environ.get("G_API_KEY")} '

        try:
            response = requests.get(url=url)
            raw_data = response.json()

            if response.status_code != 200:
                await ctx.send(embed=re.error('Произошла ашибка API\n' + raw_data["error"]["status"]))

            if raw_data["searchInformation"]["totalResults"] == "0":
                await ctx.send(embed=re.warn(f'Картинка по запросу {query} не найдена!'))
            index = 0

            image = raw_data["items"][index]

            def get_embed(_index):
                return generate_embed_image(query, _index, image)

            embed = generate_embed_image(query, index, image)

            self.pages = [get_embed(0), get_embed(1), get_embed(2), get_embed(3), get_embed(4),
                          get_embed(5), get_embed(6), get_embed(7), get_embed(8), get_embed(9)]

            paginator = pages.Paginator(pages=self.get_pages())
            await paginator.respond(ctx.interaction, target_message=f"По запросу {query} найдено", ephemeral=False)

        except Exception as E:
            await ctx.respond(embed=re.error(E))


def setup(bot):
    bot.add_cog(Utils(bot))
