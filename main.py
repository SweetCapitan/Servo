import os
import time
# noinspection PyUnresolvedReferences,PyPackageRequirements
import discord_slash
from discord.ext import commands
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandOptionType
import config
from discord_webhook import DiscordWebhook
from Lib import Logger, embed_generator, pluralize, perms

bot_start_time = time.time()
logger = Logger()


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        command_list = []
        logger.log('=====================================================')
        logger.log(f'Готово! Авторизовался под именем: {bot.user.name}')
        count = 0
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                logger.log(f'Загружен модуль {file[:-3]}')
                count += 1
        command_list = str(await slash.to_dict())
        logger.log(f'Всего Модулей: {count}')
        logger.log('Всего Команд: {}'.format(command_list.find("{'name'") - 1))
        try:
            await slash.sync_all_commands()
        except Exception as Ex:
            wh = DiscordWebhook(url=os.environ.get('WH_URL'), content='Ошибка Сихронизации slash команд!')
            wh.execute()
            logger.warn(f'Произошла ошибка при синхронизации slash команд!\n {Ex}')
        else:
            logger.log('Slash команды синхронизированны!')
        logger.log('=====================================================')
        bot_time = round(time.time() - bot_start_time)
        logger.log(f'Загрузка завершена за {str(bot_time) + pluralize(bot_time, " секунду", " секунды", " секунд")}!')


bot = Bot(command_prefix='?', owner_id=252469010308792322,
          description='Этот бот напсан чисто по фану, для использования на собственном сервере. Если возникли вопросы, '
                      'то прошу ко мне на сервер https://discord.gg/4c7TbSd')
slash = SlashCommand(bot, sync_commands=True)

module_List_Choices = [{"name": str(file[:-3]),
                        "value": str(file[:-3])} for file in os.listdir('modules') if file.endswith('.py')]
module_List_Choices.append({"name": "Все_нахуй!!!",
                            "value": "all"})


@slash.slash(name='reload', description='Перезагрузка модуля из памяти бота', permissions=perms,
             options=[create_option(name='module', description='Имя модуля, который вы хотите перезапустить',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=module_List_Choices)])
async def reload(ctx: SlashContext, module):
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
        await ctx.send(embed=embed_generator(f'Всего модулей перезагружено: {count}\n',
                                             f'{module_list_text}'))
        logger.comm(f'RELOAD module: [{module}]. Author: {ctx.author}')
    else:
        bot.unload_extension(f'modules.{module}')
        bot.load_extension(f'modules.{module}')
        await ctx.send(embed=embed_generator('Перезагружен!', f'Модуль [{module}] перезагружен'))
        logger.comm(f'RELOAD module: [{module}]. Author: {ctx.author}')


@slash.slash(name='load',
             description='Загружает модуль в память бота, до его перезагрузки', permissions=perms,
             options=[create_option(name='extension', description='Имя модуля, который вы хотите загрузить example.py',
                                    option_type=SlashCommandOptionType.STRING, required=True)])
async def load(self, ctx, extension):
    self.bot.load_extension(f'modules.{extension}')
    await result_embed('Загружен!', f'Модуль [{extension}] Загружен', ctx)
    self.logger.comm(f'LOAD module: {extension}. Author: {ctx.message.author}')


bot.run(os.environ.get('BOT_TOKEN'))
