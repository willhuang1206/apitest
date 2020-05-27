import logging
import traceback
import ast
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from api_test.common.auth import TokenAuthentication
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.service.runService import RunService
from api_test.service.taskService import TaskService
from api_test.service.publishService import PublishService
from api_test.service.commandService import CommandService
from api_test.common.auth import permission_required
from api_test.models import Project, Group, Automation, AutomationTask,AutomationStep, ApiInfo, Automation2Step,\
    AutomationList2Automation,AutomationResult,ProjectConfig,PublishConfig
from api_test.serializers import ProjectSerializer,ApiInfoSerializer, AutomationSerializer, AutomationListSerializer,AutomationDeserializer, \
    AutomationTaskSerializer,AutomationStepSerializer,AutomationResultSerializer,GroupSerializer,Automation2StepSerializer,\
    AutomationList2AutomationSerializer,AutomationTaskDeserializer,PublishConfigSerializer,PublishConfigDeserializer

class GroupList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取分组
        :return:
        """
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
        groups = getSubGroups(project_id)
        return JsonResponse(data=groups, code="999999", msg="成功！")

def getSubGroups(project_id,groupId=None):
    subGroups=[]
    if groupId:
        groups = Group.objects.filter(project=project_id,parent=groupId).order_by("id")
    else:
        groups = Group.objects.filter(project=project_id,parent__isnull=True).order_by("id")
    for group in groups:
        groupInfo={"id":str(group.id),"label":group.name,"value":{"path":"/autolist/project=%s/group=%s" % (project_id,group.id)}}
        childGroups=getSubGroups(project_id,group.id)
        if len(childGroups)>0:
            groupInfo["children"]=childGroups
        subGroups.append(groupInfo)
    return subGroups

class AddGroup(APIView):
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
            # 必传参数 name, host
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("add_automationgroup")
    def post(self, request):
        """
        新增分组
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            parent = Group.objects.get(id=data["parent_id"])
        except ObjectDoesNotExist:
            parent=None
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project=obj,parent=parent)
        else:
            return JsonResponse(code="999998", msg="失败！")
        record_dynamic(project=serializer.data.get("id"),
                       _type="添加", operationObject="分组", user=request.user.pk,
                       data="新增分组“%s”" % data["name"])
        return JsonResponse(data={
            "group_id": serializer.data.get("id")
        }, code="999999", msg="成功！")


class DelGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("delete_automationgroup")
    def post(self, request):
        """
        删除分组
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = Group.objects.filter(id=data["id"], project=data["project_id"])
        if obi:
            name = obi[0].name
            obi.delete()
        else:
            return JsonResponse(code="999991", msg="分组不存在！")
        record_dynamic(project=data["project_id"],
                       _type="删除", operationObject="分组", user=request.user.pk, data="删除分组“%s”" % name)
        return JsonResponse(code="999999", msg="成功！")


class UpdateNameGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, host
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automationgroup")
    def post(self, request):
        """
        修改分组名称
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Group.objects.get(id=data["id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)
        else:
            return JsonResponse(code="999998", msg="失败！")
        record_dynamic(project=serializer.data.get("id"),
                       _type="修改", operationObject="分组", user=request.user.pk,
                       data="修改分组“%s”" % data["name"])
        return JsonResponse(code="999999", msg="成功！")


class UpdateGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["ids"] or not data["group_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list) \
                    or not isinstance(data["group_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automationgroup")
    def post(self, request):
        """
        修改用例分组
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = Group.objects.get(id=data["group_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        id_list = Q()
        for i in data["ids"]:
            id_list = id_list | Q(id=i)
        case_list = Automation.objects.filter(id_list, project=data["project_id"])
        with transaction.atomic():
            case_list.update(group=obj)
            name_list = []
            for j in case_list:
                name_list.append(str(j.name))
            record_dynamic(project=data["project_id"],
                           _type="修改", operationObject="用例", user=request.user.pk, data="修改用例分组，列表“%s”" % name_list)
            return JsonResponse(code="999999", msg="成功！")

class AutomationList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化列表
        :param request:
        :return:
        """
        try:
            page = int(request.GET.get("page", 1))
            project_id = request.GET.get("project_id")
            automation_id = request.GET.get("automation_id")
            group_id = request.GET.get("first_group_id")
            type = request.GET.get("type")
            name = request.GET.get("name")
            exclude = ast.literal_eval(request.GET.get("exclude","[]"))
            page_size = int(request.GET.get("page_size", 20)) if not group_id else 100
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
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
        if automation_id:
            automation=Automation.objects.get(id=automation_id)
            obis=automation.automations.all().order_by("id")
        else:
            if group_id:
                if not group_id.isdecimal():
                    return JsonResponse(code="999996", msg="参数有误！")
                if name and type:
                    obis = Automation.objects.filter(Q(name__contains=name)|Q(publish__contains="'%s'" % name),project=project_id,group=group_id, type=type).exclude(id__in=exclude).order_by("-id")
                elif name:
                    obis = Automation.objects.filter(Q(name__contains=name)|Q(publish__contains="'%s'" % name),project=project_id,group=group_id).exclude(id__in=exclude).order_by("-id")
                elif type:
                    obis = Automation.objects.filter(project=project_id, type=type,group=group_id).exclude(id__in=exclude).order_by("-id")
                else:
                    obis = Automation.objects.filter(project=project_id,group=group_id).exclude(id__in=exclude).order_by("-id")
            else:
                if name and type:
                    obis = Automation.objects.filter(Q(name__contains=name)|Q(group__name=name)|Q(publish__contains="'%s'" % name),project=project_id, type=type).exclude(id__in=exclude).order_by("-id")
                elif name:
                    obis = Automation.objects.filter(Q(name__contains=name)|Q(group__name=name)|Q(publish__contains="'%s'" % name),project=project_id).exclude(id__in=exclude).order_by("-id")
                elif type:
                    obis = Automation.objects.filter(project=project_id, type=type).exclude(id__in=exclude).order_by("-id")
                else:
                    obis = Automation.objects.filter(project=project_id).exclude(id__in=exclude).order_by("-id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(obis)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = AutomationListSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "page_size":page_size,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["name"] or not data["group_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["group_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("add_automation")
    def post(self, request):
        """
        添加用例
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        data["user"]=request.user.pk
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(project)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        name = Automation.objects.filter(name=data["name"], project=data["project_id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            with transaction.atomic():
                try:
                    serialize = AutomationDeserializer(data=data)
                    if serialize.is_valid():
                        try:
                            group = Group.objects.get(id=data["group_id"], project=data["project_id"])
                            serialize.save(project=project, group=group, user=request.user)
                            if data["copyId"]:
                                if data["type"] in ("case","reuse","data"):
                                    steps=Automation.objects.get(id=data["copyId"]).steps.all().order_by("automation2step__order")
                                    for i, step in enumerate(steps):
                                        if step.type=="normal":
                                            step.id=None
                                            step.save()
                                        Automation2Step.objects.create(order=i+1,automation_id=serialize.data.get("id"),step=step)
                                elif data["type"]=="list":
                                    automations=AutomationList2Automation.objects.filter(automationParent_id=data["copyId"],status=True).order_by("order")
                                    for i, automation in enumerate(automations):
                                        AutomationList2Automation.objects.create(order=i+1,automationParent_id=serialize.data.get("id"),automationStep=automation.automationStep)
                                elif data["type"]=="monitor":
                                    apis=Automation.objects.get(id=data["copyId"]).apis.all()
                                    automation=Automation.objects.get(id=serialize.data.get("id"))
                                    for i, api in enumerate(apis):
                                        automation.apis.add(api)
                        except KeyError:
                            serialize.save(project=project, user=request.user)
                        record_dynamic(project=data["project_id"],
                                       _type="新增", operationObject="自动化", user=request.user.pk,
                                       data="新增自动化\"%s\"" % data["name"])
                        return JsonResponse(data={"automation_id": serialize.data.get("id")},
                                            code="999999", msg="成功！")
                    return JsonResponse(code="999996", msg="参数有误！")
                except:
                    logging.error(traceback.format_exc())
                    return JsonResponse(code="999998", msg="失败！")


class UpdateAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["name"] or not data["id"] \
                    or not data["group_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int) \
                    or not isinstance(data["group_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automation")
    def post(self, request):
        """
        修改自动化
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        try:
            automation = Automation.objects.get(id=data["id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="自动化用例不存在！")
        try:
            Group.objects.get(id=data["group_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        name = Automation.objects.filter(name=data["name"], project=data["project_id"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            try:
                serialize = AutomationDeserializer(data=data)
                if serialize.is_valid():
                    data["user_id"] = request.user.pk
                    serialize.update(instance=automation, validated_data=data)
                    if "orders" in data:
                        orders=data["orders"]
                        for index,id in enumerate(orders):
                            if automation.type in ("case","reuse"):
                                Automation2Step.objects.filter(id=id).update(order=index+1)
                            elif automation.type in ("list"):
                                AutomationList2Automation.objects.filter(id=id).update(order=index+1)
                    record_dynamic(project=data["project_id"],
                                   _type="修改", operationObject="自动化", user=request.user.pk, data="修改自动化\"%s\"" % data["name"])
                    return JsonResponse(code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")
            except:
                logging.error(traceback.format_exc())


class DelAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("delete_automation")
    def post(self, request):
        """
        删除用例
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        project = ProjectSerializer(project)
        if not project.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            for j in data["ids"]:
                with transaction.atomic():
                    obi = Automation.objects.filter(id=j, project=data['project_id'])
                    if len(obi) != 0:
                        name = obi[0].name
                        if obi[0].type in ("case","reuse","data"):
                            steps=obi[0].steps.all()
                            for step in steps:
                                if step.type=="normal":
                                    step.delete()
                        obi.delete()
                        record_dynamic(project=data["project_id"],
                                       _type="删除", operationObject="自动化", user=request.user.pk, data="删除自动化\"%s\"" % name)
        except Exception:
            logging.error(traceback.format_exc())
        return JsonResponse(code="999999", msg="成功！")


class StepList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例步骤列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 1000))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")

        if request.GET.get("automation_id"):
            automation_id = request.GET.get("automation_id")
            if not automation_id.isdecimal():
                return JsonResponse(code="999996", msg="参数有误！")
            try:
                automation=Automation.objects.get(id=automation_id)
            except ObjectDoesNotExist:
                return JsonResponse(code="999987", msg="自动化不存在！")
            if automation.type in ("case","reuse","data"):
                steps=Automation2Step.objects.filter(automation=automation).order_by("order")
                # steps=automation.steps.all().order_by("automation2step__order")
                steps=Automation2StepSerializer(steps, many=True).data
                results=AutomationResult.objects.filter(automation=automation_id,step=None).order_by("-id")[:10].values("trace","result","testTime")
            elif automation.type=="list":
                steps=AutomationList2Automation.objects.filter(automationParent=automation).order_by("order")
                steps=AutomationList2AutomationSerializer(steps, many=True).data
                results=AutomationResult.objects.filter(automation=automation_id,step=None).order_by("-id")[:10].values("trace","result","testTime")
            elif automation.type=="monitor":
                steps=automation.apis.all().order_by("id")
                steps=ApiInfoSerializer(steps, many=True).data
                results=AutomationResult.objects.filter(automation=automation_id,api=None).order_by("-id")[:10].values("trace","result","testTime")
            # step = AutomationStep.objects.filter(automation=automation_id).order_by("id")
            return JsonResponse(data={"steps": steps,
                                      "automation": AutomationSerializer(automation).data,
                                      "results":results,
                                      }, code="999999", msg="成功！")
        else:
            project_id = int(request.GET.get("project_id"))
            # automation_id = int(request.GET.get("automation_id"))
            steps = AutomationStep.objects.filter(Q(type="project",project=project_id)|Q(type="global")).order_by("id")
            paginator = Paginator(steps, page_size)  # paginator对象
            pages = paginator.num_pages  # 总页数
            total = len(steps)
            try:
                obm = paginator.page(page)
            except PageNotAnInteger:
                obm = paginator.page(1)
            except EmptyPage:
                obm = paginator.page(paginator.num_pages)
            serialize = AutomationStepSerializer(obm, many=True)
            return JsonResponse(data={"data": serialize.data,
                                      "page": page,
                                      "pages": pages,
                                      "total": total
                                      }, code="999999", msg="成功！")

class StepInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取步骤详细信息
        :param request:
        :return:
        """
        automation_id = request.GET.get("automation_id")
        step_id = request.GET.get("step_id")
        if not automation_id.isdecimal() or not step_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            Automation.objects.get(id=automation_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="用例不存在！")
        try:
            obm = AutomationStep.objects.get(id=step_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="步骤不存在！")
        data = AutomationStepSerializer(obm).data
        return JsonResponse(data=data, code="999999", msg="成功！")


class AddStep(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            if not data["name"] or not data["type"] or not data["steps"] or not data["order"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not data["automation_id"] or not data["project_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["type"] not in ["normal","project","global"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automation")
    def post(self, request):
        """
        新增用例步骤
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        data["user"] = request.user.pk
        if result:
            return result
        with transaction.atomic():
            try:
                project=Project.objects.get(id=data["project_id"])
                automation = Automation.objects.get(id=data["automation_id"])
                step=AutomationStep.objects.create(name=data["name"],type=data["type"],steps=data["steps"],
                                                   params=data["params"],description=data["description"],
                                                   project=project,automation=automation)
                Automation2Step.objects.create(order=data["order"],automation=automation,step=step)
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(data={"step_id": step.id},code="999999", msg="成功！")

class StepStatusUpdate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        修改用例步骤
        :param request:
        :return:
        """
        data = request.data

        with transaction.atomic():
            try:
                if data["type"] in ("case","reuse","data"):
                    AutomationList2Automation.objects.filter(id=data["id"]).update(status=data["status"])
                else:
                    Automation2Step.objects.filter(id=data["id"]).update(status=data["status"])
                return JsonResponse(code="999999", msg="成功！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败！")

class UpdateStep(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["name"] or not data["type"] or not data["steps"] or not data["order"] or not data["id"] or not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            if not data["automation_id"] or not data["project_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["type"] not in ["normal","project","global"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automation")
    def post(self, request):
        """
        修改用例步骤
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # try:
        #     step = AutomationStep.objects.get(id=data["id"])
        # except ObjectDoesNotExist:
        #     return JsonResponse(code="999990", msg="步骤不存在！")
        if data["type"]=="project":
            name = AutomationStep.objects.filter(name=data["name"], project=data["project_id"],type="project").exclude(id=data["id"])
            if len(name):
                return JsonResponse(code="999997", msg="存在相同名称！")
        if data["type"]=="global":
            name = AutomationStep.objects.filter(name=data["name"], type="global").exclude(id=data["id"])
            if len(name):
                return JsonResponse(code="999997", msg="存在相同名称！")
        with transaction.atomic():
            try:
                AutomationStep.objects.filter(id=data["id"]).update(name=data["name"],type=data["type"],steps=str(data["steps"]),
                                                       params=data["params"],description=data["description"])
                return JsonResponse(code="999999", msg="成功！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败！")

class DelStep(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["ids"] or not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    @permission_required("change_automation")
    def post(self, request):
        """
        删除用例步骤
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        automation=Automation.objects.get(id=data["automation_id"])
        for item in data["ids"]:
            step=AutomationStep.objects.get(id=item["id"])
            if step is not None:
                # automation.steps.remove(step)
                Automation2Step.objects.filter(automation=automation,step=step,order=item["order"]).delete()
                if step.type=="normal":
                    step.delete()
        steps=Automation2Step.objects.filter(automation=automation).order_by("order")
        order=0
        for step in steps:
            order+=1
            step.order=order
            # step.update(order=order)
            step.save()
        return JsonResponse(code="999999", msg="成功！")


class AddReuseStep(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        新增可重用用例步骤
        :param request:
        :return:
        """
        data = request.data
        if not data["automation_id"] or not data["project_id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        with transaction.atomic():
            try:
                automation = Automation.objects.get(id=data["automation_id"])
                order=len(automation.steps.all())
                for id in data["ids"]:
                    order=order+1
                    step = AutomationStep.objects.get(id=id)
                    Automation2Step.objects.create(order=order,automation=automation,step=step)
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(code="999999", msg="成功！")


class LinkApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        关联接口
        :param request:
        :return:
        """
        data = request.data
        if not data["automation_id"] or not data["project_id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        with transaction.atomic():
            try:
                automation = Automation.objects.get(id=data["automation_id"])
                for id in data["ids"]:
                    api = ApiInfo.objects.get(id=id)
                    automation.apis.add(api)
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(code="999999", msg="成功！")


class UnlinkApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        取消关联接口
        :param request:
        :return:
        """
        data = request.data
        if not data["automation_id"] or not data["project_id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        with transaction.atomic():
            try:
                automation = Automation.objects.get(id=data["automation_id"])
                for id in data["ids"]:
                    api = ApiInfo.objects.get(id=id)
                    automation.apis.remove(api)
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(code="999999", msg="成功！")


class LinkAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        关联用例
        :param request:
        :return:
        """
        data = request.data
        if not data["automation_id"] or not data["project_id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        with transaction.atomic():
            try:
                automationParent = Automation.objects.get(id=data["automation_id"])
                order=len(automationParent.automations.all())
                for id in data["ids"]:
                    order=order+1
                    automationStep = Automation.objects.get(id=id)
                    AutomationList2Automation.objects.create(order=order,automationParent=automationParent,automationStep=automationStep)
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(code="999999", msg="成功！")

class UnlinkAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        取消关联用例
        :param request:
        :return:
        """
        data = request.data
        if not data["automation_id"] or not data["project_id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        with transaction.atomic():
            try:
                automationParent = Automation.objects.get(id=data["automation_id"])
                # order=len(automationParent.automations.all())
                for id in data["ids"]:
                    # order=order+1
                    automationStep = Automation.objects.get(id=id)
                    AutomationList2Automation.objects.filter(automationParent=automationParent,automationStep=automationStep).delete()
            except Exception:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="参数有误！")
            return JsonResponse(code="999999", msg="成功！")

class RunAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        执行测试用例
        :param request:
        :return:
        """
        data = request.data

        try:
            logging.info("Run automation with data: {data}".format(data=json.dumps(data)))
            trace=datetime.now().strftime('%Y%m%d%H%M%S%f')
            paramMap={}
            envMap={}
            ids=data["ids"] if "ids" in data else None
            result={}

            if "automation_id" in data:
                automation = Automation.objects.get(id=data["automation_id"])
                projectId=automation.project.id
                if json.is_json(data["env"]):
                    envMap=json.loads(data["env"])
                else:
                    env="集成" if data["env"]==1 else "预发布" if data["env"]==2 else "线上" if data["env"]==3 else data["env"]
                    obi = ProjectConfig.objects.filter(project=projectId,name=env,type="env").order_by("-id")
                    if len(obi)>0:
                        envMap=json.loads(obi[0].value)
                context={"project":projectId,"ids":ids,"result":{},"details":[],"status":"RUNNING","trace":trace,"env":envMap["env"] if "env" in envMap else "","envMap":envMap,"user": request.user.pk if request.user.pk else 1}
                context["debug"]=True
                if "params" in data:
                    paramMap=json.loads(data["params"])
                    if "data" in data and len(data["data"])>0:
                        obis = ProjectConfig.objects.filter(project=projectId,name__in=data["data"],type="data")
                        for obi in obis:
                            paramMap=ParamUtil.replaceMap(paramMap,json.loads(obi.value))
                context["value"]=paramMap
                if automation.type=="list":
                    thread=RunService.run_automationlist(automation,context)
                    result=thread.result
                else:
                    thread=RunService.run_automation(automation,context)
                    result=thread.result
                record_dynamic(project=projectId,_type="执行", operationObject="自动化用例", user=request.user.pk,data="执行自动化用例[%s]" % automation.name)
            elif "publish" in data:
                env="集成" if data["env"]==1 else "预发布" if data["env"]==2 else "线上" if data["env"]==3 else data["env"]
                publish = PublishConfig.objects.filter(name=data["publish"],env=env,status=True)
                if len(publish)==0:
                    return JsonResponse(data={}, code="999990", msg="没有满足条件的发布项目配置！")
                publish=publish[0]
                projectId=publish.project.id
                obi = ProjectConfig.objects.filter(project=projectId,name=env,type="env").order_by("-id")
                if len(obi)>0:
                    envMap=json.loads(obi[0].value)
                context={"project":projectId,"ids":ids,"result":{},"details":[],"status":"RUNNING","trace":trace,"env":envMap["env"] if "env" in envMap else "","envMap":envMap,"user": request.user.pk if request.user.pk else 1}
                publishId=data["id"] if "id" in data else None
                paramMap=json.loads(publish.params)
                context["value"]=paramMap
                result=PublishService.run_test(publish,publishId,context)
        except Exception as e:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="执行失败! 异常信息: %s" % str(e))
        return JsonResponse(data=result, code="999999", msg="成功！")

class ResultList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例执行结果
        :param request:
        :return:
        """

        if request.GET.get("automation_id"):
            automation_id = request.GET.get("automation_id")
            trace=request.GET.get("trace")
            if not automation_id.isdecimal():
                return JsonResponse(code="999996", msg="参数有误！")
            try:
                automation=Automation.objects.get(id=automation_id)
            except ObjectDoesNotExist:
                return JsonResponse(code="999987", msg="自动化不存在！")
            automation_result=RunService.getAutomationResult(automation,trace)
            return JsonResponse(data=automation_result, code="999999", msg="成功！")
        else:
            trace=request.GET.get("trace")
            automation_result=RunService.getPublishResult(trace)
            return JsonResponse(data=automation_result, code="999999", msg="成功！")

class CommandList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取操作列表
        :param request:
        :return:
        """
        commands=CommandService.get_all_commands()
        project_id = request.GET.get("project_id")
        automation_id = request.GET.get("automation_id")
        if not project_id:
            return JsonResponse(code="999996", msg="参数有误!")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在!")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        apis = ApiInfo.objects.filter(project=project_id).order_by("-id")
        for apiInfo in apis:
            command={"name":apiInfo.name,"type":"api","desc":apiInfo.description,"alias":apiInfo.name,"value":apiInfo.params,"actionId":apiInfo.id}
            commands.append(command)
        automations = Automation.objects.filter(project=project_id,type="reuse").exclude(id=automation_id).order_by("-id")
        for automation in automations:
            command={"name":automation.name,"type":"automation","desc":automation.description,"alias":automation.name,"value":automation.params,"actionId":automation.id}
            commands.append(command)

        return JsonResponse(data={"data": commands}, code="999999", msg="成功!")


class TaskList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化任务列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        automation_id = request.GET.get("automation_id")
        name = request.GET.get("name")
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
        if automation_id:
            if name:
                tasks=AutomationTask.objects.filter(project=project_id, automation=automation_id,name__contains=name).order_by("-id")
            else:
                tasks=AutomationTask.objects.filter(project=project_id, automation=automation_id).order_by("-id")
        else:
            if name:
                tasks=AutomationTask.objects.filter(project=project_id, name__contains=name).order_by("-id")
            else:
                tasks=AutomationTask.objects.filter(project=project_id).order_by("-id")
        paginator = Paginator(tasks, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(tasks)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = AutomationTaskSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("add_task")
    def post(self, request):
        """
        添加任务
        :param request:
        :return:
        """
        data = request.data
        data["user"] = request.user.pk
        name = AutomationTask.objects.filter(name=data["name"], project=data["project_id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            with transaction.atomic():
                try:
                    serialize = AutomationTaskDeserializer(data=data)
                    if serialize.is_valid():
                        try:
                            project = Project.objects.get(id=data["project_id"])
                            serialize.save(project=project)
                            task=AutomationTask.objects.get(id=serialize.data.get("id"))
                            if data["status"]:
                                TaskService.start_task(task)
                        except Exception as e:
                            logging.exception(e)
                            traceback.print_exc()
                            return JsonResponse(code="999998", msg="失败！")
                        record_dynamic(project=data["project_id"],
                                       _type="新增", operationObject="自动化任务", user=request.user.pk,
                                       data="新增自动化任务\"%s\"" % data["name"])
                        return JsonResponse(data={"task_id": serialize.data.get("id")},
                                            code="999999", msg="成功！")
                    return JsonResponse(code="999996", msg="参数有误！")
                except:
                    logging.error(traceback.format_exc())
                    return JsonResponse(code="999998", msg="失败！")


class UpdateTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        修改自动化任务
        :param request:
        :return:
        """
        data = request.data
        if not data["project_id"] or not data["name"] or not data["id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        project = ProjectSerializer(project)
        if not project.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            task = AutomationTask.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="自动化任务不存在！")
        name = AutomationTask.objects.filter(name=data["name"], project=data["project_id"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            try:
                serialize = AutomationTaskDeserializer(data=data)
                if serialize.is_valid():
                    serialize.update(instance=task,validated_data=data)
                    # serialize.save()
                    if data["status"]:
                        TaskService.start_task(task)
                    else:
                        TaskService.stop_task(task)
                    return JsonResponse(code="999999", msg="成功！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败！")


class DelTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("delete_task")
    def post(self, request):
        """
        删除任务
        :param request:
        :return:
        """
        data = request.data
        if not data["project_id"] or not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
        if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list):
            return JsonResponse(code="999996", msg="参数有误！")
        for i in data["ids"]:
            if not isinstance(i, int):
                return JsonResponse(code="999996", msg="参数有误！")
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        project = ProjectSerializer(project)
        if not project.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        for j in data["ids"]:
            task = AutomationTask.objects.filter(id=j, project=data['project_id'])
            if len(task) != 0:
                name = task[0].name
                TaskService.stop_task(task[0])
                task.delete()
                record_dynamic(project=data["project_id"],
                               _type="删除", operationObject="自动化任务", user=request.user.pk, data="删除自动化任务\"%s\"" % name)
        return JsonResponse(code="999999", msg="成功！")


class StopTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        停止任务
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            task = AutomationTask.objects.get(id=data["id"])
            task.status = False
            task.save()
            TaskService.stop_task(task)
            record_dynamic(project=data["project_id"],
                           _type="禁用", operationObject="任务", user=request.user.pk, data=task.name)
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="任务不存在！")

class StartTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        启动任务
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            task = AutomationTask.objects.get(id=data["id"])
            task.status = True
            task.save()
            TaskService.start_task(task)
            record_dynamic(project=data["project_id"],
                           _type="启用", operationObject="任务", user=request.user.pk, data=task.name)
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="任务不存在！")

class RunTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # @permission_required("run_task")
    def post(self, request):
        """
        执行任务
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            task = AutomationTask.objects.get(id=data["id"])
            task.sendEmail=data["sendEmail"]
            task.emails=data["emails"]
            context={"project":task.project.id,"result":{},"details":[],"status":"RUNNING","user": request.user.pk if request.user.pk else 1}
            TaskService.run_task(task,context)
            record_dynamic(project=data["project_id"],
                           _type="执行", operationObject="任务", user=request.user.pk, data=task.name)
            return JsonResponse(code="999999", msg="成功")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="失败！")

class PublishConfigList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取发布项目配置列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        name = request.GET.get("name")
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
        if name:
            publishs=PublishConfig.objects.filter(project=project_id, name__contains=name).order_by("-id")
        else:
            publishs=PublishConfig.objects.filter(project=project_id).order_by("-id")
        paginator = Paginator(publishs, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(publishs)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = PublishConfigSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddPublishConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("add_task")
    def post(self, request):
        """
        添加发布项目配置
        :param request:
        :return:
        """
        data = request.data
        data["user"] = request.user.pk
        with transaction.atomic():
            try:
                serialize = PublishConfigDeserializer(data=data)
                if serialize.is_valid():
                    project = Project.objects.get(id=data["project_id"])
                    serialize.save(project=project)
                    record_dynamic(project=data["project_id"],
                                   _type="新增", operationObject="发布项目配置", user=request.user.pk,
                                   data="新增发布项目配置:\"%s\",测试环境:\"%s\"" % (data["name"],data["env"]))
                    return JsonResponse(data={"id": serialize.data.get("id")},
                                        code="999999", msg="成功！")
                return JsonResponse(code="999996", msg="参数有误！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败！")


class UpdatePublishConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        修改发布项目配置
        :param request:
        :return:
        """
        data = request.data
        if not data["project_id"] or not data["name"] or not data["id"]:
            return JsonResponse(code="999996", msg="参数有误！")
        if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        project = ProjectSerializer(project)
        if not project.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            publish = PublishConfig.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="发布项目配置不存在！")
        try:
            serialize = PublishConfigDeserializer(data=data)
            if serialize.is_valid():
                serialize.update(instance=publish,validated_data=data)
                # serialize.save()
                return JsonResponse(code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")


class DelPublishConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("delete_task")
    def post(self, request):
        """
        删除发布项目配置
        :param request:
        :return:
        """
        data = request.data
        if not data["project_id"] or not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
        if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list):
            return JsonResponse(code="999996", msg="参数有误！")
        for i in data["ids"]:
            if not isinstance(i, int):
                return JsonResponse(code="999996", msg="参数有误！")
        try:
            project = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        project = ProjectSerializer(project)
        if not project.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            for j in data["ids"]:
                publish = PublishConfig.objects.filter(id=j, project=data['project_id'])
                if len(publish) != 0:
                    name = publish[0].name
                    env=publish[0].env
                    publish.delete()
                    record_dynamic(project=data["project_id"],
                                   _type="删除", operationObject="发布项目配置", user=request.user.pk, data="删除发布项目配置:\"%s\",测试环境:\"%s\"" % (name,env))
            return JsonResponse(code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class DisablePublishConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        禁用发布项目配置
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            publish = PublishConfig.objects.get(id=data["id"])
            publish.status = False
            publish.save()
            record_dynamic(project=data["project_id"],
                           _type="禁用", operationObject="发布项目配置", user=request.user.pk, data="禁用发布项目配置:\"%s\",测试环境:\"%s\"" % (publish.name,publish.env))
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="发布项目配置不存在！")

class EnablePublishConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_task")
    def post(self, request):
        """
        启用发布项目配置
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            publish = PublishConfig.objects.get(id=data["id"])
            publish.status = True
            publish.save()
            record_dynamic(project=data["project_id"],
                           _type="启用", operationObject="发布项目配置", user=request.user.pk, data="启用发布项目配置:\"%s\",测试环境:\"%s\"" % (publish.name,publish.env))
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="发布项目配置不存在！")

class RunPublishTest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # @permission_required("run_task")
    def post(self, request):
        """
        执行发布项目测试
        :param request:
        :return:
        """
        data = request.data
        # 查找项目是否存在
        try:
            publish = PublishConfig.objects.get(id=data["publish"])
            publish.sendEmail=data["sendEmail"]
            publish.emails=data["emails"]
            trace=datetime.now().strftime('%Y%m%d%H%M%S%f')
            paramMap=json.loads(publish.params)
            env = ProjectConfig.objects.filter(project=publish.project.id,name=publish.env,type="env").order_by("-id")[0]
            envMap=json.loads(env.value)
            env=envMap["env"] if "env" in envMap else ""
            context={"project":publish.project.id,"value":paramMap,"result":{},"details":[],"status":"RUNNING","trace":trace,"env":env,"envMap":envMap,"user": request.user.pk if request.user.pk else 1}
            PublishService.run_test(publish,data["id"],context)
            record_dynamic(project=data["project_id"],
                           _type="执行", operationObject="发布项目测试", user=request.user.pk, data="测试发布项目:\"%s\",测试环境:\"%s\",上线单ID:\"%s\"" % (publish.name,publish.env,data["id"]))
            return JsonResponse(code="999999", msg="成功")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="失败！")

