# Generated by Django 2.2.1 on 2019-10-16 09:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('R', 'Rent'), ('P', 'Purchase'), ('S', 'Sale')], default='R', max_length=20)),
                ('customer_uuid', models.UUIDField()),
                ('price', models.IntegerField()),
                ('prop_uuid', models.UUIDField()),
                ('order_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
