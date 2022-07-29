from asyncore import dispatcher
import logging

from telegram.ext import Updater

from handlers import setup_dispatcher
from settings import TELEGRAM_BOT_TOKEN

# Setup logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    # Setup bot handlers
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher = setup_dispatcher(dispatcher)

    # Run bot
    print('Bot has started!')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()