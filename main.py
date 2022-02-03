import time

import requests
import discord.ext.commands
from discord import Option
from discord.ext import commands
from discord.ext.commands import slash_command
from discord.ext.commands.context import Context
from discord.ui.view import View

import sys
import os
import config
from Utilities import logger
from Utilities.embeds import pluralize, ResultEmbeds
from Utilities.webhook import send_webhook
from Utilities.servomysql.servo_mysql import ServoMySQL

db = ServoMySQL()
bot_start_time = time.time()
re = ResultEmbeds()
module_list_choices = []


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.persistent_views_added = False

    async def on_ready(self):
        logger.log('=====================================================')
        logger.log(f'Готово! Авторизовался под именем: {bot.user.name}')
        count = 0

        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                logger.log(f'Загружен модуль {file[:-3]}')
                count += 1
                module_list_choices.append(file[:-3])
        logger.log(f'Всего Модулей: {count}')
        logger.log('Всего Команд: {}'.format(len(self.all_commands)))
        module_list_choices.append("all")
        try:
            await self.register_commands()
            # await self.sync_commands()
        except Exception as Ex:
            # await send_webhook(os.environ.get('WH_URL'), 'Ошибка Сихронизации slash команд!')
            logger.warn(f'Произошла ошибка при синхронизации slash команд!\n {Ex}')
            await discord.Bot.close(self)
        else:
            logger.log('Slash команды синхронизированны!')
        logger.log(db.init())
        logger.log('=====================================================')
        bot_time = round(time.time() - bot_start_time)
        logger.log(f'Загрузка завершена за {str(bot_time) + pluralize(bot_time, " секунду", " секунды", " секунд")}!')
        self.persistent_views_added = True


bot = Bot(command_prefix='?', owner_id=252469010308792322,
          description='Этот бот напсан чисто по фану, для использования на собственном сервере. Если возникли вопросы, '
                      'то прошу ко мне на сервер https://discord.gg/4c7TbSd', intents=discord.Intents.default())


class Main(commands.Cog):
    @slash_command(guild_ids=[int(os.environ.get("SERVER_ID"))], name='reload',
                   description='Перезагрузка модуля из памяти бота')
    async def reload(self, ctx, module: Option(str,
                                               choices=module_list_choices,
                                               description="модуль, который будет перезапущен"), ):
        if not ctx.author.guild_permissions.manage_messages:  # Костыльно Ориентированное Программирование в деле
            return ctx.respond("Прав не завезли!", ephemeral=True)
        if str(module) == 'all':
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
            logger.comm(f'RELOAD module: [{module}]. Author: {ctx.author}')
            await ctx.respond(embed=re.done(f'Всего модулей перезагружено: {count}\n{module_list_text}'))
        else:
            bot.unload_extension(f'modules.{module}')
            bot.load_extension(f'modules.{module}')
            logger.comm(f'RELOAD module: [{module}]. Author: {ctx.author}')
            await ctx.respond(embed=re.done(f'Модуль [{module}] перезагружен'))

    @slash_command(guild_ids=[int(os.environ.get("SERVER_ID"))], name='load',
                   description='Загружает модуль в память бота, до его перезагрузки', )
    async def load(self, ctx, extension: Option(str, choices=module_list_choices,
                                                description="модуль, который будет перезапущен")):
        if not ctx.author.guild_permissions.manage_messages:
            return ctx.respond("Прав не завезли!", ephemeral=True)
        bot.load_extension(f'modules.{extension}')
        logger.comm(f'LOAD module: {extension}. Author: {ctx.message.author}')
        await ctx.respond(embed=re.done(f'Модуль [{extension}] Загружен'))


bot.add_cog(Main())
bot.run(os.environ.get('BOT_TOKEN'))
