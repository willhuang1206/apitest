import logging
import traceback
import xlrd
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api_test.common.confighttp import run_http
from django.conf import settings
from api_test.models import ApiInfo
from api_test.serializers import ApiInfoSerializer
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.service.autoService import getAutoActionSteps
from api_test.models import Automation,User,Project, ApiGroupLevelFirst, Group,ApiInfo, \
    ApiOperationHistory, APIRequestHistory, ApiHead, ApiParameter, ApiResponse, ApiParameterRaw, AutomationStep, Automation2Step
from api_test.serializers import ApiGroupLevelFirstSerializer, ApiInfoSerializer, APIRequestHistorySerializer, \
    ApiOperationHistorySerializer, ApiInfoListSerializer, ApiInfoDocSerializer, ApiGroupLevelFirstDeserializer, \
    ApiInfoDeserializer, ApiHeadDeserializer, ApiParameterDeserializer, \
    ApiResponseDeserializer, APIRequestHistoryDeserializer, ProjectSerializer,AutomationDeserializer

auto_url=settings.AUTO_URL

class AutomationService():
    @staticmethod
    def run_automation(api_type, url, method, headers, content_type, data, env=None,cookies=None):
        """
        根据接口类型,地址,接口参数调用接口
        :param request:
        :return: 接口返回数据
        """
        if api_type == "http":
            if env is not None:
                url=ParamUtil.replaceParam(url,json.loads(env))
            result = run_http(request_type=method, header=headers, url=url,
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

    @staticmethod
    def getAutomation(id):
        return Automation.objects.get(id=id)

    @staticmethod
    def addAutomation(data):
        project = Project.objects.get(id=data["project_id"])
        group = Group.objects.get(id=data["group_id"], project=data["project_id"])
        with transaction.atomic():
            if data["type"] in ["case","reuse"]:
                serialize = AutomationDeserializer(data=data)
                if serialize.is_valid():
                    # print("开始导入用例[%s]..." % (data["name"]))
                    serialize.save(project_id=data["project_id"], group=group)
                    if data["steps"]:
                        stepList=[]
                        currentStep={"steps":[]}
                        for step in json.loads(data["steps"]):
                            # print(step)
                            if step["group"]=="ACTION":
                                stepList.append({"name":step["action"],"steps":getAutoActionSteps(step["actionId"]),"params":step["value"],"description":step["description"]})
                            elif step["group"]=="API":
                                if "name" in currentStep:
                                    stepList.append(currentStep)
                                    currentStep={"steps":[]}
                                api=ApiInfo.objects.filter(project=data["project_id"],name=step["action"])
                                if len(api)>0:
                                    paramMap=json.loads(api[0].params)
                                    for name in paramMap:
                                        paramMap[name]="${%s,%s}" % (name,paramMap[name])
                                    currentStep={"name":step["action"],"steps":currentStep["steps"],"params":step["value"],"description":step["description"]}
                                    currentStep["steps"].append({"type":"api","name":step["action"],"actionId":api[0].id,"params":json.dumps(paramMap),"description":api[0].description,"disable":step["disable"]})
                                else:
                                    currentStep={"name":step["action"],"steps":currentStep["steps"],"params":step["value"],"description":step["description"]}
                            elif step["group"] in ["STEP"]:
                                stepList.append({"name":step["action"],"steps":[],"params":step["value"],"description":step["description"]})
                            elif step["group"] in ["COMMON"]:
                                currentStep["steps"].append({"type":step["group"].lower(),"name":step["action"],"actionId":0,"params":step["value"],"description":step["description"],"disable":step["disable"]})
                            else:
                                raise Exception("导入用例[%s]时,找不到步骤[%s]" % (data["name"],step["action"]))
                        if "name" in currentStep:
                            stepList.append(currentStep)
                        # print("保存用例步骤: " + str(stepList))
                        for i,currentStep in enumerate(stepList):
                            step=AutomationStep.objects.create(name=currentStep["name"],type="normal",steps=json.dumps(currentStep["steps"]),
                                                               params=currentStep["params"],description=currentStep["description"],
                                                               project=project,automation=serialize.data)
                            Automation2Step.objects.create(order=i+1,automation_id=serialize.data.get("id"),step=step)
                else:
                    raise Exception("用例数据校验不合法,保存失败!")
        return data

    @staticmethod
    def importFromExcel(projectId,groupId,fileName):
        # 打开文件
        data = xlrd.open_workbook('./api_test/upload/{fileName}'.format(fileName=fileName))

        table = data.sheet_by_index(0)

        totalCount=0
        passCount=0
        failCount=0
        existCount=0
        errorList=[]

        for rowNum in range(1,table.nrows):
            try:
                totalCount+=1
                rowVale = table.row_values(rowNum)
                apiNameEndIndex=rowVale[3].find('（')
                apiName=rowVale[3][0:apiNameEndIndex] if apiNameEndIndex>=0 else rowVale[3]
                objs = Automation.objects.filter(name=rowVale[4], project=projectId)
                if len(objs):
                    logging.info("已存在用例[%s]!" % rowVale[4])
                    existCount+=1
                    continue
                user = User.objects.filter(first_name=rowVale[11])
                user_id=user[0].id if len(user)>0 else 1
                params=rowVale[7]
                data={"project_id":projectId,"group_id":groupId,"name":rowVale[4],"type":"case","params":params,"user":user_id,"description":rowVale[9]}
                steps=[]
                stepLines=rowVale[9].split('\n')
                actionLines=rowVale[8].split('\n')
                for stepIndex in range(len(stepLines)):
                    stepLine=stepLines[stepIndex]
                    stepLinePre="%s、" % str(stepIndex+1)
                    if not stepLine.startswith(stepLinePre):
                        continue
                    step={"group":"STEP","action":stepLine,"value":params,"disable":"False"}
                    stepActions=[]
                    for actionIndex in range(len(actionLines)):
                        actionLine=actionLines[actionIndex]
                        actionLinePre="%s.%s、" % (str(stepIndex+1),str(actionIndex+1))
                        if not actionLine.startswith(actionLinePre):
                            if stepIndex==0:
                                actionLinePre="%s、" % (str(actionIndex+1))
                                if not actionLine.startswith(actionLinePre):
                                    continue
                                else:
                                    stepActions.append(actionLine)
                            else:
                                continue
                        else:
                            stepActions.append(actionLine[len("%s." % str(stepIndex+1)):])
                    actionLines=actionLines[len(stepActions):]
                    step["description"]='\n'.join(stepActions)
                    steps.append(step)
                data["steps"]=json.dumps(steps)
                AutomationService.addAutomation(data)
                logging.info("导入第%s行,接口名[%s],用例名[%s]" % (rowNum,apiName,rowVale[4]))
                passCount+=1
            except Exception as e:
                failCount+=1
                errorList.append(str(e))
                logging.error("导入第%s行失败!" % rowNum)
                logging.error(traceback.format_exc())
        return {"totalCount":totalCount,"passCount":passCount,"failCount":failCount,"existCount":existCount,"errorList":errorList}

# AutomationService.importFromExcel(9,29,"潍坊银行接口用例-ones导入版.xlsx")

