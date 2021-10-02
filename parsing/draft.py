import logging
import random
import time

from bs4 import BeautifulSoup
from requests import get
from loguru import logger

OBJECTS_COUNT = 5
PAGES_TO_PARSE = 1


def scrape(link, tag, class_name):
    """Takes objects from given url pages."""
    scraped_apartments = []
    scraping_count = 1
    while scraping_count <= PAGES_TO_PARSE:
        link = link + str(scraping_count)
        response = get(link)
        html_soup = BeautifulSoup(response.text, "html.parser")
        apartment_data = html_soup.find_all(tag, class_name)

        if apartment_data:
            scraped_apartments.extend(apartment_data)
            # scaled_value = random.randint(2, 10)
            # time.sleep(scaled_value)
        else:
            break
        scraping_count += 1
    logger.debug(len(scraped_apartments))
    return scraped_apartments


def parse():
    """Parses taken data from scraping sites and searches needed info and objects."""
    for info in all_apartments:
        logger.debug(type(info))
        for site in sites_and_necessary_blocks:
            logger.debug(sites_and_necessary_blocks[site]["tag_for_price"])
            logger.debug(type(sites_and_necessary_blocks[site]["class_for_price"]))
            price = int(
                "".join(
                    info.find(
                        sites_and_necessary_blocks[site]["tag_for_price"],
                        sites_and_necessary_blocks[site]["class_for_price"],
                    )
                    .text.replace("₽", "")
                    .split()
                )
            )

            title_obj = info.find(
                sites_and_necessary_blocks[site]["tag_for_title"],
                sites_and_necessary_blocks[site]["class_for_title"],
            )
            if title_obj is not None:
                title = title_obj.text.split()
                logger.debug(title)
                if title[0] != "Квартира-студия,":
                    index_of_area = 2
                else:
                    index_of_area = 1
                square = float(title[index_of_area].replace(",", "."))
                link = info.find(
                    sites_and_necessary_blocks[site]["tag_for_url"],
                    sites_and_necessary_blocks[site]["class_for_url"],
                )
                link = sites_and_necessary_blocks[site]["first_part_of_url"] + link.get(
                    "href"
                )
                price_per_meter = int(price / square)

                # print(price)
                # print(square)
                # print(price_per_meter)
                # print(link)
            else:
                logger.debug("WTF")


if __name__ == "__main__":

    sites_and_necessary_blocks = {
        "avito": {
            "link": "https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=",
            "tag": "div",
            "class_name": "iva-item-content-UnQQ4",
            "tag_for_price": "span",
            "class_for_price": {
                "class": "price-text-E1Y7h text-text-LurtD text-size-s-BxGpL"
            },
            "tag_for_title": "h3",
            "class_for_title": {
                "class": "title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title"
                "-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO"
            },
            "tag_for_url": "a",
            "class_for_url": {
                "class": "link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item"
                "-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes"
            },
            "first_part_of_url": "https://www.avito.ru",
        },
    }

    for url in sites_and_necessary_blocks:
        all_apartments = scrape(
            sites_and_necessary_blocks[url]["link"],
            sites_and_necessary_blocks[url]["tag"],
            sites_and_necessary_blocks[url]["class_name"],
        )
    parse()
