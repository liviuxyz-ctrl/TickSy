# Generated by Django 4.0.3 on 2022-04-15 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_alter_employeesprivatedata_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='finish_at',
            field=models.DateTimeField(null=True),
        ),
    ]