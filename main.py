import random

from bs4 import BeautifulSoup
from requests import get
import time


def scraping(link, tag, class_name):
    """Takes objects from given url pages."""
    scraping_apartments = []
    scraping_count = 1

    while scraping_count <= 1:
        link = link + str(scraping_count)
        response = get(link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        apartment_data = html_soup.find_all(tag, class_name)

        if apartment_data:
            scraping_apartments.extend(apartment_data)
            # scaled_value = random.randint(100, 1000)
            # scaled_value = 1 + (value * (9 - 5))
            # time.sleep(scaled_value)
        else:
            print('empty')
            break
        scraping_count += 1

    return scraping_apartments


def parsing():
    """Parses taken data from scraping sites and searches needed info and objects."""
    for url in sites:
        apartments = scraping(sites[url]['link'], sites[url]['tag'], sites[url]['class_name'])

    count = 0
    while count <= 5:
        try:
            info = apartments[count]
        except IndexError:
            break

        for tag in tags_for_searching_data:
            price = int(''.join(
                info.find(tags_for_searching_data[tag]['tag_for_price'],
                          tags_for_searching_data[tag]['class_for_price']).text.replace('₽', '').split()))
            title = info.find(tags_for_searching_data[tag]['tag_for_title'],
                              tags_for_searching_data[tag]['class_for_title']).text.split()
            square = float(title[2].replace(',', '.'))
            price_per_meter = price / square

            print(price)
            print(square)
            print(price_per_meter)
        count += 1


if __name__ == '__main__':

    sites = {
        'avito': {
            'link': 'https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=',
            'tag': 'div',
            'class_name': 'iva-item-content-UnQQ4'
        }, }

    tags_for_searching_data = {
        'avito': {
            'tag_for_price': 'span',
            'class_for_price': {'class': 'price-text-E1Y7h text-text-LurtD text-size-s-BxGpL'},
            'tag_for_title': 'h3',
            'class_for_title': {
                'class': 'title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title'
                         '-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO'},
        }, }
