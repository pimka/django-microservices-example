# Generated by Django 2.2.1 on 2019-11-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
