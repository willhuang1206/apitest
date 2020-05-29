
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from api_test.models import Project, ProjectConfig, ApiGroupLevelFirst, ApiInfo, \
    APIRequestHistory, ApiOperationHistory, ProjectDynamic, ProjectMember, \
    AutomationTask, UserProfile, ApiHead, ApiParameter, ApiResponse, \
    ApiParameterRaw

from django.contrib import admin
from django.utils.text import capfirst
from collections import OrderedDict as SortedDict


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        for app in template_response.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return template_response

    return inner


registry = SortedDict()
registry.update(admin.site._registry)
admin.site._registry = registry
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)
admin.site.site_header = '测试平台后台管理'
admin.site.siteTitle = '后台管理'

display = ()


class ProfileInline(admin.TabularInline):
    """
    用户模块扩展
    """
    model = UserProfile


class PhoneForm(admin.ModelAdmin):
    fieldsets = ([
        '手机号', {
            'fields': ('phone',)
        }],)


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """ModelAdmin class that prevents modifications through the admin.

    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    """

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return True
        return super(ReadOnlyModelAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class ReadAndDeleteModelAdmin(admin.ModelAdmin):
    """ModelAdmin class that prevents modifications through the admin.

    The changelist and the detail view work, but a 403 is returned
    if one actually tries to edit an object.
    """

    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them
    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return True
        return super(ReadAndDeleteModelAdmin, self).has_change_permission(request, obj)


class MemberInProject(admin.TabularInline):
    model = ProjectMember


class ConfigInProject(admin.TabularInline):
    model = ProjectConfig


class ProjectForm(admin.ModelAdmin):
    inlines = [MemberInProject, ConfigInProject]
    search_fields = ('name', 'type')
    list_display = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'user')
    list_display_links = ('id', 'name',)
    list_filter = ('status', 'type')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '项目', {
            'fields': ('name', 'version', 'type', 'description', 'status', 'user')
        }],
    )


admin.site.register(Project, ProjectForm)


class ProjectConfigForm(admin.ModelAdmin):
    search_fields = ('name', 'project')
    list_display = ('id', 'project', 'name', 'value', 'status')
    list_display_links = ('id', 'project', 'name', 'value')
    list_filter = ('project', 'status')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '项目配置', {
            'fields': ('project', 'name', 'value', 'description', 'status')
        }],)


admin.site.register(ProjectConfig, ProjectConfigForm)


class CustomMethodForm(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'project', 'name', 'description', 'type', 'status', 'dataCode')
    list_display_links = ('id', 'project', 'name')
    list_filter = ('project', 'type', 'status')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '自定义方法', {
            'fields': ('project', 'name', 'description', 'type', 'status', 'dataCode')
        }],)


class ApiGroupLevelFirstForm(admin.ModelAdmin):
    search_fields = ('name', 'project')
    list_display = ('id', 'project', 'name')
    list_display_links = ('id', 'project', 'name')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口分组', {
            'fields': ('project', 'name')
        }],)


admin.site.register(ApiGroupLevelFirst, ApiGroupLevelFirstForm)


class ApiHeadInline(admin.TabularInline):
    model = ApiHead


class ApiParameterInline(admin.TabularInline):
    model = ApiParameter


class ApiParameterRawInline(admin.TabularInline):
    model = ApiParameterRaw


class ApiResponseInline(admin.TabularInline):
    model = ApiResponse


class ApiInfoForm(admin.ModelAdmin):
    inlines = [ApiHeadInline, ApiParameterInline, ApiParameterRawInline, ApiResponseInline]
    search_fields = ('name', 'project', 'httpType', 'requestType', 'apiAddress', 'requestParameterType')
    list_display = ('id', 'project', 'name', 'httpType', 'requestType',
                    'apiAddress', 'status', 'lastUpdateTime', 'userUpdate')
    list_display_links = ('id', 'name', 'project')
    list_filter = ('project', 'httpType', 'requestType', 'status')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口信息', {
            'fields': ('project', 'apiGroupLevelFirst', 'name', 'httpType',
                       'requestParameterType', 'requestType', 'apiAddress', 'status', 'mockCode', 'data', 'userUpdate')
        }],)


admin.site.register(ApiInfo, ApiInfoForm)


class APIRequestHistoryForm(ReadOnlyModelAdmin):
    search_fields = ('api', 'requestType', 'httpCode')
    list_display = ('id', 'api', 'requestType', 'requestAddress', 'httpCode', 'requestTime')
    list_display_links = ('id', 'api', 'requestTime')
    list_filter = ('requestType', 'httpCode')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口请求历史', {
            'fields': ('api', 'requestType', 'requestAddress', 'httpCode')
        }],)


admin.site.register(APIRequestHistory, APIRequestHistoryForm)


class ApiOperationHistoryForm(ReadOnlyModelAdmin):
    search_fields = ('api', 'user')
    list_display = ('id', 'api', 'user', 'description', 'time')
    list_display_links = ('id', 'api', 'user')
    list_filter = ('user',)
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '接口操作记录', {
            'fields': ('api', 'user', 'description')
        }],)


admin.site.register(ApiOperationHistory, ApiOperationHistoryForm)


class ProjectMemberForm(admin.ModelAdmin):
    search_fields = ('user', 'project')
    list_display = ('id', 'group', 'project', 'user')
    list_display_links = ('group', 'project')
    list_filter = ('group', 'project', 'user')
    list_per_page = 20
    ordering = ('id',)
    fieldsets = ([
        '项目成员', {
            'fields': ('group', 'project', 'user')
        }],
    )


admin.site.register(ProjectMember, ProjectMemberForm)


class ProjectDynamicForm(ReadOnlyModelAdmin):
    search_fields = ('operationObject', 'user')
    list_display = ('id', 'project', 'time', 'type', 'operationObject', 'description', 'user')
    list_display_links = ('id', 'project', 'time')
    list_filter = ('project', 'type')
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(ProjectDynamic, ProjectDynamicForm)
