import re
from datetime import datetime
# import ctypes  # Це костыль для отображения цветов в консоли Windows
# kernel32 = ctypes.windll.kernel32
# kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
import discord


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
# TODO Дописать парсер ключей и добавить его использвание в некоторые функции
# def key_parser(string):   Це альфа альфа альфа бета гамма тест парсера ключей, он тут чтобы не забыть про него
#     parser = re.search(r'--([^\s=]+)(?:=(\S+))?', string)
#     return parser.group(2)
