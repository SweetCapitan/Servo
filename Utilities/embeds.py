import discord


class ResultEmbeds:
    def error(self, description):
        embed = discord.Embed(title='❌️ Криворукий уебан, у тебя ошибка! ❌', description=description, color=0xf44336)
        return embed

    def done(self, description):
        embed = discord.Embed(title='✔️ Успешно', description=description, color=0x8fce00)
        return embed

    def embed(self, title, description):
        embed = discord.Embed(title=title, description=description, color=0x008080)
        return embed

    def warn(self, description):
        embed = discord.Embed(title='⚠️ Что-то пошло не так ⚠️', description=description, color=0xFFFF00)
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

