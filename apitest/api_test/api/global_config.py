import logging
import traceback
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from api_test.common.auth import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.conf import settings
from api_test.common.confighttp import run_http
from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic
from api_test.common.jsonUtil import json
from api_test.common.auth import permission_required
from api_test.models import GlobalConfig
from api_test.serializers import GlobalConfigSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class GlobalConfigList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取配置列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")
        name = request.GET.get("name")
        type = request.GET.get("type")
        if name and type:
            obis = GlobalConfig.objects.filter(name__contains=name,type=type).order_by("-id")
        elif name:
            obis = GlobalConfig.objects.filter(name__contains=name).order_by("-id")
        elif type:
            obis = GlobalConfig.objects.filter(type=type).order_by("-id")
        else:
            obis = GlobalConfig.objects.filter().order_by("-id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(obis)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = GlobalConfigSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddGlobalConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, value,type
            if not data["name"] or not data["value"] or not data["type"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        添加Config
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        obi = GlobalConfig.objects.filter(name=data["name"], type=data["type"])
        if obi:
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = GlobalConfigSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.save()
                    return JsonResponse(data={
                        "config_id": serializer.data.get("id")
                    }, code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class UpdateGlobalConfig(APIView):
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
            if not isinstance(data["id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
            # 必传参数 name, host
            if not data["name"] or not data["value"] or not data["type"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        修改配置
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obi = GlobalConfig.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="配置不存在！")
        config_name = GlobalConfig.objects.filter(name=data["name"],type=data["type"]).exclude(id=data["id"])
        if len(config_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = GlobalConfigSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.update(instance=obi, validated_data=data)
                    return JsonResponse(code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class DelGlobalConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            if not isinstance(data["ids"], list):
                for i in data["ids"]:
                    if not isinstance(i, int):
                        return JsonResponse(code="999995", msg="参数有误！")
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        删除配置
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for j in data["ids"]:
                obj = GlobalConfig.objects.filter(id=j)
                if obj:
                    name = obj[0].name
                    obj.delete()
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")


class DisableGlobalConfig(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            if not isinstance(data["config_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        禁用Config
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = GlobalConfig.objects.get(id=data["config_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="config不存在")
        obj.status = False
        obj.save()
        return JsonResponse(code="999999", msg="成功！")


class EnableGlobalConfig(APIView):
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
            if not isinstance(data["config_id"], int):
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    @permission_required("")
    def post(self, request):
        """
        启用配置
        :param request:
        :return:
        """
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = GlobalConfig.objects.get(id=data["config_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="config不存在")
        obj.status = True
        obj.save()
        return JsonResponse(code="999999", msg="成功！")

class PublishList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取发布项目列表
        :param request:
        :return:
        """
        try:
            publish_list_url=settings.PUBLISH_LIST_URL
            publishList={}
            response=requests.get(url=publish_list_url)
            if response.status_code == 200:
                response=response.json()
                publishList={publish["name"] for publish in response["data"]["data"]}

        except Exception as e:
            logging.exception(e)
        return JsonResponse(data=list(publishList), code="999999", msg="成功！")
