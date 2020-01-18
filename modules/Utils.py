import asyncio
import io
import os
from contextlib import redirect_stdout
import discord
import requests
from discord.ext import commands
from .main import result_embed

BTC_PRICE_URL_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_btc_price():
        r = requests.get(BTC_PRICE_URL_coinmarketcap)
        response_json = r.json()
        usd_price = response_json[0]['price_usd']
        rub_rpice = response_json[0]['price_rub']
        percent_change_1h = response_json[0]['percent_change_1h']
        percent_change_24h = response_json[0]['percent_change_24h']
        percent_change_7d = response_json[0]['percent_change_7d']
        return usd_price, rub_rpice, percent_change_1h, percent_change_24h, percent_change_7d

    @commands.command(aliases=['btc'],
                      description='This command sends you the current value of bitcoin in rubles and dollars.'
                                  '\nЗачем боту эта функция ? А хуй ее знает ¯\_(ツ)_/¯'
                                  '\n args: <7d,1d,1h,None>',
                      brief='Bitcoin price')
    async def btcprice(self, ctx, *args: str):
        btc_price_usd, btc_price_rub, percent1, percent24, percent7 = self.get_btc_price()
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

    @commands.command(
        description='By executing the command, the bot will send a random quote taken from bash.im to the chat',
        brief='Random quote with bash.im')
    async def bash(self,ctx):
        from bs4 import BeautifulSoup
        url = 'https://bash.im/random'
        rs = requests.get(url)
        root = BeautifulSoup(rs.text, 'html.parser')
        mydivs = root.find("div", {"class": "quote__body"})
        quote = mydivs.getText('\n', strip=True)
        await result_embed('Рандомная цитата с Bash.im', str(quote), ctx)

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
                                  'Usage:execute ` ` `code` ` ` (without spaces)',
                      brief='Execute Python code "')
    async def execute(self, ctx):
        code = ctx.message.content.split("```")
        if len(code) < 3:
            await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', 'Код где блять ?', ctx)
        out, is_error = self._exec(code[1].strip().rstrip(), globals(), locals())

        if is_error:
            await result_embed('⚠️ Криворукий уебан, у тебя ошибка! ⚠️', out, ctx)

        else:
            await result_embed('Код успешно выполнен!', out, ctx)

#  --------------------------------------End of ITERATORW Code---------------------------------------------------------
def setup(bot):
    bot.add_cog(Utils(bot))