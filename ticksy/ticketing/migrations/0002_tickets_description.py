# Generated by Django 4.0.3 on 2022-04-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='description',
            field=models.TextField(default='empty'),
        ),
    ]