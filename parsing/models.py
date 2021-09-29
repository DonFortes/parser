from django.db import models


class MarketPlace(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Имя площадки объявлений')
    url = models.URLField(verbose_name='Ссылка на площадку')
    main_block_tag = models.CharField(
        max_length=255, verbose_name='Тэг главного блока')
    main_block_class_name = models.CharField(
        max_length=255, verbose_name='Класс главного блока')
    price_tag = models.CharField(
        max_length=255, verbose_name='Тэг блока цены')
    price_class = models.CharField(
        max_length=255, verbose_name='Класс блока цены')
    title_tag = models.CharField(
        max_length=255, verbose_name='Класс блока заголовка')
    title_class = models.CharField(
        max_length=255, verbose_name='Класс блока заголовка')
    url_tag = models.CharField(
        max_length=255, verbose_name='Класс блока ссылки')
    url_class = models.CharField(
        max_length=255, verbose_name='Класс блока ссылки')
    url_first_part = models.CharField(
        max_length=255, verbose_name='Неизменяемая первая часть ссылки')

    class Meta:
        verbose_name = 'Площадка объявлений'
        verbose_name_plural = 'Площадки объявлений'

    def __srt__(self):
        return f'Рекламная площадка {self.name}'


class Apartment(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Заголовок объявления')
    url = models.URLField(verbose_name='Ссылка на площадку')
    price = models.PositiveIntegerField(
        verbose_name='Стоимость квартиры'
    )
    total_area = models.DecimalField()
    price_per_meter = models.DecimalField()
