# Generated by Django 2.0.2 on 2020-01-16 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0010_apiautomationcoverage'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiautomationcoverage',
            name='num',
            field=models.IntegerField(default=0, verbose_name='关联数量'),
        ),
    ]
