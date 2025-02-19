# Generated by Django 2.2.1 on 2019-10-04 11:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addres', models.CharField(max_length=250)),
                ('area', models.IntegerField()),
                ('is_living', models.BooleanField()),
                ('owner_uuid', models.UUIDField()),
                ('prop_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
