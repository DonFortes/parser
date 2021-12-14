from datetime import datetime

from parsing.models import Apartment, MarketPlace, Phrase


def get_or_create_apartment_object(apartment):
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


def get_apartment_from_base(apartment):
    """Get apartment from database by url."""
    apartment_in_base = Apartment.objects.get(url=apartment["url"])
    return apartment_in_base


def get_all_apartments():
    """Get all apartments."""
    all_apartments = Apartment.objects.all()
    return all_apartments


def delta_objects_count(old_min_value, new_max_value):
    object_count = Apartment.objects.filter(price__range=(old_min_value, new_max_value)).count()
    return object_count


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
