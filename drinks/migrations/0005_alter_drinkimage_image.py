# Generated by Django 4.2.7 on 2023-12-25 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0004_alter_drink_options_drinkimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='drinks'),
        ),
    ]
