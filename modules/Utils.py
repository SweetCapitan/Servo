import os

import discord
import requests
from discord.ext import commands

BTC_PRICE_URL_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'


class Utils(commands.Cog):

    def __init__(self,bot):
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
    async def btcprice(self,ctx, *args: str):
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
