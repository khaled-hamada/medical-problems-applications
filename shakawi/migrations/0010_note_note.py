# Generated by Django 3.0.2 on 2021-02-11 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shakawi', '0009_auto_20210211_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
