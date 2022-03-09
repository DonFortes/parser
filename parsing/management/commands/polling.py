import datetime as dt
import random
import time

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from my_parser.settings import AVITO_HEADERS, START_HOUR, STOP_HOUR, logger_new
from parsing.service import Avito, Telegram, find_in_delta_price

load_dotenv()


def its_time_to_run():
    now_time = dt.datetime.now().time()
    random_minute = random.randint(0, 59)
    start_time = dt.time(START_HOUR, random_minute, 0)
    stop_time = dt.time(STOP_HOUR, 0, 0)
    logger_new.debug(f"now_time: {now_time}")
    logger_new.debug(f"random_minute: {random_minute}")
    force_start = False

    if start_time <= now_time <= stop_time or force_start:
        return True
    return False


def start():
    """Function, that starts our service."""

    # Create the telegram client.
    telegram_client = Telegram()
    # Create Avito market place.
    avito = Avito(telegram_client, AVITO_HEADERS)

    # If you need to find objects in delta price existing in database - uncomment calling
    # below and comment avito.processing_market_place() below in while loop:
    #
    # find_in_delta_price(telegram_client)

    while True:
        if its_time_to_run():
            logger_new.debug("Работаем!")
            avito.processing_market_place()
        else:
            logger_new.debug("Ждем начала рабочего дня")
            time.sleep(60)


class Command(BaseCommand):
    help = "Run parser"

    def handle(self, *args, **options):
        start()
