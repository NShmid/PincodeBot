from aiogram import Bot, types
from core.database.db import admins


async def set_commands(bot: Bot):
    # Команды для всех
    await bot.set_my_commands([types.BotCommand(command='start', description='Запустить бота')])
    
    # Команды админа
    for admin_id in admins:
        await bot.set_my_commands(
            [
                types.BotCommand(command='start', description='Запустить бота'),
                types.BotCommand(command='link', description='Создать ссылку-приглашение')
            ],
            scope=types.BotCommandScopeChat(chat_id=admin_id)
        )