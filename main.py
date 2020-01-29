import os
from datetime import datetime

# import discord
# noinspection PyUnresolvedReferences,PyPackageRequirements
# from config import BOT_TOKEN
from discord.ext import commands


# TODO:ФИКС ИМПОРТА
# async def result_embed(result_state, description, message):
#     embed = discord.Embed(title=result_state, description=description, color=0xd5de21)
#     await message.send(embed=embed)
#
#
# def pluralize(source, first, second, third):
#     if int(str(source)[-1]) == 0:
#         return third
#     elif int(str(source)[-2:]) in range(11, 21):
#         return third
#     elif int(str(source)[-1]) == 1:
#         return first
#     elif int(str(source)[-1]) in range(2, 5):
#         return second
#     elif int(str(source)[-1]) in range(5, 10):
#         return third
# TODO Добавить логгирование всех событий на сервере в лог
# TODO Потыкать домен и сайт и намутить отправку текстовых логов на домен
import ctypes  # Це костыль для отображения цветов в консоли Windows
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


class Logger:
    #TODO Попробовать реализовать универсальный логгер комманд, без ручного добавления в логгирование
    @staticmethod
    def get_time():
        iso = datetime.now().isoformat()
        return iso[11:19]

    def log(self, text):
        print(f"\033[32m {self.get_time()} [Logs] \033[37m{str(text)}")

    def warn(self, text):
        print(f"\033[33m\033[3m {self.get_time() + ' [Warning] ' + str(text)}")

    def error(self, text):
        print(f"\033[31m\033[1m {self.get_time() + ' [Error] ' + str(text)}")

    def comm(self, text):
        print(f"\033[32m {self.get_time()} [Logs][Command] \033[37m{str(text)}")

class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        Logger.log(f'Ready! Authorized with the names: {bot.user.name}')
        count = 0
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                Logger.log(f'Loaded extension {file[:-3]}.')
                count += 1
        Logger.log(f'Total Modules: {count}')


bot = Bot(command_prefix='?')


@bot.command()
async def reload_all(ctx):
    count = 0
    for file in os.listdir('modules'):
        if file.endswith('.py'):
            module_list = []
            module_list.append(file[:-3] + '\n')
            bot.unload_extension(f'modules.{file[:-3]}')
            bot.load_extension(f'modules.{file[:-3]}')
            Logger.log(f'Перезагружен модуль: {file}')
            count += 1
    module_list_text = ''
    for mod in module_list:
        module_list_text = module_list_text + mod + '\n'
    await ctx.send(f'Всего модулей перезагружено: {count}'
                   f'{module_list_text}')


# bot.run(BOT_TOKEN)
bot.run(os.environ.get('BOT_TOKEN'))
