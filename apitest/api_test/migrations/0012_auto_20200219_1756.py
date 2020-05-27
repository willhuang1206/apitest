# Generated by Django 2.0.2 on 2020-02-19 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0011_apiautomationcoverage_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiautomationcoverage',
            name='num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='关联数量'),
        ),
        migrations.AlterField(
            model_name='apiautomationcoverage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coverage_project', to='api_test.Project', verbose_name='项目'),
        ),
        migrations.AlterField(
            model_name='apiparameter',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='参数值'),
        ),
        migrations.AlterField(
            model_name='apiresponse',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='参数值'),
        ),
        migrations.AlterField(
            model_name='automation',
            name='params',
            field=models.TextField(blank=True, null=True, verbose_name='参数'),
        ),
        migrations.AlterField(
            model_name='automationresult',
            name='automation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_automation', to='api_test.Automation', verbose_name='用例'),
        ),
        migrations.AlterField(
            model_name='automationstep',
            name='params',
            field=models.TextField(blank=True, null=True, verbose_name='参数'),
        ),
        migrations.AlterField(
            model_name='automationtask',
            name='params',
            field=models.TextField(blank=True, null=True, verbose_name='参数'),
        ),
    ]