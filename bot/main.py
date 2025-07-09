import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from .config import settings
from .handlers import user, admin


def create_bot() -> Bot:
    return Bot(token=settings.token, default=DefaultBotProperties(parse_mode="HTML"))


def setup_dispatcher(bot: Bot) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(user.router)
    dp.include_router(admin.router)
    return dp


async def main():
    bot = create_bot()
    dp = setup_dispatcher(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
