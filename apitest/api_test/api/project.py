import logging
import traceback
from crontab import CronTab
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api_test.common.auth import TokenAuthentication,Group
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic
from api_test.common.jsonUtil import json
from api_test.common.auth import permission_required
from api_test.models import Project,ProjectMember,ProjectDynamic,ProjectConfig
from api_test.serializers import ProjectSerializer, ProjectDeserializer, \
    ProjectMemberDeserializer,ProjectDynamicSerializer,ProjectConfigSerializer,ProjectMemberSerializer,ProjectInfoSerializer
from api_test.service.configService import getConfigValueByName

class ProjectList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
            status=request.GET.get("status", False)
            name = request.GET.get("name")
            businessline = request.GET.get("businessline")
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        if status:
            obis = Project.objects.filter(status=True).order_by("-id")
        elif name:
            obis = Project.objects.filter(name__contains=name).order_by("-id")
        elif businessline:
            obis = Project.objects.filter(businessline=businessline).order_by("-id")
        else:
            obis = Project.objects.all().order_by("-id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(obis)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ProjectSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功")


class AddProject(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, version, type
            if not data["name"] or not data["version"] or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误！")
            # type 类型 Web， App
            if data["type"] not in ["Web", "App"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def add_project_member(self, project, user):
        """
        添加项目创建人员
        :param project: 项目ID
        :param user:  用户ID
        :return:
        """
        # project = Project.objects.get(id=project)
        # user = User.objects.get(id=user)
        ProjectMember.objects.create(project_id=project,user_id=user,group_id=1)

    def post(self, request):
        """
        新增项目
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = request.user.pk
        project_serializer = ProjectDeserializer(data=data)
        try:
            Project.objects.get(name=data["name"])

            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if project_serializer.is_valid():
                    # 保持新项目
                    project_serializer.save()
                    # 记录动态
                    record_dynamic(project=project_serializer.data.get("id"),
                                   _type="添加", operationObject="项目", user=request.user.pk, data=data["name"])
                    # 创建项目的用户添加为该项目的成员
                    self.add_project_member(project_serializer.data.get("id"), request.user.pk)
                    return JsonResponse(data={
                            "project_id": project_serializer.data.get("id")
                        }, code="999999", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class UpdateProject(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["project_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, version , type
            if not data["name"] or not data["version"] or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误！")
            # type 必为Web， App
            if data["type"] not in ["Web", "App"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改项目
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        # 查找是否相同名称的项目
        pro_name = Project.objects.filter(name=data["name"]).exclude(id=data["project_id"])
        if len(pro_name):
            return JsonResponse(code="999997", msg="存在相同名称")
        else:
            try:
                serializer = ProjectDeserializer(data=data)
                with transaction.atomic():
                    if serializer.is_valid():
                        # 修改项目
                        serializer.update(instance=obj, validated_data=data)
                        # 记录动态
                        record_dynamic(project=data["project_id"],
                                       _type="修改", operationObject="项目", user=request.user.pk, data=data["name"])
                        return JsonResponse(code="999999", msg="成功")
                    else:
                        return JsonResponse(code="999998", msg="失败")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败")


class DelProject(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        删除项目
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                try:
                    obj = Project.objects.get(id=i)
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="项目不存在！")
            for j in data["ids"]:
                obj = Project.objects.filter(id=j)
                obj.delete()
                my_user_cron = CronTab(user=True)
                my_user_cron.remove_all(comment=j)
                my_user_cron.write()
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class DisableProject(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["project_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        禁用项目
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = Project.objects.get(id=data["project_id"])
            obj.status = False
            obj.save()
            record_dynamic(project=data["project_id"],
                           _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class EnableProject(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["project_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        启用项目
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = Project.objects.get(id=data["project_id"])
            obj.status = True
            obj.save()
            record_dynamic(project=data["project_id"],
                           _type="启用", operationObject="项目", user=request.user.pk, data=obj.name)
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")

class ProjectInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目详情
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        if not project_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not project_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        # 查找项目是否存在
        try:
            obj = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        serialize = ProjectInfoSerializer(obj)
        if serialize.data["status"]:
            return JsonResponse(data=serialize.data, code="999999", msg="成功！")
        else:
            return JsonResponse(code="999985", msg="该项目已禁用")

class Dynamic(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目动态
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        if not project_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        name = request.GET.get("name","")
        objs = ProjectDynamic.objects.filter(project=project_id,description__contains=name).order_by("-time")
        paginator = Paginator(objs, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(objs)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ProjectDynamicSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")

class ConfigList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目配置列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        if not project_id.isdecimal():
            return JsonResponse(code="999995", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        name = request.GET.get("name")
        type = request.GET.get("type")
        if name and type:
            obis = ProjectConfig.objects.filter(project=project_id,name__contains=name,type=type).order_by("-id")
        elif name:
            obis = ProjectConfig.objects.filter(project=project_id,name__contains=name).order_by("-id")
        elif type:
            obis = ProjectConfig.objects.filter(project=project_id,type=type).order_by("-id")
        else:
            obis = ProjectConfig.objects.filter(project=project_id).order_by("-id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(obis)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ProjectConfigSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("add_projectconfig")
    def post(self, request):
        """
        添加项目配置
        :param request:
        :return:
        """
        data = request.data
        try:
            obj = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = ProjectConfig.objects.filter(name=data["name"], project=data["project_id"])
        if obi:
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = ProjectConfigSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.save(project=obj)
                    # 记录动态
                    record_dynamic(project=data["project_id"],
                                   _type="添加", operationObject="配置", user=request.user.pk, data=data["name"])
                    return JsonResponse(data={
                        "config_id": serializer.data.get("id")
                    }, code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class UpdateConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_projectconfig")
    def post(self, request):
        """
        修改项目配置
        :param request:
        :return:
        """
        data = request.data
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obi = ProjectConfig.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="配置不存在！")
        config_name = ProjectConfig.objects.filter(project=data["project_id"],name=data["name"]).exclude(id=data["id"])
        if len(config_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = ProjectConfigSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.update(instance=obi, validated_data=data)
                    # 记录动态
                    record_dynamic(project=data["project_id"],
                                   _type="修改", operationObject="配置", user=request.user.pk, data=data["name"])
                    return JsonResponse(code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class DelConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("delete_projectconfig")
    def post(self, request):
        """
        删除项目配置
        :param request:
        :return:
        """
        data = request.data
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            for j in data["ids"]:
                obj = ProjectConfig.objects.filter(id=j)
                if obj:
                    name = obj[0].name
                    obj.delete()
                    record_dynamic(project=data["project_id"],
                                   _type="删除", operationObject="配置", user=request.user.pk, data=name)
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="配置不存在！")


class DisableConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_projectconfig")
    def post(self, request):
        """
        禁用项目配置
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = ProjectConfig.objects.get(id=data["config_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="配置不存在")
        obj.status = False
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="禁用", operationObject="配置", user=request.user.pk, data=obj.name)
        return JsonResponse(code="999999", msg="成功！")


class EnableConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_projectconfig")
    def post(self, request):
        """
        启用项目配置
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = ProjectConfig.objects.get(id=data["config_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="配置不存在")
        obj.status = True
        obj.save()
        record_dynamic(project=data["project_id"],
                       _type="启用", operationObject="配置", user=request.user.pk, data=obj.name)
        return JsonResponse(code="999999", msg="成功！")

class ProjectMemberList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目成员列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        if not project_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not project_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obis = ProjectMember.objects.filter(Q(project=project_id) & ~Q(group=1)).order_by("id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(obis)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ProjectMemberSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")

class UpdateMembers(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_projectmember")
    def post(self, request):
        """
        添加用户
        :param request:
        :return:
        """
        data = request.data
        with transaction.atomic():
            try:
                project=Project.objects.get(id=data["project_id"])
                ids=data["ids"]
                for id in ids:
                    user=User.objects.get(id=id)
                    if int(data["group"])==0:
                        ProjectMember.objects.filter(project=project,user=user).delete()
                    else:
                        group=Group.objects.get(id=data["group"])
                        members=ProjectMember.objects.filter(project=project,user=user)
                        if len(members)>0:
                            members.update(group=group)
                        else:
                            ProjectMember.objects.create(project=project,user=user,group=group)
                return JsonResponse(code="999999", msg="成功！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="执行失败！")


