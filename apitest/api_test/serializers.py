import ast
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db.models import Q
from api_test.common.dateUtil import DateUtil
from api_test.models import Project, ProjectDynamic, ProjectMember, ProjectConfig, GlobalConfig,Group,ApiGroupLevelFirst, \
    ApiInfo, APIRequestHistory, ApiOperationHistory, Automation,AutomationStep,AutomationTask, \
    AutomationResult,ApiHead, ApiParameter, ApiResponse, ApiParameterRaw,\
    UserProfile,Automation2Step,AutomationList2Automation,PublishConfig,ApiAutomationCoverage


class TokenSerializer(serializers.ModelSerializer):
    """
    用户信息序列化
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.phone")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.CharField(source="user.date_joined")

    class Meta:
        model = Token
        fields = ('first_name', 'last_name', 'phone', 'email', 'key', 'date_joined')


class UserSerializer(serializers.ModelSerializer):

    id=serializers.CharField(source="user.id")
    username=serializers.CharField(source="user.username")
    name = serializers.CharField(source="user.first_name")
    email = serializers.CharField(source="user.email")
    password=serializers.CharField(source="user.password")

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name','email','phone','type','password')


class ProjectDeserializer(serializers.ModelSerializer):
    """
    项目信息反序列化
    """
    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'type', 'businessline','status', 'LastUpdateTime', 'createTime', 'description', 'user')

class ProjectSerializer(serializers.ModelSerializer):
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'type', 'businessline','status', 'LastUpdateTime', 'createTime', 'description', 'user')

class ProjectInfoSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    apiCount = serializers.SerializerMethodField()
    apiAutomatedCount = serializers.SerializerMethodField()
    automationCount=serializers.SerializerMethodField()
    resultCount=serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    configCount=serializers.SerializerMethodField()
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.first_name')

    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'apiCount',
                  'automationCount','apiAutomatedCount','resultCount','dynamicCount','memberCount', 'configCount','description', 'user')

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_apiAutomatedCount(self, obj):
        return obj.coverage_project.all().filter(api__isnull=False,num__gt=0).count()

    def get_automationCount(self, obj):
        return obj.automation_project.filter(type="case").count()

    def get_resultCount(self, obj):
        return obj.result_project.all().filter(step__isnull=True,automation__isnull=False).count()

    def get_resultCountLastWeek(self, obj):
        start_time,end_time=DateUtil.delta_week(-1)
        if end_time:
            end_time=(datetime.strptime(end_time,'%Y-%m-%d')+timedelta(days=1)).strftime("%Y-%m-%d")
        return obj.result_project.all().filter(step__isnull=True,automation__isnull=False,testTime__gte=start_time,testTime__lte=end_time).count()

    def get_resultCountThisWeek(self, obj):
        start_time,end_time=DateUtil.delta_week(0)
        if end_time:
            end_time=(datetime.strptime(end_time,'%Y-%m-%d')+timedelta(days=1)).strftime("%Y-%m-%d")
        return obj.result_project.all().filter(step__isnull=True,automation__isnull=False,testTime__gte=start_time,testTime__lte=end_time).count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_dynamicCountLastWeek(self, obj):
        start_time,end_time=DateUtil.delta_week(-1)
        if end_time:
            end_time=(datetime.strptime(end_time,'%Y-%m-%d')+timedelta(days=1)).strftime("%Y-%m-%d")
        return obj.dynamic_project.all().filter(time__gte=start_time,time__lte=end_time).count()

    def get_dynamicCountThisWeek(self, obj):
        start_time,end_time=DateUtil.delta_week(0)
        if end_time:
            end_time=(datetime.strptime(end_time,'%Y-%m-%d')+timedelta(days=1)).strftime("%Y-%m-%d")
        return obj.dynamic_project.all().filter(time__gte=start_time,time__lte=end_time).count()

    def get_memberCount(self, obj):
        return obj.member_project.all().filter(~Q(group=1)).count()

    def get_configCount(self, obj):
        return obj.config_project.all().count()


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """
    class Meta:
        model = ProjectDynamic
        fields = ('id', 'project', 'time', 'type', 'operationObject', 'user', 'description')


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'time', 'type', 'operationObject', 'operationUser', 'description')

    def get_operationUser(self, obj):
        if obj.user:
            return obj.user.first_name
        else:
            return "未知"


