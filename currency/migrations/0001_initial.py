# Generated by Django 3.1.7 on 2021-04-27 03:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.PositiveSmallIntegerField(choices=[(1, 'USD'), (2, 'EUR')])),
                ('source', models.PositiveSmallIntegerField(choices=[(1, 'USD'), (2, 'EUR')])),
                ('buy', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sale', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
