import datetime as dt
import http
import json
import random
import time

import bs4
import loguru
import requests
import schedule
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from dotenv import load_dotenv

from my_parser.settings import (AVITO_HEADERS, CHAT_ID, NEW_MAX_VALUE,
                                OLD_MIN_VALUE, PAGES_TO_PARSE,
                                REDEMPTION_VALUE, bot)
from parsing.db_processing import (get_all_apartments,
                                   get_all_phrases, get_apartment_from_base,
                                   get_market_place_object,
                                   get_or_create_apartment_object,
                                   save_new_data_for)
from parsing.models import MarketPlace

load_dotenv()


class ScrapeClient:
    """Class for scraping."""

    def __init__(self, marketplace_tags: MarketPlace, telegram_client):
        self.market_tags = marketplace_tags
        self.telegram_client = telegram_client

    def scrape_page(self, page_number, market):
        """Takes objects from given url pages."""
        link = self.market_tags.url + str(page_number)
        loguru.logger.debug(f"Смотрю {page_number} страницу.")

        headers = market.make_dynamic_headers(link)
        loguru.logger.debug(headers)
        try:
            with requests.get(link, headers=headers) as response:
                loguru.logger.debug(response.status_code)
                if response.status_code != 200:
                    self.telegram_client.send_message_with_error(response.status_code)
                html_soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.ConnectionError:
            start()

        apartment_data = html_soup.find_all(
            self.market_tags.main_block_tag, self.market_tags.main_block_class_name
        )
        return apartment_data


class MarketPlaceProcessing:
    """Factory class to work with each market place."""

    def __init__(self, telegram_client, headers):
        self.telegram_client = telegram_client
        self.marketplace_tags = None
        self.headers = headers

    def parse(self, page_to_parse: bs4.element.Tag, market: MarketPlace):
        """Method for overriding in each subclass."""
        pass

    def make_headers(self, link):
        """Method for overriding in each subclass."""
        pass

    def processing_market_place(self, market):
        """Makes all necessary processes to find apartments at each marketplace."""
        scrape_client = ScrapeClient(self.marketplace_tags, self.telegram_client)
        for page_number in range(1, PAGES_TO_PARSE + 1):
            html_apartments = scrape_client.scrape_page(page_number, market)

            if html_apartments:
                for html_apartment in html_apartments:
                    apartment = self.parse(html_apartment, self.marketplace_tags)

                    if apartment is not None:
                        try:
                            apartment_in_base = get_apartment_from_base(apartment)
                        except ObjectDoesNotExist:
                            get_or_create_apartment_object(apartment)
                            if apartment["price_per_meter"] <= REDEMPTION_VALUE:
                                self.telegram_client.send_message_with_new_object(
                                    apartment
                                )
                        else:
                            if (
                                apartment_in_base.price_per_meter
                                == apartment["price_per_meter"]
                            ):
                                continue
                            else:
                                price_difference = (
                                    apartment["price_per_meter"]
                                    - apartment_in_base.price_per_meter
                                )
                                apartment_in_base.price_per_meter = apartment[
                                    "price_per_meter"
                                ]
                                save_new_data_for(apartment_in_base)
                                if apartment["price_per_meter"] <= REDEMPTION_VALUE:
                                    self.telegram_client.send_message_with_existing_object(
                                        apartment, price_difference
                                    )
                time.sleep(random.randint(37, 62))
            else:
                self.telegram_client.send_final_message_with(page_number)
                break


