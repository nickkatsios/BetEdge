# Generated by Django 4.2.4 on 2023-08-15 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ArbBackend", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArbitrageOutcomes",
            fields=[
                ("outcome_id", models.AutoField(primary_key=True, serialize=False)),
                ("outcome_title", models.CharField(max_length=255)),
                ("outcome_odds", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "db_table": "Arbitrage",
                "managed": False,
            },
        ),
    ]
