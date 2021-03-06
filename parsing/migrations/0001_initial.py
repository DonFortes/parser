# Generated by Django 3.2.7 on 2021-10-11 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Apartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Заголовок объявления"
                    ),
                ),
                (
                    "url",
                    models.URLField(unique=True, verbose_name="Ссылка на площадку"),
                ),
                (
                    "price",
                    models.PositiveIntegerField(verbose_name="Стоимость квартиры"),
                ),
                (
                    "total_area",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Общая площадь"
                    ),
                ),
                (
                    "price_per_meter",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена за метр"
                    ),
                ),
                ("time", models.TimeField()),
            ],
            options={
                "verbose_name": "Объект недвижимости",
                "verbose_name_plural": "Объекты недвижимости",
            },
        ),
        migrations.CreateModel(
            name="MarketPlace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Имя площадки объявлений"
                    ),
                ),
                ("url", models.URLField(verbose_name="Ссылка на площадку")),
                (
                    "main_block_tag",
                    models.CharField(max_length=255, verbose_name="Тэг главного блока"),
                ),
                (
                    "main_block_class_name",
                    models.CharField(
                        max_length=255, verbose_name="Класс главного блока"
                    ),
                ),
                (
                    "price_tag",
                    models.CharField(max_length=255, verbose_name="Тэг блока цены"),
                ),
                (
                    "price_class",
                    models.CharField(max_length=255, verbose_name="Класс блока цены"),
                ),
                (
                    "title_tag",
                    models.CharField(
                        max_length=255, verbose_name="Класс блока заголовка"
                    ),
                ),
                (
                    "title_class",
                    models.CharField(
                        max_length=255, verbose_name="Класс блока заголовка"
                    ),
                ),
                (
                    "url_tag",
                    models.CharField(max_length=255, verbose_name="Класс блока ссылки"),
                ),
                (
                    "url_class",
                    models.CharField(max_length=255, verbose_name="Класс блока ссылки"),
                ),
                (
                    "url_first_part",
                    models.CharField(
                        max_length=255, verbose_name="Неизменяемая первая часть ссылки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Площадка объявлений",
                "verbose_name_plural": "Площадки объявлений",
            },
        ),
        migrations.CreateModel(
            name="Phrase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(max_length=255, verbose_name="Фразы парсера"),
                ),
            ],
            options={
                "verbose_name": "фразу парсера",
                "verbose_name_plural": "фразы парсера",
            },
        ),
    ]
