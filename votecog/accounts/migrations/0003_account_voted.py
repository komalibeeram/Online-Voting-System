# Generated by Django 3.1 on 2020-11-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_person_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='voted',
            field=models.CharField(default='no', max_length=30),
        ),
    ]
