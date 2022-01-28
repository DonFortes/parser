import datetime as dt
import time

import loguru
import schedule
from django.http import HttpResponse
from dotenv import load_dotenv

from my_parser.settings import AVITO_HEADERS
from parsing.service import Telegram, Avito
from django.core.management.base import BaseCommand, CommandError

load_dotenv()


def start(marketplace):
    """Function, that starts our service."""

    now_time = dt.datetime.now().time()
    end_time = dt.time(22, 0, 0)

    while now_time <= end_time:
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
    schedule.every().day.at("08:00").do(start, marketplace=avito)

    while True:
        schedule.run_pending()
        time.sleep(1)


class Command(BaseCommand):
    help = 'Run parser'

    def handle(self, *args, **options):
        scheduler()
