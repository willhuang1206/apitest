from django.contrib.auth.models import User,Group as UserGroup
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('application/x-www-form-urlencoded','表单(x-www-form-urlencoded)'),
    ('application/json', 'JSON'),
    ('application/xml', 'XML'),
    ('text/plain', 'Text'),
    ('multipart/form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('Restful', 'Restful')
)

API_TYPE = (
    ('http', '普通http'),
    ('jyb', '加油宝app'),
    ('service', '微服务')
)

STEP_TYPE = (
    ('normal', '普通'),
    ('project', '项目'),
    ('global', '全局')
)

AUTOMATION_TYPE = (
    ('case', '普通用例'),
    ('reuse', '可复用用例'),
    ('list', '用例集'),
    ('data', '数据用例'),
    ('monitor', '接口监控')
)

CONFIG_TYPE = (
    ('env', '环境'),
    ('data', '数据'),
    ('config', '配置'),
    ('tag', '标签')
)

SENDEMAIL_TYPE = (
    (0, '不发送'),
    (1, '发送'),
    (2, '失败发送'),
    (3, '成功发送')
)

FAIL_TYPE = (
    ('code', '编码'),
    ('env', '环境'),
    ('data', '数据'),
    ('other', '其他')
)

SEVERITY = (
    ('fatal', '致命的'),
    ('critical', '严重的'),
    ('major', '一般的'),
    ('minor', '微小的')
)

PARAMETER_TYPE_CHOICE = (
    ('text', 'text'),
    ('file', 'file')
)

HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)

EXAMINE_TYPE_CHOICE = (
    ('no_check', '不校验'),
    ('only_check_status', '校验http状态'),
    ('json', 'JSON校验'),
    ('entirely_check', '完全校验'),
    ('Regular_check', '正则校验'),
)

UNIT_CHOICE = (
    ('m', '分'),
    ('h', '时'),
    ('d', '天'),
    ('w', '周'),
)

RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
    ('RUNNING', '执行中'),
)


TASK_CHOICE = (
    ('circulation', '循环'),
    ('timing', '定时'),
)

USER_TYPE = (
    ('global', '统一用户'),
    ('local', '本地用户'),
)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# ==================扩展用户====================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='user')
    phone = models.CharField(max_length=11, default='', blank=True, verbose_name='手机号')
    type = models.CharField(max_length=50, default='global',verbose_name='用户类型', choices=USER_TYPE)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.phone

class Project(models.Model):
    """
    项目表
    """
    ProjectType = (
        ('Web', 'Web'),
        ('App', 'App')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, verbose_name='项目名称')
    version = models.CharField(max_length=50, verbose_name='版本')
    type = models.CharField(max_length=50, verbose_name='类型', choices=ProjectType)
    businessline = models.CharField(max_length=50, null=True, verbose_name='业务线')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='dynamic_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(max_length=128, verbose_name='操作时间')
    type = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, related_name='userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True,  verbose_name='描述')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'


class ProjectMember(models.Model):
    """
    项目成员
    """
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(UserGroup, related_name='member_group', on_delete=models.CASCADE, verbose_name='用户组')
    project = models.ForeignKey(Project, related_name='member_project', on_delete=models.CASCADE, verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.group.name

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'


class ProjectConfig(models.Model):
    """
    host域名
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='config_project',on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=1024, verbose_name='名称')
    value = models.CharField(max_length=1024, blank=True, verbose_name='值')
    type = models.CharField(max_length=50, verbose_name='类型', choices=CONFIG_TYPE)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目配置'
        verbose_name_plural = '项目配置管理'

class GlobalConfig(models.Model):
    """
    配置
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, verbose_name='名称')
    value = models.CharField(max_length=1024, blank=True, verbose_name='值')
    type = models.CharField(max_length=50, verbose_name='类型', choices=CONFIG_TYPE)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = '配置'

class CustomMethod(models.Model):
    """
    自定义方法
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='方法名')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    type = models.CharField(max_length=50, verbose_name='类型')
    dataCode = models.TextField(verbose_name='代码')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '自定义方法'
        verbose_name_plural = '自定义方法'

class Group(models.Model):
    """
    分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    parent = models.ForeignKey("Group", on_delete=models.SET_NULL, null=True, verbose_name='父分组')
    name = models.CharField(max_length=1024, verbose_name='分组名称')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例分组'
        verbose_name_plural = '用例分组'

class ApiGroupLevelFirst(models.Model):
    """
    接口一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    parent = models.ForeignKey("ApiGroupLevelFirst", on_delete=models.SET_NULL, null=True, verbose_name='父分组')
    name = models.CharField(max_length=1024, verbose_name='分组名称')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'


class ApiInfo(models.Model):
    """
    接口信息
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='api_project', on_delete=models.CASCADE, verbose_name='所属项目')
    apiGroupLevelFirst = models.ForeignKey(ApiGroupLevelFirst, on_delete=models.SET_NULL,null=True,
                                           related_name='api_group',verbose_name='所属分组')
    name = models.CharField(max_length=1024, verbose_name='接口名称')
    type = models.CharField(max_length=50, default='http', verbose_name='接口类型', choices=API_TYPE)
    params = models.TextField(blank=True, null=True, verbose_name='参数')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.BooleanField(default=True, verbose_name='状态')
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")
    mockCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    data = models.TextField(blank=True, null=True, verbose_name='mock内容')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='更新人',
                                   related_name='ApiUpdateUser')
    publish = models.CharField(max_length=1024, blank=True, null=True, verbose_name='发布项目')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'


class ApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='headers')
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


class ApiParameter(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameter')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型', choices=(('Int', 'Int'), ('String', 'String'), ('Object', 'Object'),('Array', 'Array')))
    value = models.TextField(blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必填")
    restrict = models.CharField(max_length=1024, blank=True, null=True, verbose_name="输入限制")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求参数'
        verbose_name_plural = '请求参数管理'


class ApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.OneToOneField(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameterRaw')
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'


class ApiResponse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='response')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型', choices=(('Int', 'Int'), ('String', 'String'), ('Object', 'Object'), ('Array', 'Array')))
    value = models.TextField(blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必含")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '返回参数'
        verbose_name_plural = '返回参数管理'


class APIRequestHistory(models.Model):
    """
    接口请求历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    requestTime = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')
    requestType = models.CharField(max_length=50, verbose_name='请求方法')
    requestAddress = models.CharField(max_length=1024, verbose_name='请求地址')
    httpCode = models.CharField(max_length=50, verbose_name='HTTP状态')

    def __unicode__(self):
        return self.requestAddress

    class Meta:
        verbose_name = '接口请求历史'
        verbose_name_plural = '接口请求历史'


class ApiOperationHistory(models.Model):
    """
    API操作历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='用户姓名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='操作内容')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = '接口操作历史'
        verbose_name_plural = '接口操作历史'

class AutomationStep(models.Model):
    """
    自动化步骤
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True,
                                verbose_name='项目', related_name="project")
    name = models.CharField(max_length=1024, verbose_name='步骤名称')
    type = models.CharField(max_length=50, default='normal', verbose_name='步骤类型', choices=STEP_TYPE)
    params = models.TextField(blank=True, null=True, verbose_name='参数')
    steps = models.TextField(verbose_name='步骤操作')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="创建人",
                             related_name="stepUser")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '自动化步骤'
        verbose_name_plural = '自动化步骤'

class Automation(models.Model):
    """
    自动化
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name="automation_project",on_delete=models.CASCADE, verbose_name='所属项目')
    group = models.ForeignKey(Group, blank=True, null=True,on_delete=models.SET_NULL, verbose_name='分组', related_name="automationGroup")
    name = models.CharField(max_length=1024, verbose_name='自动化名称')
    type = models.CharField(max_length=50, default='case', verbose_name='自动化类型', choices=AUTOMATION_TYPE)
    params = models.TextField(blank=True, null=True, verbose_name='参数')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="更新人",
                             related_name="automationUser")
    publish = models.CharField(max_length=1024, blank=True, null=True, verbose_name='发布项目')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    steps = models.ManyToManyField(AutomationStep,through="Automation2Step")
    apis = models.ManyToManyField(ApiInfo)
    automations = models.ManyToManyField("Automation",through="AutomationList2Automation")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '自动化'
        verbose_name_plural = '自动化'


class Automation2Step(models.Model):
    id = models.AutoField(primary_key=True)
    automation = models.ForeignKey(Automation,on_delete=models.CASCADE)
    step = models.ForeignKey(AutomationStep,on_delete=models.CASCADE)
    status = models.BooleanField(default=True, verbose_name='状态')
    order = models.IntegerField(blank=True, null=True, verbose_name='顺序')


class AutomationList2Automation(models.Model):
    id = models.AutoField(primary_key=True)
    automationParent = models.ForeignKey(Automation,on_delete=models.CASCADE,related_name="automationParent")
    automationStep = models.ForeignKey(Automation,on_delete=models.CASCADE,related_name="automationStep")
    status = models.BooleanField(default=True, verbose_name='状态')
    order = models.IntegerField(blank=True, null=True, verbose_name='顺序')

