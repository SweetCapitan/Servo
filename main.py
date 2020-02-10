import os
# noinspection PyUnresolvedReferences,PyPackageRequirements
from discord.ext import commands

# TODO Потыкать домен и сайт и намутить отправку текстовых логов на домен
from Lib import Logger, result_embed
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
@commands.has_permissions(administrator=True)
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
    await result_embed(f'Всего модулей перезагружено: {count}\n',
                   f'{module_list_text}',ctx)

    logger.comm(f'RELOAD_ALL. Author: {ctx.message.author}')


bot.run(os.environ.get('BOT_TOKEN'))
