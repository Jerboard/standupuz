import asyncio
import logging
import sys
import logging

from handlers import dp
from config import DEBUG
from init import set_main_menu, bot, log_error, scheduler
from db.base import init_models, db_command
from db.events import add_events, close_old_events


async def start_schedulers():
    scheduler.add_job(close_old_events, 'cron', hour=0)
    scheduler.start()


async def main() -> None:
    # await db_command()
    await init_models()
    await set_main_menu()
    await start_schedulers()
    await bot.delete_webhook (drop_pending_updates=True)
    await dp.start_polling(bot)
    pass


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start_bot', with_traceback=False)
    asyncio.run(main())
