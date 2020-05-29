import logging
import threading
import requests
import traceback
import time
import ast
import copy
from django.conf import settings
from datetime import datetime
from api_test.service.apiService import ApiService
from api_test.service.automationService import AutomationService
from api_test.service.configService import getProjectConfigValueByName,getConfigValueByName,getDataMap
from api_test.models import Automation,AutomationResult,AutomationList2Automation
from api_test.common.confighttp import run_http
from api_test.common.paramUtil import ParamUtil
from api_test.common.jsonUtil import json
from api_test.common.common import record_dynamic
from api_test.common.exception import ExecutionFailException,ExecutionCheckException,LoopContinueException,LoopBreakException


class RunAutomationThread (threading.Thread):
    def __init__(self, automation,context):
        threading.Thread.__init__(self)
        self.automation = automation
        self.context = context
        self.context["ids"]=None if not "ids" in self.context else self.context["ids"]
        self.result={"type":"automation","trace":context["trace"],"name":automation.name,"status":"RUNNING","description":automation.description}

    def run(self):
        self.result=run_automation(self.automation,self.context)

class RunAutomationListThread (threading.Thread):
    def __init__(self, automationlist,context):
        threading.Thread.__init__(self)
        self.automationlist = automationlist
        self.context = context
        self.context["globalValue"]=copy.deepcopy(self.context["value"])
        self.ids=self.context["ids"] if "ids" in self.context else None
        self.context["ids"]=None
        self.result={"trace":self.context["trace"],"name":self.automationlist.name,"status":"RUNNING","failCount":0,"testtime":"","duration":0,"details":[],"description":self.automationlist.description}

    def run(self):
        automationlist_details=[]
        automationlist_status="RUNNING"
        testtime=time.time()
        self.result["testtime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime))
        self.result["details"]=automationlist_details
        failCount=0
        automations=AutomationList2Automation.objects.filter(automationParent=self.automationlist,status=True).order_by("order")
        # RunService.putRunningListResult(self.context["trace"],self.result)
        try:
            for automation in automations:
                if not self.ids or automation.automationStep.id in self.ids:
                    self.context["value"]=copy.deepcopy(self.context["globalValue"])
                    thread=RunService.run_automation(automation.automationStep, self.context)
                    thread.join()
                    automationlist_details.append(thread.result)
                    if thread.result["status"]=="FAIL":
                        failCount+=1
                        automationlist_status="FAIL"
            if automationlist_status!="FAIL":
                automationlist_status="PASS"
        except:
            logging.error(traceback.format_exc())
            automationlist_status="FAIL"
        finally:
            duration=int((time.time() - testtime)*1000)
            AutomationResult(name=self.automationlist.name,trace=self.context["trace"],result=automationlist_status,
                             project=self.automationlist.project,automation=self.automationlist,testTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),duration=duration,description=self.automationlist.description,env=self.context["env"],user_id=self.context["user"]).save()

        self.result["status"]=automationlist_status
        self.result["duration"]=duration
        self.result["failCount"]=failCount
        # RunService.removeRunningListResult(self.context["trace"])

