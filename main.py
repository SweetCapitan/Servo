import discord
from discord.ext import commands
import os
from .config import BOT_TOKEN


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                print(f'loaded extension {file[:-3]}.')


bot = Bot(command_prefix='?')


async def result_embed(result_state, description, message):
    embed = discord.Embed(title=result_state, description=description, color=0xd5de21)
    await message.send(embed=embed)


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


bot.run(BOT_TOKEN)