class ProjectMemberDeserializer(serializers.ModelSerializer):
    """
    项目成员信息反序列化
    """
    class Meta:
        model = ProjectMember
        fields = ('id', 'permissionType', 'project', 'user')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    项目成员信息序列化
    """
    username = serializers.CharField(source='user.first_name')
    userPhone = serializers.CharField(source='user.user.phone')
    userEmail = serializers.CharField(source='user.email')
    group = serializers.CharField(source='group.name')

    class Meta:
        model = ProjectMember
        fields = ('id', 'group', 'username', 'userPhone', 'userEmail')


class ProjectConfigSerializer(serializers.ModelSerializer):
    """
    项目配置序列化
    """

    class Meta:
        model = ProjectConfig
        fields = ('id', 'project_id', 'name', 'value', 'type', 'status', 'description')

class GlobalConfigSerializer(serializers.ModelSerializer):
    """
    配置信息序列化
    """

    class Meta:
        model = GlobalConfig
        fields = ('id', 'name', 'value', 'type','status', 'description')

class GroupSerializer(serializers.ModelSerializer):
    """
    分组信息序列化
    """
    class Meta:
        model = Group
        fields = ('id', 'project_id', 'parent_id', 'name')

class ApiGroupLevelFirstSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """
    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name','parent_id')


class ApiGroupLevelFirstDeserializer(serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """
    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name','parent_id')


class ApiHeadSerializer(serializers.ModelSerializer):
    """
    接口请求头序列化
    """
    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiHeadDeserializer(serializers.ModelSerializer):
    """
    接口请求头反序列化
    """

    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiParameterSerializer(serializers.ModelSerializer):
    """
    接口请求参数序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterDeserializer(serializers.ModelSerializer):
    """
    接口请求参数反序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterRawSerializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiParameterRawDeserializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiResponseSerializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiResponseDeserializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiInfoSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    headers = ApiHeadSerializer(many=True, read_only=True)
    requestParameter = ApiParameterSerializer(many=True, read_only=True)
    response = ApiResponseSerializer(many=True, read_only=True)
    requestParameterRaw = ApiParameterRawSerializer(many=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.first_name')

    class Meta:
        model = ApiInfo
        fields = ('id', 'apiGroupLevelFirst', 'name', 'type','params','httpType', 'requestType', 'apiAddress', 'headers',
                  'requestParameterType', 'requestParameter', 'requestParameterRaw', 'status',
                  'response', 'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description','publish')


class ApiInfoDeserializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    class Meta:
        model = ApiInfo
        fields = ('id', 'project_id', 'name', 'type','params','httpType',
                  'requestType', 'apiAddress', 'requestParameterType', 'status',
                  'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description','publish')


class ApiInfoDocSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    First = ApiInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'name', 'First')


class ApiInfoListSerializer(serializers.ModelSerializer):
    """
    接口信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.first_name')

    class Meta:
        model = ApiInfo
        fields = ('id', 'name', 'params','description','type','requestType', 'apiAddress', 'mockStatus', 'lastUpdateTime', 'userUpdate')


class APIRequestHistorySerializer(serializers.ModelSerializer):
    """
    接口请求历史信息序列化
    """
    requestTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = APIRequestHistory
        fields = ('id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class APIRequestHistoryDeserializer(serializers.ModelSerializer):
    """
    接口请求历史信息反序列化
    """
    class Meta:
        model = APIRequestHistory
        fields = ('id', 'api_id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class ApiOperationHistorySerializer(serializers.ModelSerializer):
    """
    接口操作历史信息序列化
    """
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.first_name')

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'user', 'time', 'description')


class ApiOperationHistoryDeserializer(serializers.ModelSerializer):
    """
    接口操作历史信息反序列化
    """

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'apiInfo', 'user', 'time', 'description')


class AutomationSerializer(serializers.ModelSerializer):
    """
    自动化信息序列化
    """
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='user.first_name')

    class Meta:
        model = Automation
        fields = ('id', 'group', 'name','type', 'userUpdate',
                  'description', 'updateTime','params','publish')

class AutomationListSerializer(serializers.ModelSerializer):
    """
    自动化信息序列化
    """
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='user.first_name')

    class Meta:
        model = Automation
        fields = ('id', 'group', 'name','type', 'userUpdate',
                  'description', 'updateTime','publish')

class AutomationDeserializer(serializers.ModelSerializer):
    """
    自动化反序列化
    """
    class Meta:
        model = Automation
        fields = ('id', 'project_id', 'group', 'name', 'type','user',
                  'description', 'updateTime','params','publish')

class AutomationStepSerializer(serializers.ModelSerializer):
    """
    自动化用例步骤序列化
    """

    class Meta:
        model = AutomationStep
        fields = ('id', 'name', 'type', 'params', 'steps', 'description')


class Automation2StepSerializer(serializers.ModelSerializer):

    stepId = serializers.IntegerField(source='step.id')
    name = serializers.CharField(source='step.name')
    type = serializers.CharField(source='step.type')
    params = serializers.CharField(source='step.params')
    steps = serializers.CharField(source='step.steps')
    description = serializers.CharField(source='step.description')

    class Meta:
        model = Automation2Step
        fields = ('id', 'stepId','name', 'type', 'params', 'steps', 'description','status','order')

