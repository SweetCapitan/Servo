import os
# noinspection PyUnresolvedReferences,PyPackageRequirements
from discord.ext import commands
import discord

# TODO Потыкать домен и сайт и намутить отправку текстовых логов на домен
from Lib import Logger, result_embed

logger = Logger()


class Bot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        logger.log('=====================================================')
        logger.log(f'Ready! Authorized with the names: {bot.user.name}')
        count = 0
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.load_extension(f'modules.{file[:-3]}')
                logger.log(f'Loaded extension {file[:-3]}.')
                count += 1
        logger.log(f'Total Modules: {count}')
        logger.log('=====================================================')
        logger.log('Init Complite !')


bot = Bot(command_prefix='?')
os.environ['PREFIX'] = bot.command_prefix


@bot.command(brief='reload', description=f'Reload Module {bot.command_prefix}'
                                         f'reload <module name> or <all>')
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
        await ctx.send(f'Reloaded [{extension}]')
        logger.comm(f'RELOAD module: [{extension}]. Author: {ctx.message.author}')


@bot.command(brief='load', description=f'Load module. {bot.command_prefix}'
                                       f'load <module name>')
@commands.has_permissions(administrator=True)
async def load(self, ctx, extension):
    self.bot.load_extension(f'modules.{extension}')
    await ctx.send(f'Loaded {extension}')
    self.logger.comm(f'LOAD module: {extension}. Author: {ctx.message.author}')


bot.run(os.environ.get('BOT_TOKEN'))
