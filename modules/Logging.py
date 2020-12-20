import os
import random
from discord.ext import commands
import sys
sys.path.append('..')
from Lib import Logger, result_embed, pluralize

notification_channel = 738855014377848943
KGB_MODE = os.environ.get('KGB_MODE')


def choice_phrase(member: str, event: str):
    phrases = {
        'join': [
            f'{member} присоеденился к нам. Земля ему говном.',
            f'{member} присоеденился, чтобы рвать жопы и есть мороженное. Как видите мороженное он уже доел ...',
            f'Дружок пирожок {member}, клуб кожевного ремесла на два этажа ниже',
            f'Злой дух по имени {member} вторгся к вам'
        ],
        'leave': [
            f'{member} слился - слабак!',
            f'{member} ушел, но обещал вернуться!',
            f'{member} наелся и спит.\n {member} умер.'
        ],
        'ban': [
            f'Ой ой ой, ну ты даешь {member}. Пойди ка погуляй.',
            f'Либераху порвало. В гулаг тебя {member}.',
            f'{member} вы напугали деда, получай Банхаммером по лицу.',
            f'{member} наказан, гулять он не выйдет.'
        ],
        'unban': [
            f'{member} хорошо себя вел. Он получил помилование.',
            f'{member} ну хорошо. На этот раз я тебя прощаю.',
            f'{member}, а у тебя хорошая попка. На этот раз мы закроем глаза на твои проступки'
        ]
    }
    return random.choice(phrases[event])


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(notification_channel)

    logger = Logger()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await result_embed('Зашел на сервер!', choice_phrase(member, 'join'), self.channel)
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await result_embed('Вышел с сервера!', choice_phrase(member, 'leave'), self.channel)
        self.logger.log(f'{member} logged into the server')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        await result_embed('Забанен!', choice_phrase(member, 'ban'), self.channel)
        self.logger.log(f'[Ban] Guild: {guild} User: {member}')

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        await result_embed('Разбанен!', choice_phrase(member, 'unban'), self.channel)
        self.logger.log(f'[Unban] Guild: {guild} User: {member}')

    # @commands.command()
    # async def kgb(self, ctx, state):
    #     if state.lower() == 'true' or state.lower() == 'on':
    #         os.environ['KGB_MODE'] = 'True'
    #         await ctx.send('Включен режим слежки')
    #     elif state.lower() == 'false' or state.lower() == 'off':
    #         os.environ['KGB_MODE'] = 'False'
    #         await ctx.send('Выключен режим слежки')
    #
    # if KGB_MODE == 'True':
    #     @commands.Cog.listener()
    #     async def on_message_delete(self, message):
    #         self.logger.log(f'[Deleted Message] Text: {message.content} Author: {message.author}')
    #
    #     @commands.Cog.listener()
    #     async def on_message_edit(self, before, after):
    #         self.logger.log(f'[Edited Message] Before: {before.content} After: {after.content} Author: {before.author}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        await ctx.send(f'{ctx.message.author.mention} {ex}')


def setup(bot):
    bot.add_cog(Logging(bot))