class ApiAutomationCoverage(models.Model):
    """
    接口自动化覆盖
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, blank=True, null=True,related_name='coverage_project',on_delete=models.SET_NULL,verbose_name='项目')
    api = models.ForeignKey(ApiInfo,blank=True, null=True,on_delete=models.SET_NULL, verbose_name='接口')
    automations = models.CharField(max_length=1024, verbose_name='关联用例')
    num = models.IntegerField(blank=True, null=True,default=0, verbose_name='关联数量')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    def __unicode__(self):
        return self.api.name

    class Meta:
        verbose_name = '接口自动化覆盖'
        verbose_name_plural = '接口自动化覆盖管理'

class AutomationTask(models.Model):
    """
    用例定时任务
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE,verbose_name='项目')
    automations = models.CharField(max_length=1024, verbose_name='执行用例')
    # automation = models.ForeignKey(Automation, blank=True, null=True, on_delete=models.CASCADE,verbose_name='自动化用例')
    name = models.CharField(max_length=1024, verbose_name='任务名称')
    env = models.CharField(max_length=1024, verbose_name='执行环境')
    params = models.TextField(blank=True, null=True, verbose_name='参数')
    crontab = models.CharField(max_length=50, verbose_name='定时器')
    startTime = models.DateTimeField(max_length=50, blank=True, null=True, verbose_name='开始时间')
    endTime = models.DateTimeField(max_length=50, blank=True, null=True, verbose_name='结束时间')
    status = models.BooleanField(default=True, verbose_name='状态')
    sendEmail = models.IntegerField(blank=True, null=True, default=0,verbose_name='发送邮件',choices=SENDEMAIL_TYPE)
    emails = models.CharField(max_length=1024, blank=True, null=True, verbose_name='邮箱地址')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例定时任务'
        verbose_name_plural = '用例定时任务管理'


class AutomationResult(models.Model):
    """
    自动化执行结果
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='result_project',blank=True, null=True, on_delete=models.CASCADE,verbose_name='项目')
    automation = models.ForeignKey(Automation, blank=True, null=True, on_delete=models.CASCADE, verbose_name='用例'
                                          , related_name="result_automation")
    step = models.ForeignKey(AutomationStep, blank=True, null=True,on_delete=models.SET_NULL, verbose_name='步骤'
                                          , related_name="步骤")
    api = models.ForeignKey(ApiInfo, blank=True, null=True,on_delete=models.SET_NULL, verbose_name='接口'
                                          , related_name="接口")
    name = models.CharField(blank=True, null=True,max_length=1024, verbose_name='名称')
    trace = models.CharField(blank=True, null=True,max_length=25, verbose_name='时间戳')
    value = models.TextField(blank=True, null=True, verbose_name='输入')
    env = models.CharField(blank=True, null=True,max_length=50, verbose_name='环境')
    details = models.TextField(blank=True, null=True, verbose_name='执行详情')
    result = models.CharField(max_length=50, verbose_name='执行结果', choices=RESULT_CHOICE)
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='执行人')
    testTime = models.CharField(max_length=50,blank=True, null=True, verbose_name='测试时间')
    duration=models.IntegerField(blank=True, null=True, default=0,verbose_name='执行时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '自动化执行结果'
        verbose_name_plural = '自动化执行结果管理'

class AutomationResultFailDetail(models.Model):
    """
    自动化执行失败详情
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='faildetail_project',blank=True, null=True, on_delete=models.CASCADE,verbose_name='项目')
    result = models.ForeignKey(AutomationResult, on_delete=models.CASCADE, verbose_name='执行结果', related_name="failDetail")
    type = models.CharField(max_length=50, verbose_name='失败类型', choices=FAIL_TYPE)
    severity = models.CharField(max_length=50, verbose_name='严重等级', choices=SEVERITY)
    cause = models.CharField(max_length=256,blank=True, null=True, verbose_name='根源')
    detail = models.TextField(blank=True, null=True, verbose_name='详情')
    bug = models.CharField(max_length=50,blank=True, null=True, verbose_name='关联缺陷')
    action = models.CharField(max_length=256,blank=True, null=True, verbose_name='处理方式')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = '自动化执行失败详情'
        verbose_name_plural = '自动化执行失败详情管理'

class PublishConfig(models.Model):
    """
    发布项目配置
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE,verbose_name='项目')
    name = models.CharField(max_length=1024, verbose_name='发布项目名称')
    automations = models.CharField(max_length=1024, verbose_name='执行用例')
    env = models.CharField(max_length=1024, verbose_name='测试环境')
    params = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数')
    status = models.BooleanField(default=True, verbose_name='状态')
    sendEmail = models.IntegerField(blank=True, null=True, default=0,verbose_name='发送邮件',choices=SENDEMAIL_TYPE)
    emails = models.CharField(max_length=1024, blank=True, null=True, verbose_name='邮箱地址')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '发布项目配置'
        verbose_name_plural = '发布项目配置管理'

class AutomationReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")

    def __unicode__(self):
        return self.reportFrom

    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"


class VisitorsRecord(models.Model):
    """
    访客记录
    """
    id = models.AutoField(primary_key=True)
    formattedAddress = models.CharField(max_length=1024, blank=True, null=True, verbose_name="访客地址")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="国家")
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name="省份")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="城市")
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name="县级")
    township = models.CharField(max_length=50, blank=True, null=True, verbose_name="镇")
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name="街道")
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name="门牌号")
    success = models.CharField(max_length=50, blank=True, null=True, verbose_name="成功")
    reason = models.CharField(max_length=1024, blank=True, null=True, verbose_name="原因")
    callTime = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __unicode__(self):
        return self.formattedAddress

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = "访客查看"
