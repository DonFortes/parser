import json
import random
import time
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from dotenv import load_dotenv

from my_parser.settings import CHAT_ID, PAGES_TO_PARSE, REDEMPTION_VALUE, OLD_MIN_VALUE, NEW_MAX_VALUE, bot
from parsing.models import Apartment, MarketPlace, Phrase

load_dotenv()


class ScrapeClient:
    """Class for scraping."""

    def __init__(self, market: MarketPlace, telegram_client):
        self.market = market
        self.telegram_client = telegram_client

    def scrape_page(self, scraping_count):
        """Takes objects from given url pages."""
        link = self.market.url + str(scraping_count)
        with requests.get(link) as response:
            if response.status_code != 200:
                self.telegram_client.send_message_with_error(response.status_code)

            html_soup = BeautifulSoup(response.text, "html.parser")

            apartment_data = html_soup.find_all(
                self.market.main_block_tag, self.market.main_block_class_name
            )
            return apartment_data


class MarketPlaceProcessing:
    """Factory class to work with each market place."""

    def __init__(self, telegram_client):
        self.telegram_client = telegram_client
        self.tags = None
        """Method for overriding in each subclass."""

    def parse(self, page_to_parse: bs4.element.Tag, market: MarketPlace):
        """Method for overriding in each subclass."""
        pass

    def processing_market_place(self):
        """Makes all necessary processes to find apartments at each marketplace."""
        avito_scrape_client = ScrapeClient(self.tags, self.telegram_client)

        for page_number in range(1, PAGES_TO_PARSE):
            html_apartments = avito_scrape_client.scrape_page(page_number)

            if html_apartments:
                for html_apartment in html_apartments:
                    apartment = self.parse(html_apartment, self.tags)

                    if apartment is not None:
                        if Apartment.objects.filter(url=apartment["url"]).exists():
                            apartment_in_base = Apartment.objects.get(
                                url=apartment["url"]
                            )

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
                                apartment_in_base.save()
                                if apartment["price_per_meter"] <= REDEMPTION_VALUE:
                                    self.telegram_client.send_message_with_existing_object(
                                        apartment, price_difference
                                    )

                        else:
                            self.get_or_create_apartment_object(apartment)
                            if apartment["price_per_meter"] <= REDEMPTION_VALUE:
                                self.telegram_client.send_message_with_new_object(
                                    apartment
                                )
                time.sleep(6)
            else:
                self.telegram_client.send_final_message_with(page_number)
                break

    def get_or_create_apartment_object(self, apartment):
        """Create Apartment-class object."""
        apartment_object = Apartment.objects.get_or_create(
            name=apartment["name"],
            url=apartment["url"],
            price=apartment["price"],
            total_area=apartment["total_area"],
            price_per_meter=apartment["price_per_meter"],
            time=datetime.now(),
        )
        return apartment_object


class Avito(MarketPlaceProcessing):
    """Class that encapsulates all work with Avito site."""

    def __init__(self, telegram_client):
        super().__init__(telegram_client)
        self.tags = MarketPlace.objects.get(name="Avito")

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
                apartment_info = {
                    "name": title,
                    "url": url,
                    "price": price,
                    "total_area": total_area,
                    "price_per_meter": price_per_meter,
                    "time": datetime.now(),
                }
                return apartment_info


class Telegram:
    """Class that resolves sending different messages to telegram."""

    def __init__(self):
        self.phrases = self.get_phrases_queryset()
        self.chat_id = CHAT_ID

    def get_phrases_queryset(self):
        """Get all phrases from database."""
        phrases = Phrase.objects.all()
        return phrases

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
    delta_objects = (obj for obj in Apartment.objects.all() if OLD_MIN_VALUE < obj.price_per_meter < NEW_MAX_VALUE)
    for obj in delta_objects:
        price = obj.price_per_meter
        url = obj.url
        message = f'Дельта-объект с ценой {price}₽ за метр. Этот объект уже был. Смотри тут: {url}'
        telegram_client.send_prepared_message(message)
        delta_objects.__next__()


def main(request):
    """Main function, that starts our service."""
    # Create the telegram client.
    telegram_client = Telegram()
    # Create Avito market place.
    avito = Avito(telegram_client)
    # Processing Avito.
    avito.processing_market_place()

    # If you need to find object in price delta existing in database - uncomment this calling.
    # find_in_delta_price(telegram_client)

    return HttpResponse("Nicely done")
