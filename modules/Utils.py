import asyncio
import io
import os
from contextlib import redirect_stdout
import discord
import requests
from discord.ext import commands
import sys

sys.path.append('..')
from Lib import Logger, result_embed, pluralize

BTC_PRICE_URL_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'
PREFIX = os.environ.get('PREFIX')


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    logger = Logger()

    @commands.command(aliases=['btc', 'crypto', 'cry'],
                      description='Реклама YOBA в описании SERVO-BOT'
                                  '\nЗачем боту эта функция ? А хуй ее знает ¯\\_(ツ)_/¯'
                                  '\n args: <money_code:str>',
                      brief='Bitcoin price')
    async def crypto(self, ctx, *args):
        valute = ''
        limit = 8
        if not args:
            valute = 'usd'
        elif args[0]:
            valute = args[0]
        valute = valute.upper()

        os.environ['API_KEY_COINMARKET'] = '3f4061e6-fb5e-40a0-8f7c-d3f70842fca7'
        API_KEY_COINMARKET = os.environ.get('API_KEY_COINMARKET')

        url_usd = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/' \
                  f'listings/latest?start=1&limit={limit}&convert={valute}&CMC_PRO_API_KEY={API_KEY_COINMARKET}'
        req = requests.get(url_usd)
        json = req.json()
        embed = discord.Embed(title="Сryptocurrencies price",
                              description="The cost of cryptocurrencies at the "
                                          "moment according to the coinmarketcap exchange.",
                              color=0xd5de21)
        for i in json['data']:
            price = str(i['quote'][valute]['price'])
            embed.add_field(name=i['name'], value=price, inline=True)
            # embed.add_field(name='Изменения за Час', Коммментированно до востребованности
            #                 value=f"[{round(((int(float(price)) / 100) * int(float(i['quote'][valute]['percent_change_1h']))), 1)}]",inline=True)
            embed.add_field(name='Изменения за Сутки',
                            value=f"[{round(((int(float(price)) / 100) * int(float(i['quote'][valute]['percent_change_24h']))), 1)}]",
                            inline=True)
            embed.add_field(name='Неделю',
                            value=f"[{round(((int(float(price)) / 100) * int(float(i['quote'][valute]['percent_change_7d']))), 1)}]",
                            inline=True)

        await ctx.send(embed=embed)
        self.logger.comm('crypto_price')

    @commands.command(
        description='By executing the command, the bot will send a random quote taken from bash.im to the chat',
        brief='Random quote with bash.im')
    async def bash(self, ctx):
        from bs4 import BeautifulSoup
        url = 'https://bash.im/random'
        rs = requests.get(url)
        root = BeautifulSoup(rs.text, 'html.parser')
        mydivs = root.find("div", {"class": "quote__body"})
        quote = mydivs.getText('\n', strip=True)
        await result_embed('Рандомная цитата с Bash.im', str(quote), ctx)
        self.logger.comm(f'BASH. Author: {ctx.message.author}')

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

    def _await(self, coro):  # це костыль для выполнения асинхронных функций в exec
        asyncio.ensure_future(coro)

    @commands.command(aliases=['ex', 'exec'],
                      description='This command allows you to execute python code directly from the chat itself.\n'
                                  'P.s. Temporarily runs on Iteratorw code\n'
                                  f'Usage: {PREFIX}execute ` ` `code` ` ` (without spaces)',
                      brief='Execute Python code "')
    @commands.has_permissions(administrator=True)
    async def execute(self, ctx):
        code = ctx.message.content.split("```")
        if len(code) < 3:
            await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', 'Код где блять ?', ctx)
        out, is_error = self._exec(code[1].strip().rstrip(), globals(), locals())

        if is_error:
            await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', out, ctx)
            self.logger.error(f'Unsuccessful attempt to execute code. Author: {ctx.message.author}\n{out}')
        else:
            await result_embed('Код успешно выполнен!', out, ctx)
            self.logger.comm(f'EXECUTE. Author: {ctx.message.author}')

    #  --------------------------------------End of ITERATORW Code------------------------------------------------------
    @commands.command(brief='Opening a coub in chat',
                      description='Are you too bored and lonely? Do you want to share a good coub with someone?'
                                  'But doesn’t it open right in the chat? Not a problem, just enter the command and'
                                  ' link to the coub and it will immediately appear in the chat!'
                                  f'{PREFIX}coub <link>')
    async def coub(self, ctx, url):
        url = "http://coub.com//api/v2/coubs" + url[21:]
        r = requests.get(url)
        coub_data = r.json()
        views = coub_data["views_count"]
        title = coub_data["title"]
        await ctx.channel.purge(limit=1)
        try:
            link = coub_data["file_versions"]["share"]["default"]
        except Exception as e:
            await result_embed('Упс...', 'Что-то пошло не так, проверьте ссылку', ctx)
            return
        await ctx.send(f'Название: {title} Просмотров: {views} Ссылка: {link}')
        self.logger.comm(f'COUB. Author: {ctx.message.author}')

    @commands.command(aliases=['rainbow', 'rb'], brief='YOBA',
                      description='Реклама YOBA в говнокоде Python')
    @commands.has_permissions(administrator=True)
    async def change_rainbow(self, ctx, state):
        rainbow_role_name = os.environ.get('ROLE_RAINBOW')
        role = discord.utils.get(ctx.guild.roles, name=rainbow_role_name)
        if role is not None:
            if state.lower() == 'on' or state.lower() == 'true':
                os.environ[str(ctx.guild.id) + '_RAINBOW_STATUS'] = 'True'
                await result_embed('Модуль [RAINBOW]', 'Включен!', ctx)
                self.logger.comm(f'[RAINBOW] Turn On! Guild: {ctx.guild.name}')
            if state.lower() == 'off' or state.lower() == 'false':
                os.environ[str(ctx.guild.id) + '_RAINBOW_STATUS'] = 'False'
                await result_embed('Модуль [RAINBOW]', 'Выключен!', ctx)
                self.logger.comm(f'[RAINBOW] Turn Off! Guild: {ctx.guild.name}')
        else:
            try:
                await discord.Guild.create_role(ctx.guild,
                                                name='Rainbow',
                                                hoist=True,
                                                reason='SERVO-BOT Автоматическое добавление роли!')
                await result_embed('[RAINBOW]',
                                   'Т.к. роль не была найдена, она была добавлена автоматически!\n'
                                   'Пожалуйста добавте эту роль, тем кому вы хотите сделать радужный никнейм :3', ctx)
            except discord.Forbidden:
                await result_embed('Прав не завезли!',
                                   f'Добавте боту права "manage_roles" или сами создайте роль ``{rainbow_role_name}``',
                                   ctx)


def setup(bot):
    bot.add_cog(Utils(bot))
