import logging
import traceback
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api_test.common.confighttp import run_http
from django.conf import settings
from api_test.models import ApiInfo
from api_test.serializers import ApiInfoSerializer
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.models import User,Project, ApiGroupLevelFirst, ApiInfo, \
    ApiOperationHistory, APIRequestHistory, ApiHead, ApiParameter, ApiResponse, ApiParameterRaw
from api_test.serializers import ApiGroupLevelFirstSerializer, ApiInfoSerializer, APIRequestHistorySerializer, \
    ApiOperationHistorySerializer, ApiInfoListSerializer, ApiInfoDocSerializer, ApiGroupLevelFirstDeserializer, \
    ApiInfoDeserializer, ApiHeadDeserializer, ApiParameterDeserializer, \
    ApiResponseDeserializer, APIRequestHistoryDeserializer, ProjectSerializer

auto_url=settings.AUTO_URL
executor = ThreadPoolExecutor(max_workers=1)

def match(expect,actual):
    result=False
    try:
        if expect.isnumeric():
            result=float(expect)==float(actual)
        else:
            result=str(expect)==str(actual)
            if not result and re.fullmatch(expect, str(actual)):
                result=True
    except:
        pass
    return result

def run_api(api_type, url, method, headers, content_type, data, env,cookies):
    """
    根据接口类型,地址,接口参数调用接口
    :param request:
    :return: 接口返回数据
    """
    if api_type == "http":
        if env is not None:
            url=ParamUtil.replaceParam(url,json.loads(env))
        result = run_http(request_type=method.upper(), header=headers, url=url,
                          request_parameter_type=content_type, parameter=data,cookies=cookies)
    else:
        params = {"url": url, "type": api_type, "method": method, "contentType": content_type,
                  "headers": json.dumps(headers), "data": json.dumps(data)}
        if env is not None:
            params["env"] = env
        result = run_http(request_type="POST",
                          header={"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'},
                          url="%s/api/run_api" % auto_url,
                          request_parameter_type="application/json", parameter=params,cookies=cookies)
    return result

class ApiService():
    @staticmethod
    def get_api_by_name(project_id,api_name):
        api=ApiInfo.objects.filter(name=api_name, project=project_id)
        if len(api):
            return api[0]
        else:
            return None

    @staticmethod
    def get_api_by_id(project_id,api_id):
        api=ApiInfo.objects.get(id=api_id, project=project_id)
        return api

    @staticmethod
    def run_api(api_type, url, method, headers, content_type, data, env=None,cookies=None):
        task = executor.submit(run_api, api_type, url, method, headers, content_type, data, env,cookies)
        return task.result()

    @staticmethod
    def run_api_by_id(id, value,cookies):
        """
        根据接口ID,接口参数调用接口
        :param request:
        :return: 接口返回数据
        """
        result=""
        try:
            serialize = ApiInfoSerializer(ApiInfo.objects.get(id=id))
            api=serialize.data
            headers={}
            for header in api["headers"]:
                headers[header["name"]]=header["value"]
            parameters={}
            valueMap=json.loads(value)
            for parameter in api["requestParameter"]:
                if parameter["name"]=="postData" and len(api["requestParameter"])==1:
                    if parameter["name"] in valueMap:
                        parameters=json.loads2(valueMap[parameter["name"]]) if parameter["_type"] in ("Object","Array") else valueMap[parameter["name"]]
                    else:
                        parameters=json.loads2(parameter["value"]) if parameter["_type"] in ("Object","Array") else parameter["value"]
                else:
                    if parameter["name"] in valueMap:
                        parameterValue=valueMap[parameter["name"]]
                    else:
                        parameterValue=json.loads2(parameter["value"]) if parameter["_type"] in ("Object","Array") else parameter["value"]
                    if parameterValue!="NULL":
                        parameters[parameter["name"]]=parameterValue
            api["apiAddress"]=ParamUtil.replaceParam(api["apiAddress"],json.loads(value))
            code, response_data, header_data=ApiService.run_api(api["type"], api["apiAddress"], api["requestType"],
                                      headers, api["requestParameterType"], parameters, env=value,cookies=cookies)
            assertMessage=[]
            if len(api["response"])>0:
                for response in api["response"]:
                    responseValues=json.get_values(response_data,response["name"])
                    if responseValues:
                        for value in responseValues:
                            if response["value"] and not match(response["value"],value):
                                assertMessage.append("接口返回数据参数%s实际值%s,与预期值%s不一致!" % (response["name"],value,response["value"]))
                            actualType=json.get_type(value)
                            if actualType and actualType!=response["_type"]:
                                assertMessage.append("接口返回数据参数%s实际类型%s,与预期类型%s不一致!" % (response["name"],actualType,response["_type"]))
                    elif response["required"]:
                        assertMessage.append("接口返回数据不存在必含参数%s!" % response["name"])
            result={"url":api["apiAddress"],"method":api["requestType"],"data":parameters,"response":response_data,"responseCode":code}
            if len(assertMessage)>0:
                result["assertMessage"]=str(assertMessage) if len(assertMessage)>1 else assertMessage[0]
            return result
        except Exception as e:
            logging.error(traceback.format_exc())
            raise e

    @staticmethod
    def addApi(data):
        with transaction.atomic():  # 执行错误后，帮助事物回滚
            try:
                serialize = ApiInfoDeserializer(data=data)
                if serialize.is_valid():
                    try:
                        obj = Project.objects.get(id=data["project_id"])
                        obi = ApiGroupLevelFirst.objects.get(id=data["apiGroupLevelFirst_id"], project=data["project_id"])
                        serialize.save(project=obj, apiGroupLevelFirst=obi)
                    except KeyError:
                        serialize.save(project=obj)
                    api_id = serialize.data.get("id")
                    data["id"]=api_id
                    if "headDict" in data and len(data.get("headDict"))>0:
                        for i in data["headDict"]:
                            if i.get("name"):
                                i["api"] = api_id
                                head_serialize = ApiHeadDeserializer(data=i)
                                if head_serialize.is_valid():
                                    head_serialize.save(api=ApiInfo.objects.get(id=api_id))
                    if data["requestParameterType"] in ("application/x-www-form-urlencoded","application/json","text/plain"):
                        if "requestList" in data and len(data.get("requestList")):
                            for i in data["requestList"]:
                                if i.get("name"):
                                    i["api"] = api_id
                                    param_serialize = ApiParameterDeserializer(data=i)
                                    if param_serialize.is_valid():
                                        param_serialize.save(api=ApiInfo.objects.get(id=api_id))
                    else:
                        if "requestList" in data and len(data.get("requestList")):
                            ApiParameterRaw(api=ApiInfo.objects.get(id=api_id), data=data["requestList"]).save()
                    if "responseList" in data and len(data.get("responseList")):
                        for i in data["responseList"]:
                            if i.get("name"):
                                i["api"] = api_id
                                response_serialize = ApiResponseDeserializer(data=i)
                                if response_serialize.is_valid():
                                    response_serialize.save(api=ApiInfo.objects.get(id=api_id))
                    return data
                else:
                    print("添加接口[%s]出现异常: %s" % (data["name"],serialize.error))
                    return None
            except:
                logging.error(traceback.format_exc())

    @staticmethod
    def updateApi(data):
        with transaction.atomic():
            try:
                serialize = ApiInfoDeserializer(data=data)
                if serialize.is_valid():
                    try:
                        data["userUpdate"] = User.objects.get(id=data["userUpdate"])
                        obi = ApiInfo.objects.get(id=data["id"])
                        serialize.update(instance=obi, validated_data=data)
                    except KeyError:
                        serialize.update(instance=obi, validated_data=data)
                    header = Q()
                    if "headDict" in data and len(data.get("headDict")):
                        for i in data["headDict"]:
                            if i.get("api") and i.get("id"):
                                header = header | Q(id=i["id"])
                                if i["name"]:
                                    head_serialize = ApiHeadDeserializer(data=i)
                                    if head_serialize.is_valid():
                                        i["api"] = ApiInfo.objects.get(id=i["api"])
                                        head_serialize.update(instance=ApiHead.objects.get(id=i["id"]), validated_data=i)
                            else:
                                if i.get("name"):
                                    i["api"] = data['id']
                                    head_serialize = ApiHeadDeserializer(data=i)
                                    if head_serialize.is_valid():
                                        head_serialize.save(api=ApiInfo.objects.get(id=data["id"]))
                                        header = header | Q(id=head_serialize.data.get("id"))
                    ApiHead.objects.exclude(header).filter(api=data["id"]).delete()
                    api_param = Q()
                    api_param_raw = Q()
                    if "requestList" in data and len(data.get("requestList")):
                        if data["requestParameterType"] in ("application/x-www-form-urlencoded","application/json","text/plain"):
                            ApiParameterRaw.objects.filter(api=data["id"]).delete()
                            for i in data["requestList"]:
                                if i.get("api") and i.get("id"):
                                    api_param = api_param | Q(id=i["id"])
                                    if i["name"]:
                                        param_serialize = ApiParameterDeserializer(data=i)
                                        if param_serialize.is_valid():
                                            i["api"] = ApiInfo.objects.get(id=i["api"])
                                            param_serialize.update(instance=ApiParameter.objects.get(id=i["id"]),
                                                                   validated_data=i)
                                else:
                                    if i.get("name"):
                                        i["api"] = data['id']
                                        param_serialize = ApiParameterDeserializer(data=i)
                                        if param_serialize.is_valid():
                                            param_serialize.save(api=ApiInfo.objects.get(id=data["id"]))
                                            api_param = api_param | Q(id=param_serialize.data.get("id"))
                        else:
                            try:
                                obj = ApiParameterRaw.objects.get(api=data["id"])
                                obj.data = data["requestList"]
                                obj.save()
                            except ObjectDoesNotExist:
                                obj = ApiParameterRaw(api=ApiInfo.objects.get(id=data['id']), data=data["requestList"])
                                obj.save()
                            api_param_raw = api_param_raw | Q(id=obj.id)
                    ApiParameter.objects.exclude(api_param).filter(api=data["id"]).delete()
                    ApiParameterRaw.objects.exclude(api_param_raw).filter(api=data["id"]).delete()
                    api_response = Q()
                    if "responseList" in data and len(data.get("responseList")):
                        for i in data["responseList"]:
                            if i.get("api") and i.get("id"):
                                api_response = api_response | Q(id=i["id"])
                                if i["name"]:
                                    response_serialize = ApiResponseDeserializer(data=i)
                                    if response_serialize.is_valid():
                                        i["api"] = ApiInfo.objects.get(id=i["api"])
                                        response_serialize.update(instance=ApiResponse.objects.get(id=i["id"]),
                                                                  validated_data=i)
                            else:
                                if i.get("name"):
                                    i["api"] = data['id']
                                    response_serialize = ApiResponseDeserializer(data=i)
                                    if response_serialize.is_valid():
                                        response_serialize.save(api=ApiInfo.objects.get(id=data["id"]))
                                        api_response = api_response | Q(id=response_serialize.data.get("id"))
                    ApiResponse.objects.exclude(api_response).filter(api=data["id"]).delete()
                    return data
                else:
                    print("更新接口[%s]出现异常: %s" % (data["name"],serialize.error))
                    return None
            except:
                logging.error(traceback.format_exc())

    @staticmethod
    def importFromPostman(projectId,groupId,fileName,userId):
        # 打开文件
        apiInfoList=[]
        with open('./api_test/upload/{fileName}'.format(fileName=fileName),"r") as f:
            data=json.loads(f.read())
            if "item" in data:
                apiInfoList=getApiInfoList(data["item"])

        totalCount=0
        passCount=0
        failCount=0
        existCount=0
        errorList=[]

        for index,apiInfo in enumerate(apiInfoList):
            try:
                totalCount+=1
                apiInfo.update({"apiGroupLevelFirst_id":groupId,"project_id":projectId,"type":"http","params":"{}","userUpdate":userId})
                objs = ApiInfo.objects.filter(name=apiInfo["name"], project=projectId)
                if len(objs):
                    existCount+=1
                    # apiInfo["id"]=objs[0].id
                    # ApiService.updateApi(apiInfo)
                else:
                    ApiService.addApi(apiInfo)
                    logging.info("导入第%s行,接口名[%s]" % (index+1,apiInfo["name"]))
                    passCount+=1
            except Exception as e:
                failCount+=1
                errorList.append(str(e))
                logging.error("导入第%s行失败!" % index+1)
                logging.error(traceback.format_exc())
        return {"totalCount":totalCount,"passCount":passCount,"failCount":failCount,"existCount":existCount,"errorList":errorList}

def getApiInfoList(items):
    currentList=[]
    for item in items:
        if "item" in item:
            currentList.extend(getApiInfoList(item["item"]))
        else:
            if "request" in item:
                headerList,headerDic=getHeaders(item["request"]["header"])
                apiInfo={"name":item["name"],"requestType":item["request"]["method"],"apiAddress":item["request"]["url"]["raw"],
                "requestParameterType":headerDic["Content-Type"] if "Content-Type" in headerDic else "application/json",
                "description":item["request"]["description"] if "description" in item["request"] else ""}
                apiInfo["headDict"]=headerList
                apiInfo["requestList"]=getRequests(item["request"]["body"]) if "body" in item["request"] else []
                apiInfo["responseList"]=[]
                currentList.append(apiInfo)
    return currentList

def getHeaders(headers):
    headerList=[]
    headerDic={}
    for header in headers:
        headerList.append({"name":header["name"],"value":header["value"]})
        headerDic[header["name"]]=header["value"]
    return headerList,headerDic

def getRequests(body):
    fieldList=[]
    if body["mode"]=="raw":
        fields=json.loads(body["raw"])
        for key in fields:
            fieldList.append({"name":key,"value":fields[key],"_type":json.get_type(fields[key]),"required":True,"restrict":"","description":""})
    else:
        fields=body[body["mode"]]
        for field in fields:
            fieldList.append({"name":field["key"],"value":field["value"],"_type":json.get_type(field["value"]),"required":True,"restrict":"","description":""})
    return fieldList