import time

import schedule
from dotenv import load_dotenv

from my_parser.settings import AVITO_HEADERS, NOW_TIME, END_TIME
from parsing.service import Telegram, Avito
from django.core.management.base import BaseCommand

load_dotenv()


def start(marketplace):
    """Function, that starts our service."""

    while NOW_TIME <= END_TIME:
        marketplace.processing_market_place()
        # If you need to find object in price delta existing in database - uncomment this calling:
        # find_in_delta_price(telegram_client)
    return None


def scheduler():
    """A function that runs our service on a schedule at 09:00 (UTC+3) every day."""
    # return start()

    # Create the telegram client.
    telegram_client = Telegram()
    # Create Avito market place.
    avito = Avito(telegram_client, AVITO_HEADERS)

    if NOW_TIME < END_TIME:
        start(avito)
    else:
        schedule.every().day.at("10:00").do(start, marketplace=avito)

    while True:
        schedule.run_pending()
        time.sleep(1)


class Command(BaseCommand):
    help = 'Run parser'

    def handle(self, *args, **options):
        scheduler()
