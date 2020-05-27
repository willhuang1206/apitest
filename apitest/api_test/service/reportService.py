#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import logging
from jinja2 import Environment,FileSystemLoader
from django.conf import settings
from api_test.common.emaillib import EmailHandler
from api_test.common.confighttp import run_http
from api_test.common.common import record_dynamic
from api_test.common.jsonUtil import json
from api_test.service.configService import getProjectConfigValueByName

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class ReportService():

    reportBaseUrl=settings.REPORT_URL

    def __init__(self):
        pass

    def sendTaskReport(self,task,result,emails):

        try:
            env = Environment(loader=FileSystemLoader('./api_test/templates'))
            template = env.get_template("executionReport.html")

            receiver=emails if len(emails)>0 else settings.EMAIL_RECEIVER
            receiver_cc=settings.EMAIL_RECEIVER_CC

            reportMsg = 'Hi All, \r\n \r\n{taskName}执行情况如下:'.format(taskName=task.name)
            reportResult,failedResults,passedResults=self.getReportResult(task.project_id,result)
            status="通过" if len(failedResults)==0 else "失败"
            reportTitle = "{taskName}执行{status}".format(taskName=task.name,status=status)
            if task.sendEmail==1 or (task.sendEmail==2 and len(failedResults)>0) or (task.sendEmail==3 and len(failedResults)==0):
                mailbody = template.render(result=reportResult,failedResults=failedResults,passedResults=passedResults)
                emailsender = EmailHandler(settings.SMTP_SERVER, settings.SMTP_PORT,settings.SMTP_USER, settings.SMTP_CODE)
                emailsender.sendemail(settings.SMTP_USER, receiver, reportTitle, reportMsg, strMsgHtml=mailbody, listCc=receiver_cc)
                logging.info("发送执行报告(%s)" % task.name)

            robotSendUrl=getProjectConfigValueByName(task.project.id,"{taskname}_robot".format(taskname=task.name))
            if not robotSendUrl:
                robotSendUrl=getProjectConfigValueByName(task.project.id,"robot")
            if robotSendUrl:
                template = env.get_template("executionResult.md")
                content = {"msgtype":"markdown","markdown":{"content":template.render(result=reportResult)}}
                code, response_data, header_data=run_http(request_type="POST",
                  header={"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'},
                  url=robotSendUrl,request_parameter_type="application/json", parameter=json.dumps(content).encode('utf-8'))
                logging.info("发送自动化任务[{taskname}]执行结果到企业微信群{status}!".format(taskname=task.name,status=response_data["errmsg"] if "errmsg" in response_data else "未知"))
                record_dynamic(project=task.project.id,
                       _type="测试", operationObject="自动化任务", user=1,
                       data="发送自动化任务[{taskname}]执行结果到企业微信群{status}!".format(taskname=task.name,status=response_data["errmsg"] if "errmsg" in response_data else "未知"))
        except:
            logging.error(traceback.format_exc())

    def getReportResult(self,projectId,result):
        reportResult={}
        failedResults=[]
        passedResults=[]
        reportResult["name"]=result["name"]
        reportResult["totalCount"]=len(result["details"])
        reportResult["testtime"]=result["testtime"]
        reportResult["duration"]=round(result["duration"]/1000,1)
        reportResult["reportUrl"]="{reportBaseUrl}/project={projectId}/trace={trace}".format(reportBaseUrl=self.reportBaseUrl,projectId=projectId,trace=result["trace"])
        passCount=0
        for automationResult in result["details"]:
            automationResult["resultUrl"]="{reportBaseUrl}/project={projectId}/auto={automationId}/trace={trace}"\
                .format(reportBaseUrl=self.reportBaseUrl,projectId=projectId,automationId=automationResult["id"],trace=automationResult["trace"])
            if automationResult["status"]=="PASS":
                automationResult["color"]="green"
                passCount+=1
                passedResults.append(automationResult)
            else:
                automationResult["color"]="red"
                failedResults.append(automationResult)
        reportResult["passCount"]=passCount
        reportResult["failCount"]=reportResult["totalCount"]-passCount
        return reportResult,failedResults,passedResults