class RunTaskAutomationsThread (threading.Thread):
    def __init__(self, task,context):
        threading.Thread.__init__(self)
        self.task = task
        self.context = context
        self.result={"trace":self.context["trace"],"name":self.task.name,"status":"RUNNING","testtime":"","duration":0,"details":[]}

    def run(self):
        automationlist_details=[]
        automationlist_status="RUNNING"
        testtime=time.time()
        failCount=0
        # RunService.putRunningListResult(self.context["trace"],self.result)
        try:
            automations=Automation.objects.filter(id__in=ast.literal_eval(self.task.automations))
            automationlist_status,failCount,automationlist_details=run_automations(automations,self.context)
        except:
            logging.error(traceback.format_exc())
            automationlist_status="FAIL"
        finally:
            duration=int((time.time() - testtime)*1000)
            totalCount=len(automationlist_details)
            passCount=totalCount-failCount
            details={"name":self.task.name,"status":automationlist_status,"totalCount":totalCount,"passCount":passCount,"failCount":failCount,"testTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),"duration":round(duration/1000,1),"env":self.context["env"]}
            AutomationResult(name=self.task.name,trace=self.context["trace"],result=automationlist_status,
                             details=json.dumps(details),project=self.task.project,testTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),duration=duration,description="",env=self.context["env"],user_id=self.context["user"]).save()

        self.result["status"]=automationlist_status
        self.result["duration"]=duration
        self.result["testtime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime))
        self.result["details"]=automationlist_details
        # RunService.removeRunningListResult(self.context["trace"])

class RunPublishAutomationThread (threading.Thread):
    def __init__(self, publish,id,automationlist,apilist,context):
        threading.Thread.__init__(self)
        self.publish=publish
        self.publishId=id
        self.name="{name},{env}环境,上线单{id}".format(name=self.publish.name,env=self.publish.env,id=self.publishId)
        self.automationlist = automationlist
        self.apilist = apilist
        self.context = context
        self.result={"trace":self.context["trace"],"name":self.name,"status":"RUNNING","testtime":"","duration":0,"details":[]}

    def run(self):
        try:
            automation_details=[]
            automation_status="RUNNING"
            testtime=time.time()
            failCount=0
            # RunService.putRunningListResult(self.context["trace"],self.result)
            automation_status,failCount,automation_details=run_automations(self.automationlist,self.context)
        except:
            logging.error(traceback.format_exc())
            automation_status="FAIL"
        finally:
            duration=int((time.time() - testtime)*1000)
            totalCount=len(automation_details)
            passCount=totalCount-failCount
            details={"name":self.publish.name,"status":automation_status,"totalCount":totalCount,"passCount":passCount,"failCount":failCount,"testTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),"duration":round(duration/1000,1),"env":self.context["env"]}
            AutomationResult(name=self.publish.name,trace=self.context["trace"],value=self.context["value"],result=automation_status,
                             project_id=self.context["project"],testTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),
                             duration=duration,env=self.context["env"],user_id=self.context["user"],
                             details=json.dumps(details),description="上线单{id}".format(id=self.publishId)).save()
            if self.publishId:
                RunService.updatePublishResult(self.publish.name,self.publishId,automation_status,self.context["trace"],self.context["project"],self.context["user"])

        self.result["status"]=automation_status
        self.result["duration"]=duration
        self.result["testtime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime))
        self.result["details"]=automation_details
        # RunService.removeRunningListResult(self.context["trace"])

def run_automations(automations,context):
    try:
        thread_config=getConfigValueByName("thread.%s" % str(context["project"]),"false")
        threads=[]
        failCount=0
        automations_details=[]
        automations_status="RUNNING"
        for automation in automations:
            if automation.type=="list":
                currentContext=copy.deepcopy(context)
                thread=RunService.run_automationlist(automation,currentContext)
                if thread_config=="true":
                    threads.append(thread)
                else:
                    thread.join()
                    result=thread.result
                    automations_details.extend(result["details"])
                    if result["status"]=="FAIL":
                        failCount+=result["failCount"]
                        automations_status="FAIL"
            elif automation.type in ["case","reuse","data","monitor"]:
                thread=RunService.run_automation(automation, context)
                thread.join()
                automations_details.append(thread.result)
                if thread.result["status"]=="FAIL":
                    failCount+=1
                    automations_status="FAIL"
        for thread in threads:
            thread.join()
            result=thread.result
            automations_details.extend(result["details"])
            if result["status"]=="FAIL":
                failCount+=result["failCount"]
                automations_status="FAIL"
        if automations_status!="FAIL":
            automations_status="PASS"
    except:
        logging.error(traceback.format_exc())
        automations_status="FAIL"
    return automations_status,failCount,automations_details

def run_automation(automation,context):
    automation_details=[]
    automation_status="RUNNING"
    automation_message=automation.description
    testtime=time.time()
    if "cookies" not in context:
        context["cookies"]=requests.cookies.RequestsCookieJar()
    result={"type":"automation","trace":context["trace"],"name":automation.name,"status":"RUNNING","testtime":"","duration":0,"details":[],"description":automation.description}
    result["testtime"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime))
    result["details"]=automation_details
    result["id"]=automation.id
    # RunService.putRunningResult(context["trace"],result)
    # logging.info("执行用例: %s" % self.automation.name)
    try:
        projectDataMap=getDataMap(automation.project.id)
        if context["value"]:
            projectDataMap.update(context["value"])
        context["value"]=projectDataMap
        if automation.type=="monitor":
            apis=automation.apis.all()
            paramMap=ParamUtil.replaceMap(context["value"],context["envMap"])
            value=json.dumps(ParamUtil.replaceMap(json.loads(automation.params),paramMap))
            for api in apis:
                if not context["ids"] or api.id in context["ids"]:
                    if context["env"]=="生产环境":
                        time.sleep(float(getConfigValueByName("api.interval",0.5)))
                    current_testtime=time.time()
                    api_result,api_status=RunService.run_api(api.id, value, context)
                    current_duration=int((time.time() - current_testtime)*1000)
                    api_detail={"trace":context["trace"],"name":api.name,"type":"api","id":api.id,"testtime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_testtime)),"duration":current_duration,"url":api_result["url"],"method":api_result["method"],"data":api_result["data"],"result":api_result["response"],"status":api_status,"description":api.description}
                    if api_status=="FAIL":
                        automation_status="FAIL"
                        api_detail["description"]=api_result["assertMessage"] if "assertMessage" in api_result else "执行失败,异常信息[{message}]".format(message=api_detail["result"])
                    automation_details.append(api_detail)
                    AutomationResult(name=api.name,trace=context["trace"],value=context["value"],details=json.dumps([api_detail]),result=api_status,
                             project=automation.project,automation=automation, api=api,testTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_testtime)),duration=current_duration,description=api_detail["description"],env=context["env"],user_id=context["user"]).save()
        else:
            steps=automation.steps.all().filter(automation2step__status=True).order_by("automation2step__order")
            for step in steps:
                if not "ids" in context or not context["ids"] or step.id in context["ids"]:
                    step_result=RunService.run_step(automation, step, context)
                    automation_details.append(step_result)
                    if step_result["status"]=="FAIL":
                        automation_status="FAIL"
                        automation_message="步骤[{stepName}]执行失败,异常信息[{message}]".format(stepName=step.name,message=step_result["description"])
                        break
        if automation_status!="FAIL":
            automation_status="PASS"
    except Exception as e:
        logging.error(traceback.format_exc())
        automation_message=str(e)
        automation_status="FAIL"
    finally:
        duration=int((time.time() - testtime)*1000)
        AutomationResult(name=automation.name,trace=context["trace"],result=automation_status,
                         project=automation.project,automation=automation,testTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime)),duration=duration,description=automation_message if "debug" not in context or not context["debug"] else "调试",env=context["env"],user_id=context["user"]).save()
    result["status"]=automation_status
    result["duration"]=duration
    result["details"]=automation_details
    result["description"]=automation_message
    # RunService.removeRunningResult(context["trace"])
    return result

