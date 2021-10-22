# Generated by Django 3.2.7 on 2021-10-11 21:49
import json

from django.db import migrations


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
        main_block_class_name="iva-item-content-UnQQ4",
        price_tag="span",
        price_class=json.dumps(
            {"class": "price-text-E1Y7h text-text-LurtD text-size-s-BxGpL"}
        ),
        title_tag="h3",
        title_class=json.dumps(
            {
                "class": "title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title"
                "-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO"
            }
        ),
        url_tag="a",
        url_class=json.dumps(
            {
                "class": "link-link-MbQDP link-design-default-_nSbv title-root-j7cja iva-item"
                "-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes"
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