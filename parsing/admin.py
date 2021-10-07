from django.contrib import admin

from .models import Apartment, MarketPlace, Phrase

admin.site.register(MarketPlace)
admin.site.register(Apartment)
admin.site.register(Phrase)
