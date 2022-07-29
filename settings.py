import os
from dotenv import load_dotenv, find_dotenv

# Loading .env variables
load_dotenv(find_dotenv())

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise Exception("Please setup the .env variable TELEGRAM_BOT_TOKEN.")

TELEGRAM_SPEAKER_CHAT_ID = os.getenv("TELEGRAM_SPEAKER_CHAT_ID")
if TELEGRAM_SPEAKER_CHAT_ID is None or not str(TELEGRAM_SPEAKER_CHAT_ID).lstrip("-").isdigit():
    raise Exception("You need to specify 'TELEGRAM_SPEAKER_CHAT_ID' env variable: The bot will forward all messages to this chat_id.")
TELEGRAM_SPEAKER_CHAT_ID = int(TELEGRAM_SPEAKER_CHAT_ID)

WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "👋")
REPLY_TO_THIS_MESSAGE = os.getenv("REPLY_TO_THIS_MESSAGE", "REPLY_TO_THIS")
WRONG_REPLY = os.getenv("WRONG_REPLY", "WRONG_REPLY")