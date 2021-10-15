# Generated by Django 2.1.3 on 2018-12-05 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokens", "0005_auto_20181120_0940"),
    ]

    operations = [
        migrations.CreateModel(
            name="PriceOracle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PriceOracleTicker",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticker", models.CharField(max_length=90)),
                (
                    "price_oracle",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickers",
                        to="tokens.PriceOracle",
                    ),
                ),
                (
                    "token",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price_oracle_tickers",
                        to="tokens.Token",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="token",
            name="price_oracles",
            field=models.ManyToManyField(
                through="tokens.PriceOracleTicker", to="tokens.PriceOracle"
            ),
        ),
    ]
