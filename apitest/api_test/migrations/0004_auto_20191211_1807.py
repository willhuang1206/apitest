# Generated by Django 2.0.2 on 2019-12-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0003_auto_20191210_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='automationtask',
            name='automation',
        ),
        migrations.AddField(
            model_name='automationtask',
            name='automations',
            field=models.CharField(default=[], max_length=1024, verbose_name='执行用例'),
            preserve_default=False,
        ),
    ]
