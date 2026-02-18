from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application 
from aiogram import Bot, Dispatcher
from utils.webhook import set_webhook
from config.settings import (
    BOT_PROPERTIES,
    WEB_SERVER_PORT,
    WEB_SERVER_HOST,
    WEBHOOK_SECRET,
    BOT_TOKEN,
    DEBUG
)

from config.routers import ROUTERS
from aiohttp import web
import asyncio

dp = Dispatcher()
dp.include_routers(*ROUTERS)
bot = Bot(
    token=BOT_TOKEN,
    default=BOT_PROPERTIES,
)

async def start_polling() -> None:
    global dp, bot
    import logging
    import sys
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

def start_webhook():
    
    dp.startup.register(set_webhook)
    
    app = web.Application()
    
    webhook_handlers = SimpleRequestHandler(
        secret_token=WEBHOOK_SECRET,
        dispatcher=dp,
        bot=bot,
    )
    webhook_handlers.register(app, path="/webhook")
    
    setup_application(app, dp, bot=bot)
    web.run_app(
        app,
        host=WEB_SERVER_HOST,
        port=WEB_SERVER_PORT,
    )
    
if __name__ == "__main__":
    if not DEBUG:
        start_webhook()
    else:
        asyncio.run(start_polling())
    