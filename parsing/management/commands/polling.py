import datetime as dt
from distutils.log import debug
import random
import time
from loguru import logger
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from my_parser.settings import AVITO_HEADERS
from parsing.service import Avito, Telegram

load_dotenv()


def its_time_to_run():
    now_time = dt.datetime.now().time()
    random_minute = random.randint(0, 59)
    start_time = dt.time(10, random_minute, 0)
    stop_time = dt.time(21, random_minute, 0)

    if start_time <= now_time <= stop_time:
        action = True
    else:
        action = False
    return action


def start():
    """Function, that starts our service."""

    # Create the telegram client.
    telegram_client = Telegram()
    # Create Avito market place.
    avito = Avito(telegram_client, AVITO_HEADERS)
    while True:
        if its_time_to_run():
            logger.debug('Работаем!')
            avito.processing_market_place()
        else:
            logger.debug('Ждем начала рабочего дня')
            time.sleep(60)
        # If you need to find object in price delta existing in database - uncomment this calling:
        # find_in_delta_price(telegram_client)


class Command(BaseCommand):
    help = "Run parser"

    def handle(self, *args, **options):
        start()
