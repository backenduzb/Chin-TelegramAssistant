import os

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_ID = 6400925437

START_STICKERS = [
    "CAACAgIAAxkBAAEaBkZpYmoi-R1fcdKRa-6MBWHre3S9hgAC6TMAAgNG8UgXOI-Eu8pCCjgE",
    "CAACAgIAAxkBAAEaBi5pYme3GlT1Y_5zmNHQ7LnRkuENPwACID8AAiS88Uiw82Q9UOEMIDgE",
    "CAACAgIAAxkBAAEaBk5pYmps-k6lxglVuH8iSrVJaIVcWQACqDMAAhcg8UgOt91kvJO4PDgE",
]

BOT_TOKEN = os.getenv("BOT_TOKEN") or ""

DEBUG = os.getenv("BOT_DEBUG") in ["true", "True", "1", "on"]

BS_ID = os.getenv("BUSSINES_CONNECTION_ID")

BOT_PROPERTIEST = DefaultBotProperties(parse_mode="html")

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8080
WEBHOOK_SECRET = os.getenv("BOT_WEBHOOK_SECRET") or ""
WEBHOOK_BASE_URL = os.getenv("BOT_WEBHOOK_BASE_URL") or ""
