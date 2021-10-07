import json
import os
import random
import time
from datetime import datetime

import bs4
import loguru
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from dotenv import load_dotenv

from my_parser.settings import CHAT_ID, PAGES_TO_PARSE, REDEMPTION_VALUE, bot
from parsing.models import Apartment, MarketPlace, Phrase

load_dotenv()


class ScrapeClient:
    """Class for scraping."""

    def __init__(self, market: MarketPlace):
        self.market = market

    def scrape_page(self, scraping_count):
        """Takes objects from given url pages."""

        link = self.market.url + str(scraping_count)
        response = requests.get(link)

        if response.status_code != 200:
            bot.send_message(
                CHAT_ID,
                f"Парсер получил response с кодом {response.status_code}. Проверьте в чем дело.",
            )

        html_soup = BeautifulSoup(response.text, "html.parser")

        apartment_data = html_soup.find_all(
            self.market.main_block_tag, self.market.main_block_class_name
        )
        return apartment_data


class Parse:
    """Factory class for parsing sites."""

    def __init__(self, page_to_parse: bs4.element.Tag, market: MarketPlace):
        self.object_to_parse = page_to_parse
        self.market = market

    def parse(self):
        """Method for overriding in each subclass."""
        pass


class ParseAvito(Parse):
    """SubClass for parsing Avito."""

    def __init__(self, page_to_parse, market):
        super().__init__(page_to_parse, market)

    def parse(self):
        """Parses collected data from scraping sites and searches required info and objects."""

        cleaned_html = self.object_to_parse.find(
            self.market.price_tag, json.loads(self.market.price_class)
        )
        if cleaned_html is not None:
            text_only = cleaned_html.text
            text_only_no_currency_with_spaces = text_only.replace("₽", "")
            price = int("".join(text_only_no_currency_with_spaces.split()))
            title_obj = self.object_to_parse.find(
                self.market.title_tag, json.loads(self.market.title_class)
            )
            if title_obj is not None:
                title = title_obj.text.split()

                if title[0] == "Квартира-студия," or title[0] == "Апартаменты-студия,":
                    index_of_area = 1
                else:
                    index_of_area = 2

                total_area = float(title[index_of_area].replace(",", "."))
                url = self.object_to_parse.find(
                    self.market.url_tag, json.loads(self.market.url_class)
                )
                url = self.market.url_first_part + url.get("href")
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


def get_or_create_avito():
    """Get or create site Avito"""
    avito, _ = MarketPlace.objects.get_or_create(
        name="Avito",
        url="https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1&p=",
        main_block_tag="div",
        main_block_class_name="iva-item-content-UnQQ4",
        price_tag="span",
        price_class=json.dumps(
            {"class": "price-text-E1Y7h text-text-LurtD text-size-s-BxGpL"}
        ),
        title_tag="h3",
        title_class=json.dumps(
            {
                "class": "title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title"
                "-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO"
            }
        ),
        url_tag="a",
        url_class=json.dumps(
            {
                "class": "link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item"
                "-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes"
            }
        ),
        url_first_part="https://www.avito.ru",
    )
    return avito


def send_object_to_telegram(apartment, phrases):
    """Sending found object url with funny bot phrase to telegram."""
    random_phrase = random.choice(phrases)
    message = (
        f'{random_phrase.text} по цене {apartment["price_per_meter"]} за метр. '
        f'Смотри тут: {apartment["url"]}'
    )
    bot.send_message(CHAT_ID, message)
    time.sleep(3)


def count_of_all_apartments_with_low_price():
    """Count all apartments with redemption value or less."""
    apartments = (
        Apartment.objects.all().filter(price_per_meter__lte=REDEMPTION_VALUE).count()
    )
    return apartments


def get_phrases_queryset():
    """Get all phrases from database."""
    phrases = Phrase.objects.all()
    return phrases


def create_apartment_object(apartment):
    """Create Apartment-class object."""
    apartment_object = Apartment.objects.create(
        name=apartment["name"],
        url=apartment["url"],
        price=apartment["price"],
        total_area=apartment["total_area"],
        price_per_meter=apartment["price_per_meter"],
        time=datetime.now(),
    )
    return apartment_object


def processing_avito(phrases):
    """Makes all necessary processes to find apartments at Avito marketplace."""
    avito_tags = get_or_create_avito()
    avito_client = ScrapeClient(avito_tags)

    for page_number in range(1, PAGES_TO_PARSE):
        html_apartments = avito_client.scrape_page(page_number)

        if html_apartments:
            for html_apartment in html_apartments:
                apartment_to_parse = ParseAvito(html_apartment, avito_tags)
                apartment = apartment_to_parse.parse()

                if apartment is not None:
                    if Apartment.objects.filter(url=apartment["url"]).exists():
                        continue

                    apartment_object = create_apartment_object(apartment)
                    if apartment_object.price_per_meter <= REDEMPTION_VALUE:
                        send_object_to_telegram(apartment, phrases)
            time.sleep(5)
        else:
            bot.send_message(
                CHAT_ID,
                f"Парсер обошел {page_number} страниц. Больше ничего не найдено.",
            )
            break
    return HttpResponse("Nicely done")


def main(request):
    """Main function, that starts our service."""
    phrases = get_phrases_queryset()
    processing_avito(phrases)
