import datetime as dt
import time

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from my_parser.settings import AVITO_HEADERS
from parsing.service import Avito, Telegram

load_dotenv()


def its_time_to_run():
    now_time = dt.datetime.now().time()
    stop_time_1 = dt.time(22, 0, 0)
    stop_time_2 = dt.time(23, 59, 59)
    stop_time_3 = dt.time(0, 0, 0)
    stop_time_4 = dt.time(10, 0, 0)

    if stop_time_1 <= now_time <= stop_time_2 or stop_time_3 <= now_time < stop_time_4:
        action = False
    else:
        action = True
    return action


def start():
    """Function, that starts our service."""

    # Create the telegram client.
    telegram_client = Telegram()
    # Create Avito market place.
    avito = Avito(telegram_client, AVITO_HEADERS)
    while True:
        if its_time_to_run():
            avito.processing_market_place()
        else:
            time.sleep(60)
        # If you need to find object in price delta existing in database - uncomment this calling:
        # find_in_delta_price(telegram_client)
        return None


class Command(BaseCommand):
    help = "Run parser"

    def handle(self, *args, **options):
        start()
