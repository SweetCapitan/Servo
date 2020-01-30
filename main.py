import os

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
from Lib import Logger

logger = Logger()

class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        logger.log(f'Ready! Authorized with the names: {bot.user.name}')
        count = 0
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                logger.log(f'Loaded extension {file[:-3]}.')
                count += 1
        logger.log(f'Total Modules: {count}')


bot = Bot(command_prefix='?')


@bot.command()
async def reload_all(ctx):
    count = 0
    module_list = []
    for file in os.listdir('modules'):
        if file.endswith('.py'):
            module_list.append(file[:-3] + '\n')
            bot.unload_extension(f'modules.{file[:-3]}')
            bot.load_extension(f'modules.{file[:-3]}')
            logger.log(f'Reload Module: {file}')
            count += 1
    module_list_text = ''
    for mod in module_list:
        module_list_text = module_list_text + mod
    await ctx.send(f'Всего модулей перезагружено: {count}\n'
                   f'{module_list_text}')
    # TODO Засунуть это эмбед(Не делаю я этого щас, потому-что хочу пиздец спать)
    logger.comm(f'RELOAD_ALL. Author: {ctx.message.author}')


# bot.run(BOT_TOKEN)
bot.run(os.environ.get('BOT_TOKEN'))
