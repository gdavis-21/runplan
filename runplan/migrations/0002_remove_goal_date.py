# Generated by Django 4.2.3 on 2023-07-22 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runplan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='date',
        ),
    ]