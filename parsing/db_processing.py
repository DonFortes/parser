from datetime import datetime

from my_parser.settings import logger_new
from parsing.models import Apartment, MarketPlace, Phrase


def get_or_create_apartment_object(apartment):
    """Create Apartment-class object. Get or create for additional duplicate resistance."""
    apartment_object = Apartment.objects.get_or_create(
        name=apartment["name"],
        url=apartment["url"],
        price=apartment["price"],
        total_area=apartment["total_area"],
        price_per_meter=apartment["price_per_meter"],
        time=datetime.now(),
    )
    return apartment_object


def get_apartment_from_base(apartment):
    """Get apartment from database by url."""
    apartment_id = None
    if "avito" in apartment['url']:
        apartment_id = apartment['url'][-10:-1]
    # Add here a new type of market if necessary with elif construction
    apartment_in_base = Apartment.objects.get(url__contains=apartment_id)
    return apartment_in_base


def get_all_apartments():
    """Get all apartments."""
    all_apartments = Apartment.objects.all()
    return all_apartments


def get_market_place_object(name):
    """Get marketplace object by name."""
    market_place = MarketPlace.objects.get(name=name)
    return market_place


def get_all_phrases():
    """Get all phrases."""
    phrases = Phrase.objects.all()
    return phrases


def save_new_data_for(apartment_in_base):
    """Save new data for apartment is base."""
    apartment_in_base.save()
    return None
