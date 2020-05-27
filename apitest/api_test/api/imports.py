import traceback
import time
import logging
import json
import os
from django.utils.encoding import escape_uri_path
from django.http import FileResponse
from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from api_test.service.importService import import_api,import_automation
from api_test.service.devApiService import getDevApiGroups,getChildGroups,getDevApis
from api_test.service.autoService import getApiDomainList,getActionDomainList,getAutoApis,getAutoAutomations
from api_test.service.automationService import AutomationService
from api_test.service.apiService import ApiService
from api_test.common.auth import TokenAuthentication
from api_test.common.api_response import JsonResponse
from api_test.models import ApiGroupLevelFirst, Group,ApiInfo, ApiHead, ApiParameter, ApiResponse, ApiParameterRaw,Automation,User
from api_test.serializers import ApiGroupLevelFirstSerializer, ApiInfoSerializer, ApiGroupLevelFirstDeserializer, \
    ApiInfoDeserializer, ApiHeadDeserializer, ApiParameterDeserializer, \
    ApiResponseDeserializer

def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
     time_array = time.strptime(date, format_string)
     time_stamp = int(time.mktime(time_array))*1000
     return time_stamp

class DevApiGroupList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口分组
        :param request:
        :return:
        """
        try:
            groups=getDevApiGroups()
        except:
            traceback.print_exc()
            return JsonResponse(code="999995", msg="执行失败!")
        return JsonResponse(data=groups, code="999999", msg="成功!")

class ImportDevApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        导入接口
        :param request:
        :return:
        """
        apiInfoList=[]
        data=request.data
        try:
            data["fromDate"]=date_to_timestamp(data["fromDate"]) if data["fromDate"] else ""
            data["toDate"]=date_to_timestamp(data["toDate"]) if data["toDate"] else ""
            groups=getChildGroups(data["fromGroup"])
            toGroupName=ApiGroupLevelFirst.objects.get(id=data["toGroup"]).name
            paramTypeMap={"string":"String","number":"Int","boolean":"String","object":"Object","array":"Array","file":"String"}
            responseTypeMap={"string":"String","number":"Int","boolean":"String","object":"String","array":"String"}
            for groupId in groups:
                apis=getDevApis(groupId)
                for api in apis:
                    oldApis=ApiInfo.objects.filter(name=api["name"], project=data["project_id"],apiGroupLevelFirst=data["toGroup"])
                    apiInfo={"name":api["name"],"requestType":api["options"]["method"].upper(),
                      "apiAddress":api["sitUrl"] if "sitUrl" in api and api["sitUrl"] and api["sitUrl"]!="null" else "https://${envswebHost}/Trans/test",
                      "requestParameterType":"application/json","description":api["desc"],"apiGroupLevelFirst_id":data["toGroup"],"project_id":data["project_id"],"type":"http","params":"{}","userUpdate":request.user.pk}
                    if len(oldApis)>0:
                        apiInfo["id"]=oldApis[0].id
                    headers=api["options"]["headers"]["params"]
                    if len(headers)>0:
                        apiInfo["headDict"]=[{"name":header["key"],"value":header["example"] if "example" in header else header["comment"] if "comment" in header else ""} for header in headers]
                    params=api["options"]["params"]["body"] if apiInfo["requestType"]=="POST" else api["options"]["params"]["query"]
                    if len(params)>0:
                        apiInfo["requestList"]=[{"name":param["key"],"value":param["comment"] if "comment" in param else "","_type":paramTypeMap[param["type"]],"require":param["required"],"description":""} for param in params]
                    responseParams=api["options"]["response"][0]["params"]
                    if len(responseParams)>0:
                        apiInfo["responseList"]=[{"name":param["key"],"value":param["comment"] if "comment" in param else "","_type":responseTypeMap[param["type"]],"require":param["required"],"description":""} for param in responseParams]
                    apiInfoList.append(apiInfo)
            import_api(apiInfoList,data["project_id"],request.user.pk,toGroupName)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        return JsonResponse(data=[], code="999999", msg="开始导入%s个接口!" % len(apiInfoList))

class ApiDomainList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口域列表
        :param request:
        :return:
        """
        try:
            domains = getApiDomainList()
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败!")
        return JsonResponse(data=domains, code="999999", msg="成功!")

class ActionDomainList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口域列表
        :param request:
        :return:
        """
        try:
            domains = getActionDomainList()
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败!")
        return JsonResponse(data=domains, code="999999", msg="成功!")

class ImportApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    paramTypeMap={"0":"String","1":"Array","2":"Int","3":"Object"}
    responseTypeMap={"string":"String","number":"Int","boolean":"String","object":"String","array":"String"}

    def post(self,request):

        apiInfoList=[]
        data=request.data

        try:
            data["fromDate"]=data["fromDate"] if data["fromDate"] else ""
            data["toDate"]=data["toDate"] if data["toDate"] else ""
            toGroupName=ApiGroupLevelFirst.objects.get(id=data["toGroup"]).name
            contenttypeMap = {
                "0":'application/x-www-form-urlencoded',
                "1":'application/json',
                "2":'application/xml',
                "3":'text/plain',
                "4":'multipart/form-data'
            }
            apis=getAutoApis(data["fromDate"],data["toDate"],data["fromGroup"])
            for api in apis:
                oldApis=ApiInfo.objects.filter(name=api["name"], project=data["project_id"],apiGroupLevelFirst=data["toGroup"])
                apiInfo={"name":api["name"],"requestType":api["method"],"apiAddress":api["url"],
                "requestParameterType":contenttypeMap[str(api["contenttype"])],"description":api["description"],
                "apiGroupLevelFirst_id":data["toGroup"],"project_id":data["project_id"],"type":api["type"],
                "params":"{}","userUpdate":request.user.pk}
                if len(oldApis)>0:
                    apiInfo["id"]=oldApis[0].id
                apiInfo["headDict"]=self.convertHeaders(api["headers"])
                apiInfo["requestList"],apiInfo["params"]=self.convertFields(api["fields"])
                apiInfo["responseList"]=[]
                apiInfoList.append(apiInfo)
            import_api(apiInfoList,data["project_id"],request.user.pk,toGroupName)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        return JsonResponse(data=[], code="999999", msg="开始导入%s个接口!" % len(apiInfoList))

    def convertHeaders(self,str):
        headerList=[]
        headers=str.split(',')
        for header in headers:
            headerArr=header.split('=')
            if len(headerArr)>1:
                headerList.append({"name":headerArr[0],"value":headerArr[1]})
        return headerList

    def convertFields(self,str):
        fieldList=[]
        fields=json.loads(str)
        params={}
        for field in fields:
            description=""
            if "description" in field.keys():
                description=field["description"]
            fieldList.append({"name":field["name"],"value":field["value"],"_type":self.paramTypeMap[field["type"]],"required":field["mandatory"]=="Y","restrict":"","description":description})
            if field["mandatory"]=="Y":
                if field["type"] in ("1","3"):
                    params[field["name"]]=json.loads(field["value"])
                else:
                    params[field["name"]]=field["value"]
        return fieldList,json.dumps(params)

class ImportAutomation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self,request):

        automationList=[]
        data=request.data

        try:
            typeMap = {
                "normal":'case',
                "sync":'list',
                "async":'list',
                "data":'data',
                "reuse":'reuse'
            }
            data["fromDate"]=data["fromDate"] if data["fromDate"] else ""
            data["toDate"]=data["toDate"] if data["toDate"] else ""
            toGroupName=Group.objects.get(id=data["toGroup"]).name
            automations=getAutoAutomations(data["fromDate"],data["toDate"],data["fromGroup"])
            for automation in automations:
                olds=Automation.objects.filter(name=automation["name"], project=data["project_id"],group=data["toGroup"])
                automationInfo={"name":automation["name"],"type":typeMap[automation["type"]],"steps":automation["steps"],"params":automation["params"],
                                "group_id":data["toGroup"],"project_id":data["project_id"],"description":automation["description"],"user":request.user.pk}
                if len(olds)>0:
                    for old in olds:
                        old.delete()
                automationList.append(automationInfo)
            import_automation(automationList,data["project_id"],request.user.pk,toGroupName)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        return JsonResponse(data=[], code="999999", msg="开始导入%s个用例!" % len(automationList))

class ImportApiFromPostman(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self,request):

        try:
            data=request.data
            projectId=data["project_id"]
            groupId=data["group_id"]
            fileName=data["fileName"]
            result=ApiService.importFromPostman(projectId,groupId,fileName,request.user.pk)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        return JsonResponse(data=result["errorList"], code="999999", msg="共处理{totalCount}条记录,{passCount}条导入成功,{existCount}条已存在,{failCount}条导入失败!".format(totalCount=result["totalCount"],passCount=result["passCount"],existCount=result["existCount"],failCount=result["failCount"]))

class ImportAutomationFromExcel(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self,request):

        try:
            data=request.data
            projectId=data["project_id"]
            groupId=data["group_id"]
            fileName=data["fileName"]
            result=AutomationService.importFromExcel(projectId,groupId,fileName)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        return JsonResponse(data=result["errorList"], code="999999", msg="共处理{totalCount}条记录,{passCount}条导入成功,{existCount}条已存在,{failCount}条导入失败!".format(totalCount=result["totalCount"],passCount=result["passCount"],existCount=result["existCount"],failCount=result["failCount"]))

class UploadFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self,request):
        try:
            myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return JsonResponse(code="999995", msg="获取文件失败!")
            destination = open(os.path.join("./api_test/upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():      # 分块写入文件
                destination.write(chunk)
            return JsonResponse(data=[], code="999999", msg="执行成功!")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999995", msg="执行失败")
        finally:
            destination.close()

def downloadAutoTemplate(request):
    try:
        fileName='导入接口用例模板.xlsx'
        file=open('static/%s' % fileName,'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(fileName))
        return response
    except:
        logging.error(traceback.format_exc())


