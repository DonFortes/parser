import random
import time

from bs4 import BeautifulSoup
from models import Apartment, MarketPlace
from requests import get

OBJECTS_COUNT = 5
PAGES_TO_PARSE = 1


class Site:
    def __init__(self, url):
        pass


class ScrapeClient:
    """Takes needed info from given url pages."""

    def __init__(self, url, tag, class_name):
        pass


class Parse:
    """Parses taken data from scraping sites and searches needed info and objects."""
    pass


class Apartment:
    pass


def scrape(link, tag, class_name):
    """Takes objects from given url pages."""
    scraped_apartments = []
    scraping_count = 1
    while scraping_count <= PAGES_TO_PARSE:
        link = link + str(scraping_count)
        response = get(link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        apartment_data = html_soup.find_all(tag, class_name)

        if apartment_data:
            scraped_apartments.extend(apartment_data)
            # scaled_value = random.randint(2, 10)
            # time.sleep(scaled_value)
        else:
            break
        scraping_count += 1
    return scraped_apartments


def parse():
    """Parses taken data from scraping sites and searches needed info and objects."""
    count = 0
    for _ in range(OBJECTS_COUNT):
        try:
            info = all_apartments[count]
        except IndexError:
            break

        for site in sites_and_necessary_blocks:
            price = int(''.join(
                info.find(sites_and_necessary_blocks[site]['tag_for_price'],
                          sites_and_necessary_blocks[site]['class_for_price']).text.replace('₽', '').split()))
            title = info.find(sites_and_necessary_blocks[site]['tag_for_title'],
                              sites_and_necessary_blocks[site]['class_for_title']).text.split()
            square = float(title[2].replace(',', '.'))
            link = info.find(sites_and_necessary_blocks[site]['tag_for_url'],
                             sites_and_necessary_blocks[site]['class_for_url'])
            link = sites_and_necessary_blocks[site]['first_part_of_url'] + link.get('href')
            price_per_meter = int(price / square)

            print(price)
            print(square)
            print(price_per_meter)
            print(link)


if __name__ == '__main__':

    sites_and_necessary_blocks = {
        'avito': {
            'link': 'https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=',
            'tag': 'div',
            'class_name': 'iva-item-content-UnQQ4',
            'tag_for_price': 'span',
            'class_for_price': {'class': 'price-text-E1Y7h text-text-LurtD text-size-s-BxGpL'},
            'tag_for_title': 'h3',
            'class_for_title': {
                'class': 'title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title'
                         '-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO'},
            'tag_for_url': 'a',
            'class_for_url': {
                'class': 'link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item'
                         '-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes'},
            'first_part_of_url': 'https://www.avito.ru'
        }, }

    for url in sites_and_necessary_blocks:
        all_apartments = scrape(sites_and_necessary_blocks[url]['link'], sites_and_necessary_blocks[url]['tag'],
                                sites_and_necessary_blocks[url]['class_name'])
    parse()
