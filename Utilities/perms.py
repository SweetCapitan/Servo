import os
from discord_slash.utils.manage_commands import create_permission, SlashCommandPermissionType

perms = {
    os.environ.get('SERVER_ID'): [
        create_permission(int(os.environ.get('MODERATOR_ROLE_ID')), SlashCommandPermissionType.ROLE, True),
        create_permission(int(os.environ.get('SERVER_ID')), SlashCommandPermissionType.ROLE, False)]
    # Если хотите отключить обычным пользователям использовать /команду, в аргументах команды укажите
    # default_permission = False. Такой костыль не обязателен.
    }