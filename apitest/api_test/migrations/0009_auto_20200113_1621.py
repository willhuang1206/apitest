# Generated by Django 2.0.2 on 2020-01-13 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0008_auto_20191230_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationResultFailDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('code', '编码'), ('env', '环境'), ('data', '数据'), ('other', '其他')], max_length=50, verbose_name='失败类型')),
                ('severity', models.CharField(choices=[('fatal', '致命的'), ('critical', '严重的'), ('major', '一般的'), ('minor', '微小的')], max_length=50, verbose_name='严重等级')),
                ('cause', models.CharField(blank=True, max_length=256, null=True, verbose_name='根源')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='详情')),
                ('bug', models.CharField(blank=True, max_length=50, null=True, verbose_name='关联缺陷')),
                ('action', models.CharField(blank=True, max_length=256, null=True, verbose_name='处理方式')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faildetail_project', to='api_test.Project', verbose_name='项目')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='failDetail', to='api_test.AutomationResult', verbose_name='执行结果')),
            ],
            options={
                'verbose_name': '自动化执行失败详情',
                'verbose_name_plural': '自动化执行失败详情管理',
            },
        ),
        migrations.AlterField(
            model_name='automation',
            name='type',
            field=models.CharField(choices=[('case', '普通用例'), ('reuse', '可复用用例'), ('list', '用例集'), ('data', '数据用例'), ('monitor', '接口监控')], default='case', max_length=50, verbose_name='自动化类型'),
        ),
    ]