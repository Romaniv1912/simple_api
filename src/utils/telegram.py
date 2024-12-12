from aiogram import Bot
from aiogram.exceptions import AiogramError, DetailedAiogramError


async def send_message(bot_token: str, chat_id: str, message: str) -> str:
    bot = Bot(token=bot_token)

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except DetailedAiogramError as e:
        return e.message
    except AiogramError as e:
        return str(e)

    return 'OK'
