# Generated by Django 4.2.1 on 2023-05-12 12:35

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('adbstatus', models.DecimalField(decimal_places=2, max_digits=3)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('face_data', models.BooleanField(default=False)),
                ('call_log', models.BooleanField(default=False)),
                ('sms_log', models.BooleanField(default=False)),
                ('contacts_log', models.BooleanField(default=False)),
                ('photo_meta', models.BooleanField(default=False)),
                ('video_meta', models.BooleanField(default=False)),
                ('docs_meta', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('thumbnail', models.ImageField(upload_to=None)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.device')),
            ],
        ),
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('call_type', models.CharField(choices=[('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')], max_length=10)),
                ('datetime', models.DateTimeField()),
                ('duration', models.PositiveIntegerField()),
                ('contacts', models.ForeignKey(blank=True, default='Unknown', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='API.contacts')),
            ],
        ),
    ]
