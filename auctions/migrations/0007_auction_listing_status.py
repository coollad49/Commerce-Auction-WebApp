# Generated by Django 4.2.4 on 2023-12-25 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_listing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='status',
            field=models.CharField(default='OPEN', max_length=10),
        ),
    ]
