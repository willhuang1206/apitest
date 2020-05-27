# Generated by Django 2.0.2 on 2019-12-19 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0005_automationresult_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024, verbose_name='发布项目名称')),
                ('automations', models.CharField(max_length=1024, verbose_name='执行用例')),
                ('env', models.CharField(max_length=1024, verbose_name='测试环境')),
                ('params', models.CharField(blank=True, max_length=1024, null=True, verbose_name='参数')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('sendEmail', models.BooleanField(default=False, verbose_name='发送邮件')),
                ('emails', models.CharField(blank=True, max_length=1024, null=True, verbose_name='邮箱地址')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_test.Project', verbose_name='项目')),
            ],
            options={
                'verbose_name': '发布项目配置',
                'verbose_name_plural': '发布项目配置管理',
            },
        ),
    ]
