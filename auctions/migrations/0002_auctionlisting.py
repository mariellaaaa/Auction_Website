# Generated by Django 5.0.1 on 2024-05-20 10:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('category', models.CharField(blank=True, choices=[('FASHION', 'Fashion'), ('TOYS', 'Toys'), ('ELECTRONICS', 'Electronics'), ('HOME', 'Home'), ('AUTOMOBILES', 'Automobiles'), ('BOOKS', 'Books'), ('ART', 'Art'), ('SPORT', 'Sport'), ('JEWERLY', 'Jewerly'), ('HANDMADE', 'Handmade')], max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