class Avito(MarketPlaceProcessing):
    """Class that encapsulates all work with Avito site."""

    def __init__(self, telegram_client, headers):
        super().__init__(telegram_client, headers)
        self.marketplace_tags = get_market_place_object("Avito")

    def make_dynamic_headers(self, link):
        """Create a 'referer' header to avito."""
        upd = {"referer": link}
        self.headers.update(upd)
        # self.session.headers = {}
        return self.headers

    def parse(self, page_to_parse: bs4.element.Tag, market: MarketPlace):
        """Parses collected data from Avito and searches required info and objects."""

        cleaned_html = page_to_parse.find(
            market.price_tag, json.loads(market.price_class)
        )
        if cleaned_html is not None:
            text_only = cleaned_html.text
            text_only_no_currency_with_spaces = text_only.replace("₽", "")
            price = int("".join(text_only_no_currency_with_spaces.split()))
            title_obj = page_to_parse.find(
                market.title_tag, json.loads(market.title_class)
            )
            if title_obj is not None:
                title = title_obj.text.split()

                if title[0] == "Квартира-студия," or title[0] == "Апартаменты-студия,":
                    index_of_area = 1
                else:
                    index_of_area = 2

                total_area = float(title[index_of_area].replace(",", "."))
                url = page_to_parse.find(market.url_tag, json.loads(market.url_class))
                url = market.url_first_part + url.get("href")
                price_per_meter = int(price / total_area)
                loguru.logger.debug(price_per_meter)
                offset = dt.timezone(dt.timedelta(hours=3))
                apartment_info = {
                    "name": title,
                    "url": url,
                    "price": price,
                    "total_area": total_area,
                    "price_per_meter": price_per_meter,
                    "time": dt.datetime.now(offset),
                }
                return apartment_info


class Telegram:
    """Class that resolves sending different messages to telegram."""

    def __init__(self):
        self.phrases = get_all_phrases()
        self.chat_id = CHAT_ID

    def send_prepared_message(self, message):
        """Sends message and wait for 3 seconds."""
        bot.send_message(self.chat_id, message)
        time.sleep(3)

    def send_message_with_new_object(self, apartment):
        """Sends found object url with funny bot phrase to telegram."""
        random_phrase = random.choice(self.phrases)
        message = (
            f"{random_phrase.text} по цене {apartment['price_per_meter']}₽ за метр. "
            f"Смотри тут: {apartment['url']}"
        )
        return self.send_prepared_message(message)

    def send_message_with_existing_object(self, apartment, difference):
        """Sends existing object url with changed price per meter to telegram."""
        message = (
            f"Этот объект уже был в нашей базе. Его цена за метр изменилась на {difference}₽ "
            f"и стала {apartment['price_per_meter']}₽ за метр. "
            f"Смотри тут: {apartment['url']}"
        )
        return self.send_prepared_message(message)

    def send_message_with_error(self, error_code):
        """Sends a message with error."""
        message = f"Парсер получил response с кодом {error_code}. Проверьте в чем дело."
        return self.send_prepared_message(message)

    def send_final_message_with(self, page_number):
        """Sends a message after work."""
        message = f"Парсер обошел {page_number} страниц. Больше ничего не найдено."
        return self.send_prepared_message(message)


def find_in_delta_price(telegram_client):
    """Finds an object that already exists in the database with a delta price."""
    delta_objects = (
        obj
        for obj in get_all_apartments()
        if OLD_MIN_VALUE < obj.price_per_meter < NEW_MAX_VALUE
    )
    for obj in delta_objects:
        price = obj.price_per_meter
        url = obj.url
        message = f"Дельта-объект с ценой {price}₽ за метр. Этот объект уже был. Смотри тут: {url}"
        telegram_client.send_prepared_message(message)
        delta_objects.__next__()


def start():
    """Function, that starts our service."""

    now_time = dt.datetime.now().time()
    start_stop_time = dt.time(22, 0, 0)
    end_stop_time = dt.time(23, 59, 0)

    if start_stop_time < now_time < end_stop_time:
        return HttpResponse("Enough for today...")
    else:
        # Create the telegram client.
        telegram_client = Telegram()
        # Create Avito market place.
        avito = Avito(telegram_client, AVITO_HEADERS)
        # Processing Avito with Avito headers.
        avito.processing_market_place(avito)

        # If you need to find object in price delta existing in database - uncomment this calling:
        # find_in_delta_price(telegram_client)

        return start()


def main(request):
    """A function that runs our service on a schedule at 09:00 (UTC+3) every day."""
    schedule.every().day.at("06:00").do(start)

    while True:
        schedule.run_pending()
        time.sleep(1)