class AutomationList2AutomationSerializer(serializers.ModelSerializer):

    stepId = serializers.IntegerField(source='automationStep.id')
    name = serializers.CharField(source='automationStep.name')
    type = serializers.CharField(source='automationStep.type')
    params = serializers.CharField(source='automationStep.params')
    description = serializers.CharField(source='automationStep.description')

    class Meta:
        model = AutomationList2Automation
        fields = ('id', 'stepId','name', 'type', 'params', 'description','status','order')

class AutomationTaskSerializer(serializers.ModelSerializer):
    """
    定时任务信息序列化
    """
    # startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # endTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    automationName = serializers.SerializerMethodField()
    automations = serializers.SerializerMethodField()
    emails = serializers.SerializerMethodField()

    class Meta:
        model = AutomationTask
        fields = ('id', 'project','automations','automationName', 'env', 'name', 'params', 'crontab', 'status','sendEmail','emails')

    def get_automationName(self, obj):
        automations=Automation.objects.filter(id__in=ast.literal_eval(obj.automations))
        return ','.join([automation.name for automation in automations])

    def get_automations(self, obj):
        return ast.literal_eval(obj.automations)

    def get_emails(self, obj):
        return ast.literal_eval(obj.emails)

class AutomationTaskDeserializer(serializers.ModelSerializer):
    """
    定时任务信息反序列化
    """

    class Meta:
        model = AutomationTask
        fields = ('id', 'project_id','automations','env', 'name', 'params', 'crontab', 'status', 'sendEmail','emails')

class ApiAutomationCoverageSerializer(serializers.ModelSerializer):
    """
    接口自动化覆盖率
    """
    automationName = serializers.SerializerMethodField()
    automations = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ApiAutomationCoverage
        fields = ('id', 'project','automations','automationName', 'name', 'num')

    def get_automationName(self, obj):
        automations=Automation.objects.filter(id__in=ast.literal_eval(obj.automations))
        return ','.join([automation.name for automation in automations])

    def get_automations(self, obj):
        return ast.literal_eval(obj.automations)

    def get_name(self, obj):
        return obj.api.name

class AutomationResultSerializer(serializers.ModelSerializer):
    """
    自动化执行结果序列化
    """
    name=serializers.SerializerMethodField()
    testTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    failType=serializers.SerializerMethodField()
    failSeverity=serializers.SerializerMethodField()
    failCause=serializers.SerializerMethodField()
    failDetail=serializers.SerializerMethodField()
    failBug=serializers.SerializerMethodField()

    class Meta:
        model = AutomationResult
        fields = ('id', 'automation_id','result', 'testTime','trace','env','failType','failSeverity','failCause','failDetail','failBug','name','duration')

    def get_name(self,obj):
        return "%s,%s" % (obj.name,obj.description) if obj.description and "上线单" in obj.description else obj.name

    def get_failDetail(self,obj):
        return obj.failDetail.first().detail if obj.result=="FAIL" and obj.failDetail.first() else obj.description

    def get_failType(self,obj):
        return obj.failDetail.first().type if obj.result=="FAIL" and obj.failDetail.first() else "other"

    def get_failSeverity(self,obj):
        return obj.failDetail.first().severity if obj.result=="FAIL" and obj.failDetail.first() else "major"

    def get_failCause(self,obj):
        return obj.failDetail.first().cause if obj.result=="FAIL" and obj.failDetail.first() else ""

    def get_failBug(self,obj):
        return obj.failDetail.first().bug if obj.result=="FAIL" and obj.failDetail.first() else ""

class PublishConfigSerializer(serializers.ModelSerializer):
    """
    发布项目配置序列化
    """
    automationName = serializers.SerializerMethodField()
    automations = serializers.SerializerMethodField()
    emails = serializers.SerializerMethodField()

    class Meta:
        model = PublishConfig
        fields = ('id', 'project','automations','automationName', 'env', 'name', 'params', 'status','sendEmail','emails')

    def get_automationName(self, obj):
        automations=Automation.objects.filter(id__in=ast.literal_eval(obj.automations))
        return ','.join([automation.name for automation in automations])

    def get_automations(self, obj):
        return ast.literal_eval(obj.automations)

    def get_emails(self, obj):
        return ast.literal_eval(obj.emails)

class PublishConfigDeserializer(serializers.ModelSerializer):
    """
    发布项目配置反序列化
    """

    class Meta:
        model = PublishConfig
        fields = ('id', 'project_id','automations','env', 'name', 'params', 'status', 'sendEmail','emails')