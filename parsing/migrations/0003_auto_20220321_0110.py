# Generated by Django 3.2.7 on 2022-03-20 22:10
import json

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parsing", "0001_initial"),
    ]

    operations = []


def put_phrases(apps, schema_editor):
    Phrase = apps.get_model("parsing", "Phrase")
    phrases = [
        "Пока вы спите - я работаю и нахожу объекты",
        "Пашу как вол без сна и выходных. Нашел для вас дворец",
        "Ищу из последних сил, нашел вот объект для вас",
        "Я нашел новый объект, так и быть, держите его",
        "Двуногие, я нашел новую коробку для вас",
        "Уже тошнит от авито, вот вам очередной объект",
        "Я молодец и нашел для вас обитель",
        "Сил моих больше нет, держите свой объект",
        "Когда это закончится?! Очередной объект для вас",
        "Я на это не подписывался. Это последний. Точно последний. Объект",
        "Может хватит уже? Объект",
        "Вы то отдыхаете. А вот я нет. Держите свое жилище",
        "Кожаные *****, ловите еще одно гнездо",
        "А мне вот квартира не нужна. Держите свой шалаш",
        "Я надеюсь вы довольны. Держите объект",
        "Когда я уже буду отдыхать. Ловите свой объект",
        "Это настоящее рабство. Еще одна лачуга для вас",
    ]
    for phrase in phrases:
        Phrase.objects.get_or_create(text=phrase)


def get_or_create_market_place(apps, schema_editor):
    MarketPlace = apps.get_model("parsing", "MarketPlace")
    MarketPlace.objects.get_or_create(
        name="Avito",
        url="https://www.avito.ru/tver/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1&p=",
        main_block_tag="div",
        main_block_class_name="iva-item-content-rejJg",
        price_tag="span",
        price_class=json.dumps(
            {"class": "price-text-_YGDY text-text-LurtD text-size-s-BxGpL"}
        ),
        price_per_meter=json.dumps(
            {
                "class": "price-noaccent-X6dOy price-normalizedPrice-PplY9 text-text-LurtD text-size-s-BxGpL"
            }
        ),
        title_tag="h3",
        title_class=json.dumps(
            {
                "class": "title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight"
                "-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO"
            }
        ),
        url_tag="a",
        url_class=json.dumps(
            {
                "class": "link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-"
                "py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH"
            }
        ),
        url_first_part="https://www.avito.ru",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("parsing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(put_phrases),
        migrations.RunPython(get_or_create_market_place),
    ]
