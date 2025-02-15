# Generated by Django 4.2.1 on 2023-05-13 15:17

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_calllog_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calllog',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+91', max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+91', max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='smslog',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+91', max_length=128, region=None),
        ),
    ]
