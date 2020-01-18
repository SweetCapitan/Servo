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
import datetime


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                print(f'loaded extension {file[:-3]}.')


bot = Bot(command_prefix='?')


@bot.command()
async def reload_all(ctx):
    count = 0
    for file in os.listdir('modules'):
        if file.endswith('.py'):
            bot.unload_extension(f'modules.{file[:-3]}')
            bot.load_extension(f'modules.{file[:-3]}')
            await ctx.send(f'Перезагружен модуль: {file}')
            count += 1

    await ctx.send(f'Всего модулей перезагруженно: {count}')


bot.run('')