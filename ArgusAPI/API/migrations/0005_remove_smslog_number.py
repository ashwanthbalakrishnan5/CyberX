# Generated by Django 4.2.1 on 2023-05-13 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_calllog_number_alter_contacts_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smslog',
            name='number',
        ),
    ]
