import os
import time
# noinspection PyUnresolvedReferences,PyPackageRequirements
from discord.ext import commands
import config
from Lib import Logger, result_embed, pluralize

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
                cog = self.get_cog(f'{file[:-3]}')
                command = cog.get_commands()
                command_list.append([c.name for c in command])
                logger.log(f'Загружен модуль {file[:-3]}')
                count += 1
        logger.log(f'Всего Модулей: {count}')
        logger.log(f'Всего Команд: {len([c for m in command_list for c in m])}')
        logger.log('=====================================================')
        bot_time = round(time.time() - bot_start_time)
        logger.log(f'Загрузка завершена за {str(bot_time) + pluralize(bot_time, " секунду", " секунды", " секунд")}!')


help_com = commands.DefaultHelpCommand(commands_heading='Команды:', no_category='Комманды ядра')

bot = Bot(command_prefix='?', owner_id=252469010308792322,
          description='Этот бот напсан чисто по фану, для использования на собственном сервере. Если возникли вопросы, '
                      'то прошу ко мне на сервер https://discord.gg/4c7TbSd, ну или пишите в лс MeowCaptain#9480',
          help_command=help_com)
os.environ['PREFIX'] = bot.command_prefix


@bot.command(brief='Перезагрузка модуля', description=f'Совершается полная перезагрузка модуля из памяти бота',
             usage='<module name>'
             )
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    if str(extension).lower() == 'all':
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
        await result_embed(f'Всего модулей перезагружено: {count}\n',
                           f'{module_list_text}', ctx)
        logger.comm(f'RELOAD module: [{extension}]. Author: {ctx.message.author}')
    else:
        bot.unload_extension(f'modules.{extension}')
        bot.load_extension(f'modules.{extension}')
        await result_embed('Перезагружен!', f'Модуль [{extension}] перезагружен', ctx)
        logger.comm(f'RELOAD module: [{extension}]. Author: {ctx.message.author}')


@bot.command(brief='Загрузить модуль в память бота', description=f'Загружает модуль в память бота, до его перезагрузки',
             usage='<module name>')
@commands.has_permissions(administrator=True)
async def load(self, ctx, extension):
    self.bot.load_extension(f'modules.{extension}')
    await result_embed('Загружен!', f'Модуль [{extension}] Загружен', ctx)
    self.logger.comm(f'LOAD module: {extension}. Author: {ctx.message.author}')


bot.run(os.environ.get('BOT_TOKEN'))
