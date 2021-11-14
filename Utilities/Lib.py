import re
from datetime import datetime
import discord
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission,\
    create_multi_ids_permission
from discord_slash.model import SlashCommandPermissionType
import configparser
import os


class Logger:
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


class ResultEmbeds:
    def error(self, description):
        embed = discord.Embed(title='⚠️ Криворукий уебан, у тебя ошибка! ⚠️', description=description, color=0xf44336)
        return embed

    def done(self, description):
        embed = discord.Embed(title='Успешно', description=description, color=0x8fce00)
        return embed

    def embed(self, title, description):
        embed = discord.Embed(title=title, description=description, color=0x008080)
        return embed

    def warn(self, description):
        embed = discord.Embed(title='Что-то пошло не так', description=description, color=0xFFFF00)
        return embed


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


perms = {
    os.environ.get('SERVER_ID'): [
        create_permission(os.environ.get('MODERATOR_ROLE_ID'), SlashCommandPermissionType.ROLE, True),
        create_permission(os.environ.get('SERVER_ID'), SlashCommandPermissionType.ROLE, False)]
    # Если хотите отключить обычным пользователям использовать /команду, в аргументах команды укажите
    # default_permission = False. Такой костыль не обязателен.
    }
