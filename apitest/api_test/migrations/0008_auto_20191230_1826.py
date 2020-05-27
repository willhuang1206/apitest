# Generated by Django 2.0.2 on 2019-12-30 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0007_auto_20191224_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('value', models.CharField(blank=True, max_length=1024, verbose_name='值')),
                ('type', models.CharField(choices=[('env', '环境'), ('data', '数据'), ('config', '配置'), ('tag', '标签')], max_length=50, verbose_name='类型')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config_project', to='api_test.Project', verbose_name='项目')),
            ],
            options={
                'verbose_name': '项目配置',
                'verbose_name_plural': '项目配置管理',
            },
        ),
        migrations.RemoveField(
            model_name='globalhost',
            name='project',
        ),
        migrations.AlterField(
            model_name='automationtask',
            name='sendEmail',
            field=models.IntegerField(blank=True, choices=[(0, '不发送'), (1, '发送'), (2, '失败发送'), (3, '成功发送')], default=0, null=True, verbose_name='发送邮件'),
        ),
        migrations.AlterField(
            model_name='publishconfig',
            name='sendEmail',
            field=models.IntegerField(blank=True, choices=[(0, '不发送'), (1, '发送'), (2, '失败发送'), (3, '成功发送')], default=0, null=True, verbose_name='发送邮件'),
        ),
        migrations.DeleteModel(
            name='GlobalHost',
        ),
    ]