class RunService():

    AutomationResultRunningMap={}
    AutomationListResultRunningMap={}

    @staticmethod
    def run_automationlist(automationlist,context):
        # print("执行用例集: %s, %s" % (automationlist.name,automationlist.description))
        thread = RunAutomationListThread(automationlist,context)
        thread.start()
        return thread

    @staticmethod
    def run_automation(automation,context):
        thread = RunAutomationThread(automation,context)
        thread.start()
        return thread

    @staticmethod
    def run_automation_publish(publish,id,automations,apis,context):
        thread = RunPublishAutomationThread(publish,id,automations,apis,context)
        thread.start()
        return thread

    @staticmethod
    def run_taskautomations(task,context):
        thread = RunTaskAutomationsThread(task,context)
        thread.start()
        return thread

    @staticmethod
    def run_step(automation, step, context):
        from api_test.service.commandService import CommandService

        context["step_details"]=[]
        context["step_status"]="RUNNING"
        step_message=step.description
        testtime=time.time()
        try:
            steps=json.loads(step.steps)
            if len(steps)==0:
                description=step.description
                lines=description.split('\n')
                lineNo=0
                for line in lines:
                    if not line.startswith("#"):
                        lineNo+=1
                        linePre="%s、" % str(lineNo)
                        lineStartIndex=line.find(linePre)
                        if lineStartIndex>=0:
                            line=line[lineStartIndex+len(linePre):]
                        command=CommandService.get_command(line,automation.project.id)
                        if command:
                            steps.append({"type":command["type"],"name":command["name"],"actionId":command["actionId"],"params":command["value"],"description":command["desc"],"disable":"False"})
            automationParams=ParamUtil.replaceMap(json.loads(automation.params),context["value"])
            stepParams=json.loads(ParamUtil.replaceParam(step.params,context["envMap"]))
            stepParams=ParamUtil.replaceMap(stepParams,automationParams)
            context["stepParams"]=stepParams
            RunService.run_steps(steps,context,automation=automation)
            if context["step_status"]!="FAIL":
                context["step_status"]="PASS"
        except ExecutionFailException as e:
            context["step_status"]="FAIL"
            step_message=str(e)
        except Exception as e:
            logging.error(traceback.format_exc())
            context["step_status"]="FAIL"
            step_message=str(e)
        finally:
            duration=int((time.time() - testtime)*1000)
            testtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(testtime))
            AutomationResult(name=step.name,trace=context["trace"],details=json.dumps(context["step_details"]),result=context["step_status"],
                             project=automation.project,automation=automation, step=step,testTime=testtime,duration=duration,description=step_message,env=context["env"],user_id=context["user"]).save()
            # context["details"].append({"name":step.name,"status":step_status,"details":step_details,"description":step.description})
        return {"id":step.id,"name":step.name,"details":context["step_details"],"status":context["step_status"],"testtime":testtime,"duration":duration,"description":step_message}

    @staticmethod
    def run_steps(steps,context,automation=None):
        from api_test.service.commandService import CommandService

        context["control"]={"forFlag":False,"forSteps":[],"whileFlag":False,"whileSteps":[],"loopFlag":False,"loopSteps":[],"ifFlag":False,"ifResult":False};
        for action in steps:
            if not action["disable"]=="True":
                if context["control"]["forFlag"] and not action["name"]=="END_FOR":
                    context["control"]["forSteps"].append(action)
                    continue
                if context["control"]["whileFlag"] and not action["name"]=="END_WHILE":
                    context["control"]["whileSteps"].append(action)
                    continue
                if context["control"]["loopFlag"] and not action["name"]=="END_LOOP":
                    context["control"]["loopSteps"].append(action)
                    continue
                if context["control"]["ifFlag"] and not context["control"]["ifResult"] and not action["name"]=="ELSE" and not action["name"]=="END_IF":
                    continue
                # actionValue=ParamUtil.replaceParam(action["params"],context["stepParams"])
                if action["type"]!="control":
                    try:
                        tempValueMap=context["stepParams"]
                        tempValueMap.update(context["value"])
                        actionValue=ParamUtil.replaceParam(action["params"],tempValueMap)
                        actionValue=json.dumps(ParamUtil.replaceEnvMap(json.loads(actionValue),context["envMap"]))
                    except Exception as e:
                        action_result=str(e)
                        action_status="FAIL"
                        context["step_details"].append({"name":action["name"],"type":action["type"],"result":action_result,"status":action_status,"description":action["description"]})
                        raise e
                else:
                    actionValue=ParamUtil.replaceParam(action["params"],context["stepParams"])
                if action["type"]=="api" and action["actionId"]:
                    if context["env"]=="生产环境":
                        time.sleep(float(getConfigValueByName("api.interval",0.5)))
                    action_result, action_status=RunService.run_api(action["actionId"], actionValue, context)
                    context["step_details"].append({"name":action["name"],"type":action["type"],"id":action["actionId"],"url":action_result["url"],"method":action_result["method"],"value":actionValue,"data":action_result["data"],"result":action_result["response"],"status":action_status,"description":action["description"] if not "assertMessage" in action_result else action_result["assertMessage"]})
                elif action["type"]=="automation" and action["actionId"]:
                    try:
                        action_result={}
                        automation=AutomationService.getAutomation(action["actionId"])
                        if automation.type=="reuse":
                            currentContext={"project":context["project"],"user":context["user"],"value":json.loads(actionValue),"result":{},"details":[],"status":"RUNNING","trace":datetime.now().strftime('%Y%m%d%H%M%S%f'),"env":context["env"],"envMap":context["envMap"],"cookies":context["cookies"]}
                            action_result=run_automation(automation,currentContext)
                            if "storedGlobalVariable" in currentContext["result"]:
                                storedGlobalVariableMap=currentContext["result"]["storedGlobalVariable"]
                                context["value"].update(storedGlobalVariableMap)
                            action_status=action_result["status"]
                        else:
                            raise ExecutionFailException("调用的用例[%s]不是可复用!" % automation.name)
                    except ExecutionCheckException as e:
                        action["description"]=str(e)
                        action_result["details"]=[]
                        action_status="FAIL"
                    except ExecutionFailException as e:
                        action["description"]=str(e)
                        action_result["details"]=[]
                        action_status="FAIL"
                        raise e
                    finally:
                        context["step_details"].append({"name":automation.name,"type":action["type"],"id":action["actionId"],"value":actionValue,"details":action_result["details"],"status":action_status,"description":action["description"]})
                elif action["type"] in ["common","data","redis","control"]:
                    try:
                        action_result=CommandService.run_command(action["type"], action["name"], actionValue, action["description"],context)
                        action_status="PASS"
                    except ExecutionCheckException as e:
                        action_result=str(e)
                        action_status="FAIL"
                    except ExecutionFailException as e:
                        action_result=str(e)
                        action_status="FAIL"
                        raise e
                    except (LoopContinueException,LoopBreakException) as e:
                        raise e
                    except Exception as e:
                        action_result=str(e)
                        action_status="FAIL"
                        raise e
                    finally:
                        context["step_details"].append({"name":action["name"],"type":action["type"],"result":action_result,"status":action_status,"description":action["description"]})
                if "storedGlobalVariable" in context["result"].keys():
                    storedGlobalVariableMap=context["result"]["storedGlobalVariable"]
                    context["value"].update(storedGlobalVariableMap)
                    if "globalValue" in context:
                        context["globalValue"].update(storedGlobalVariableMap)
                if "storedVariable" in context["result"].keys():
                    storedVariableMap=context["result"]["storedVariable"]
                    context["value"].update(storedVariableMap)
                if automation and "storedAutomationVariable" in context["result"].keys():
                    storedAutomationVariableMap=context["result"]["storedAutomationVariable"]
                    automationParamMap=json.loads(automation.params)
                    automationParamMap.update(storedAutomationVariableMap)
                    automation.params=json.dumps(automationParamMap)
                    automation.save()
                if action_status=="FAIL":
                    context["step_status"]="FAIL"
                    break

    @staticmethod
    def run_api(id, value,context):
        api_status="RUNNING"
        api_result={}
        try:
            for i in range(3):
                api_result=ApiService.run_api_by_id(id,value,context["cookies"])
                if api_result["responseCode"]==200:
                    if "assertMessage" in api_result:
                        api_status="FAIL"
                    else:
                        api_status="PASS"
                    break
            if api_status!="FAIL":
                api_status="PASS"
        except Exception as e:
            logging.error(traceback.format_exc())
            raise ExecutionFailException(str(e))
        finally:
            context["result"]["result"]=api_result["response"]
            context["result"]["responseCode"]=api_result["responseCode"]
        return api_result,api_status

    @staticmethod
    def putRunningResult(trace,result):
        RunService.AutomationResultRunningMap[trace]=result

    @staticmethod
    def getRunningResult(trace):
        if trace in RunService.AutomationResultRunningMap:
            return RunService.AutomationResultRunningMap[trace]
        else:
            return None

    @staticmethod
    def removeRunningResult(trace):
        del RunService.AutomationResultRunningMap[trace]

    @staticmethod
    def putRunningListResult(trace,result):
        RunService.AutomationListResultRunningMap[trace]=result

    @staticmethod
    def getRunningListResult(trace):
        if trace in RunService.AutomationListResultRunningMap:
            return RunService.AutomationListResultRunningMap[trace]
        else:
            return None

    @staticmethod
    def removeRunningListResult(trace):
        del RunService.AutomationListResultRunningMap[trace]

    @staticmethod
    def getAutomationResult(automation,trace):
        if automation.type=="list":
            automation_result=RunService.getRunningListResult(trace)
            if not automation_result:
                automation_result={"name":"","details":[],"status":"RUNNING","trace":trace}
                results=AutomationResult.objects.filter(trace=trace,step=None).order_by("id")
                for result in results:
                    if int(result.automation.id)!=int(automation.id):
                        automation_result["details"].append({"id":result.automation.id,"type":"automation","name":result.name,"status":result.result,"testtime":result.testTime,"duration":result.duration,"details":json.loads(result.details) if result.details else [],"description":result.description,"trace":result.trace})
                    else:
                        automation_result["status"]=result.result
                        automation_result["name"]=result.name
                        automation_result["description"]=result.description
                        automation_result["testtime"]=result.testTime
                        automation_result["duration"]=result.duration
        elif automation.type=="monitor":
            automation_result={"name":"","details":[],"status":"RUNNING","trace":trace}
            results=AutomationResult.objects.filter(automation=automation.id,trace=trace).order_by("id")
            for result in results:
                if result.api:
                    automation_result["details"].append({"id":result.api.id,"type":"api","name":result.name,"status":result.result,"testtime":result.testTime,"duration":result.duration,"details":json.loads(result.details),"description":result.description})
                else:
                    automation_result["status"]=result.result
                    automation_result["name"]=result.name
                    automation_result["description"]=result.description
                    automation_result["testtime"]=result.testTime
                    automation_result["duration"]=result.duration
        else:
            automation_result={"name":"","details":[],"status":"RUNNING","trace":trace}
            results=AutomationResult.objects.filter(automation=automation.id,trace=trace).order_by("id")
            for result in results:
                if result.step:
                    automation_result["details"].append({"id":result.step.id,"type":"step","name":result.name,"status":result.result,"testtime":result.testTime,"duration":result.duration,"details":json.loads(result.details),"description":result.description})
                else:
                    automation_result["status"]=result.result
                    automation_result["name"]=result.name
                    automation_result["description"]=result.description
                    automation_result["testtime"]=result.testTime
                    automation_result["duration"]=result.duration
        return automation_result

    @staticmethod
    def getPublishResult(trace):
        automation_result=RunService.getRunningListResult(trace)
        if not automation_result:
            automation_result={"name":"","details":[],"status":"RUNNING","trace":trace}
            results=AutomationResult.objects.filter(trace=trace,step=None).order_by("id")
            for result in results:
                if result.automation:
                    automation_result["details"].append({"name":result.name,"status":result.result,"testtime":result.testTime,"duration":result.duration,"details":json.loads(result.details),"description":result.description})
                else:
                    automation_result["status"]=result.result
                    automation_result["name"]=result.name
                    automation_result["description"]=result.description
                    automation_result["testtime"]=result.testTime
                    automation_result["duration"]=result.duration
        return automation_result

    @staticmethod
    def updatePublishResult(publish,id,result,trace,project_id,user_id):
        report_url=settings.REPORT_URL
        publish_test_url=settings.PUBLISH_TEST_URL
        statusMap={"PASS":"测试通过","FAIL":"测试失败"}
        autotest_report="%s/project=%s/trace=%s" % (report_url,project_id,trace)
        params = {"id":id,"autotest_status":statusMap[result],"autotest_report": autotest_report}
        code, response_data, header_data=run_http(request_type="PUT",
                  header={"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'},
                  url=publish_test_url,
                  request_parameter_type="application/json", parameter=json.dumps(params).encode('utf-8'))
        record_dynamic(project=project_id,
                       _type="测试", operationObject="发布项目", user=user_id,
                       data="发布项目%s上线单%s%s,更新测试结果%s,测试报告链接:\n%s" % (publish,id,statusMap[result],response_data["msg"] if "msg" in response_data else "未知",autotest_report))
