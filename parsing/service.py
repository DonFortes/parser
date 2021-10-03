import json
import os
from my_parser.settings import OBJECTS_COUNT, PAGES_TO_PARSE, REDEMPTION_VALUE, BOT_TOKEN, CHAT_ID, bot
import bs4
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from dotenv import load_dotenv

from parsing.models import Apartment, MarketPlace

load_dotenv()


class ScrapeClient:
    """Class for scraping."""

    def __init__(self, market: MarketPlace):
        self.market = market

    def scrape(self):
        """Takes objects from given url pages."""
        scraped_apartments = []
        scraping_count = 1
        while scraping_count <= PAGES_TO_PARSE:
            link = self.market.url + str(scraping_count)
            response = requests.get(link)
            html_soup = BeautifulSoup(response.text, "html.parser")
            apartment_data = html_soup.find_all(
                self.market.main_block_tag, self.market.main_block_class_name
            )

            if apartment_data:
                scraped_apartments.extend(apartment_data)
                # scaled_value = random.randint(2, 10)
                # time.sleep(scaled_value)
            else:
                break
            scraping_count += 1
        return scraped_apartments


class Parse:
    """Factory class for parsing sites."""

    def __init__(self, object_to_parse: bs4.element.Tag, market: MarketPlace):
        self.objects_count = OBJECTS_COUNT
        self.object_to_parse = object_to_parse
        self.market = market

    def parse(self):
        """Method for overriding in each subclass."""
        pass


class ParseAvito(Parse):
    """SubClass for parsing Avito."""

    def __init__(self, object_to_parse, market):
        super().__init__(object_to_parse, market)

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

                if title[0] != "Квартира-студия,":
                    index_of_area = 2
                else:
                    index_of_area = 1

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
                }
                return apartment_info


def get_or_create_avito():
    avito, _ = MarketPlace.objects.get_or_create(
        name="Avito",
        url="https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=",
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


def main(request):
    avito_tags = get_or_create_avito()  # MarketPlace object
    avito_client = ScrapeClient(
        avito_tags
    )  # list with BeautifulSoap objects from page.
    html_apartments = avito_client.scrape()

    for html_apartment in html_apartments:

        apartment_to_parse = ParseAvito(html_apartment, avito_tags)
        apartment = apartment_to_parse.parse()

        if apartment is not None:
            if Apartment.objects.filter(url=apartment["url"]).exists():
                continue

            apartment_obj = Apartment.objects.create(
                name=apartment["name"],
                url=apartment["url"],
                price=apartment["price"],
                total_area=apartment["total_area"],
                price_per_meter=apartment["price_per_meter"],
            )
            if apartment_obj.price_per_meter <= REDEMPTION_VALUE:
                message = f'Я нашел новый объект: {apartment["url"]}'
                bot.send_message(CHAT_ID, message)

    return HttpResponse("Nicely done")
