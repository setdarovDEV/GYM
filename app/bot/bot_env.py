from os import getenv
from dotenv import load_dotenv
load_dotenv()


class Bot:
    BOT_TOKEN = getenv("BOT_TOKEN")

class DB:
    USER = getenv("DB_USER")
    PASSWORD = getenv("DB_PASSWORD")
    HOST = getenv("DB_HOST")
    PORT = getenv("DB_PORT")
    NAME = getenv("DB_NAME")



class ENV:
    bot = Bot()
    db = DB()
