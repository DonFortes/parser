from django.db import models


class MarketPlace(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя площадки объявлений")
    url = models.URLField(verbose_name="Ссылка на площадку")
    main_block_tag = models.CharField(max_length=255, verbose_name="Тэг главного блока")
    main_block_class_name = models.CharField(
        max_length=255, verbose_name="Класс главного блока"
    )
    price_tag = models.CharField(max_length=255, verbose_name="Тэг блока цены")
    price_class = models.CharField(max_length=255, verbose_name="Класс блока цены")
    price_per_meter = models.CharField(
        max_length=255, verbose_name="Класс блока цены за метр"
    )
    title_tag = models.CharField(max_length=255, verbose_name="Класс блока заголовка")
    title_class = models.CharField(max_length=255, verbose_name="Класс блока заголовка")
    url_tag = models.CharField(max_length=255, verbose_name="Класс блока ссылки")
    url_class = models.CharField(max_length=255, verbose_name="Класс блока ссылки")
    url_first_part = models.CharField(
        max_length=255, verbose_name="Неизменяемая первая часть ссылки"
    )

    class Meta:
        verbose_name = "Площадка объявлений"
        verbose_name_plural = "Площадки объявлений"

    def __srt__(self):
        return f"Рекламная площадка {self.name}"


class Apartment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Заголовок объявления")
    url = models.URLField(unique=True, verbose_name="Ссылка на площадку")
    price = models.PositiveIntegerField(verbose_name="Стоимость квартиры")
    total_area = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая площадь"
    )
    price_per_meter = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за метр"
    )
    time = models.TimeField()

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"

    def __srt__(self):
        return f"Объект: {self.name}"


class Phrase(models.Model):
    text = models.CharField(max_length=255, verbose_name="Фразы парсера")

    class Meta:
        verbose_name = "фразу парсера"
        verbose_name_plural = "фразы парсера"

    def __srt__(self):
        return f"Фраза: {self.text}"
