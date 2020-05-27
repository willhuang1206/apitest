from django.core.exceptions import ObjectDoesNotExist
from api_test.common.auth import TokenAuthentication
from rest_framework.views import APIView
from django.db.models import Q
from django.core import serializers
from django.db import connection,connections
from django.db.models import F, Q, Case, When, Count,Sum,Value,IntegerField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api_test.common.api_response import JsonResponse
from api_test.models import Project,AutomationResult,AutomationResultFailDetail,ApiAutomationCoverage,Automation
from api_test.serializers import ProjectSerializer,AutomationResultSerializer,ApiAutomationCoverageSerializer
from api_test.common.jsonUtil import json
from api_test.common.auth import permission_required
import traceback
import logging
import datetime
import ast

class Automation_Summary(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化执行汇总
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        try:
            kwargs={}
            args=(~Q(automation__type= 'reuse') & ~Q(automation__type= 'list') & ~Q(description= '调试'))
            if start_time and end_time:
                kwargs={"automation__isnull":False,"api__isnull":True,"step__isnull":True,"testTime__gte":start_time,"testTime__lte":end_time}
            else:
                kwargs={"automation__isnull":False,"api__isnull":True,"step__isnull":True}
            if project_id:
                kwargs["project_id"]=project_id
            results=AutomationResult.objects.filter(args,**kwargs).values("automation_id","name").annotate(passed=Sum(Case(When(result="PASS",then=Value(1)),default=Value(0),output_field=IntegerField())),total=Count("id"),duration=Sum("duration")).order_by("-total")
        except:
            traceback.print_exc()
            return JsonResponse(code="999998", msg="失败！")
        paginator = Paginator(results, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(results)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        # data=serializers.serialize("json",obm.object_list,ensure_ascii=False)
        return JsonResponse(data={"data": obm.object_list,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功!")

class Automation_Result(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化执行情况
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        automation_id = request.GET.get("automation_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        trace=request.GET.get("trace")
        try:
            kwargs={}
            args=()
            if automation_id:
                if start_time and end_time:
                    kwargs={"automation":automation_id,"step__isnull":True,"api__isnull":True,"testTime__gte":start_time,"testTime__lte":end_time}
                else:
                    kwargs={"automation":automation_id,"step__isnull":True,"api__isnull":True}
                results=AutomationResult.objects.filter(**kwargs).order_by("-id")
                paginator = Paginator(results, page_size)  # paginator对象
                pages = paginator.num_pages  # 总页数
                total=len(results)
                obm = paginator.page(page)
                serialize = AutomationResultSerializer(obm, many=True)
                data={"data":serialize.data,"page":page,"pages":pages,"total":total}
            elif trace:
                if start_time and end_time:
                    args=(~Q(automation__type= 'list'))
                    kwargs={"automation__isnull":False,"trace":trace,"step__isnull":True,"api__isnull":True,"testTime__gte":start_time,"testTime__lte":end_time}
                else:
                    args=(~Q(automation__type= 'list'))
                    kwargs={"automation__isnull":False,"trace":trace,"step__isnull":True,"api__isnull":True}
                results=AutomationResult.objects.filter(args,**kwargs).order_by("-id")
                total=len(results)
                page_size=total
                paginator = Paginator(results, page_size)  # paginator对象
                pages = paginator.num_pages  # 总页数
                obm = paginator.page(page)
                serialize = AutomationResultSerializer(obm, many=True)
                data={"data":serialize.data,"page":page,"pages":pages,"page_size":page_size,"total":total}
                result=AutomationResult.objects.filter(trace=trace,automation__isnull=True,step__isnull=True,api__isnull=True).order_by("-id")
                if len(result)>0:
                    data["report"]=json.loads(result[0].details)
            return JsonResponse(data=data,code="999999",msg="成功!")
        except:
            traceback.print_exc()
            return JsonResponse(code="999998", msg="失败！")

class Automations_Result(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化执行情况
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        type=request.GET.get("type", "publish")
        try:
            kwargs={}
            args=()
            if type=="publish":
                if start_time and end_time:
                    kwargs={"description__contains":"上线单","automation__isnull":True,"testTime__gte":start_time,"testTime__lte":end_time}
                else:
                    kwargs={"description__contains":"上线单","automation__isnull":True}
            elif type=="task":
                if start_time and end_time:
                    args=(~Q(description__contains="上线单"))
                    kwargs={"automation__isnull":True,"testTime__gte":start_time,"testTime__lte":end_time}
                else:
                    args=(~Q(description__contains="上线单"))
                    kwargs={"automation__isnull":True}
            elif type=="list":
                if start_time and end_time:
                    kwargs={"automation__type":"list","testTime__gte":start_time,"testTime__lte":end_time}
                else:
                    kwargs={"automation__type":"list"}
            if project_id:
                kwargs["project_id"]=project_id
            if len(args)>0:
                results=AutomationResult.objects.filter(args,**kwargs).order_by("-id")
            else:
                results=AutomationResult.objects.filter(**kwargs).order_by("-id")
        except:
            traceback.print_exc()
            return JsonResponse(code="999998", msg="失败！")
        paginator = Paginator(results, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(results)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = AutomationResultSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功!")

class Automation_Detail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化执行详情
        :param request:
        :return:
        """
        automation_id = request.GET.get("automation_id")
        trace = request.GET.get("trace")
        try:
            results=AutomationResult.objects.values("id","step_id","name","testTime","duration","result","details").filter(Q(step__isnull=False)|Q(api__isnull=False),automation=automation_id,trace=trace).order_by("id")
            for result in results:
                result["details"]=json.loads(result["details"])
            parent=AutomationResult.objects.filter(automation=automation_id,trace=trace,step__isnull=True,api__isnull=True).order_by("-id").first()
            parentResult=AutomationResultSerializer(parent)
            return JsonResponse(code="999999", msg="成功！", data={"results":results,"parentResult":parentResult.data})
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class ApiAutomatedCoverage(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口自动化覆盖率
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        project_id = request.GET.get("project_id")
        try:
            if project_id:
                results=ApiAutomationCoverage.objects.filter(project=project_id).order_by("-num")
            else:
                results=ApiAutomationCoverage.objects.all().order_by("-num")
        except:
            traceback.print_exc()
            return JsonResponse(code="999998", msg="失败！")
        paginator = Paginator(results, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total=len(results)
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ApiAutomationCoverageSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功!")

def daysBetween(date1,date2):
    date1=datetime.datetime.strptime(date1,"%Y-%m-%d")
    date2=datetime.datetime.strptime(date2,"%Y-%m-%d")
    return (date2-date1).days

class Automation_Chart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自动化用例执行统计信息
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        days=0 if not start_time or not end_time else daysBetween(start_time,end_time)
        period = request.GET.get("period","week") if 7<days<=30 else "day" if 0<days<=7 else "month"
        try:
            cursor = connection.cursor()
            sql="SELECT {date} as date,count(*) as num,round(sum(CASE WHEN result='PASS' THEN 1 ELSE 0 END)*100/count(*),2) as rate from api_test_automationresult result left join api_test_automation auto on result.automation_id=auto.id where %s result.description!='调试' and result.step_id is null and result.automation_id is not null and auto.type!='reuse' and auto.type!='list' %s GROUP BY date having num>0 order by date" % ("result.project_id={projectId} and" if project_id else "","and result.testTime >='{startDate}' AND result.testTime < '{endDate}'" if start_time and end_time else "")
            if period=="day":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( testTime, '%Y-%m-%d')")
            elif period=="week":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="date_sub(DATE_FORMAT( testTime, '%Y-%m-%d'),interval WEEKDAY(testTime) day)")
            elif period=="month":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( testTime, '%Y-%m')")
            elif period=="quarter":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="concat(year(testTime),' Q',QUARTER(testTime))")
            elif period=="year":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="year(testTime)")

            logging.info("执行sql: %s" % sql)

            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [line[0] for line in line_db]
            line_x = [line[1] if line[1] else 0 for line in line_db]
            line_x1 = [line[2] if line[2] else 0 for line in line_db]
            autoChart = {'line_name': line_name, 'line_x': line_x, 'line_x1': line_x1}

            FAIL_TYPE = {
                'code':'编码',
                'env':'环境',
                'data':'数据',
                'other':'其他'
            }
            sql="SELECT detail.type as failType,count(*) as num from api_test_automationresult result right join api_test_automationresultfaildetail detail on result.id=detail.result_id where %s result.step_id is null %s GROUP BY failType having num>0 order by num desc" % ("result.project_id={projectId} and" if project_id else "","and result.testTime >='{startDate}' AND result.testTime < '{endDate}'" if start_time and end_time else "")
            sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time)

            logging.info("执行sql: %s" % sql)
            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [FAIL_TYPE[line[0]] for line in line_db]
            line_data = [{"name":FAIL_TYPE[line[0]],"value":line[1]} for line in line_db]
            failTypeChart = {'line_name': line_name, 'line_data': line_data}

            SEVERITY = {
                'fatal':'致命的',
                'critical':'严重的',
                'major':'一般的',
                'minor':'微小的'
            }
            sql="SELECT detail.severity as failSeverity,count(*) as num from api_test_automationresult result right join api_test_automationresultfaildetail detail on result.id=detail.result_id where %s result.step_id is null %s GROUP BY failSeverity having num>0 order by num desc" % ("result.project_id={projectId} and" if project_id else "","and result.testTime >='{startDate}' AND result.testTime < '{endDate}'" if start_time and end_time else "")
            sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time)

            logging.info("执行sql: %s" % sql)
            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [SEVERITY[line[0]] for line in line_db]
            line_data = [{"name":SEVERITY[line[0]],"value":line[1]} for line in line_db]
            failSeverityChart = {'line_name': line_name, 'line_data': line_data}

            return JsonResponse(code="999999", msg="成功！", data={"autoChart":autoChart,"failTypeChart":failTypeChart,"failSeverityChart":failSeverityChart})
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class Publish_Chart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取发布项目测试统计信息
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        period = request.GET.get("period","week") if not (start_time and end_time) or daysBetween(start_time,end_time) > 7 else "day"
        try:
            cursor = connection.cursor()
            sql="SELECT {date} as date,count(*) as num,round(sum(CASE WHEN result='PASS' THEN 1 ELSE 0 END)*100/count(*),2) as rate from api_test_automationresult where " + ("project_id={projectId} and" if project_id else "") + " step_id is null and automation_id is null and description like '%上线单%'" + (" and testTime >='{startDate}' AND testTime < '{endDate}'" if start_time and end_time else "") + " GROUP BY date having num>0 order by date"
            if period=="day":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( testTime, '%Y-%m-%d')")
            elif period=="week":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="date_sub(DATE_FORMAT( testTime, '%Y-%m-%d'),interval WEEKDAY(testTime) day)")
            elif period=="month":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( testTime, '%Y-%m')")
            elif period=="quarter":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="concat(year(testTime),' Q',QUARTER(testTime))")
            elif period=="year":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="year(testTime)")

            # print(sql)

            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [line[0] for line in line_db]
            line_x = [line[1] if line[1] else 0 for line in line_db]
            line_x1 = [line[2] if line[2] else 0 for line in line_db]
            publish_chart = {'line_name': line_name, 'line_x': line_x, 'line_x1': line_x1}

            sql="SELECT name,count(*) as num from api_test_automationresult where " + ("project_id={projectId} and" if project_id else "") + " step_id is null and automation_id is null and description like '%上线单%'" + (" and testTime >='{startDate}' AND testTime < '{endDate}'" if start_time and end_time else "") + " GROUP BY name having num>0 order by num desc"
            sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time)

            logging.info("执行sql: %s" % sql)
            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [line[0] for line in line_db]
            line_data = [{"name":line[0],"value":line[1]} for line in line_db]
            publish_pie = {'line_name': line_name, 'line_data': line_data}

            return JsonResponse(code="999999", msg="成功！", data={"publish_chart":publish_chart,"publish_pie":publish_pie})
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class Api_Chart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口执行统计信息
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        period = request.GET.get("period","week") if not (start_time and end_time) or daysBetween(start_time,end_time) > 7 else "day"
        try:
            cursor = connection.cursor()
            sql="SELECT {date} as date,count(*) as num from api_test_projectdynamic where %s type='执行' and operationObject='接口' %s GROUP BY date having num>0 order by date" % ("project_id={projectId} and" if project_id else "","and time >='{startDate}' AND time < '{endDate}'" if start_time and end_time else "")
            if period=="day":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( time, '%Y-%m-%d')")
            elif period=="week":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="date_sub(DATE_FORMAT( time, '%Y-%m-%d'),interval WEEKDAY(time) day)")
            elif period=="month":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( time, '%Y-%m')")
            elif period=="quarter":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="concat(year(time),' Q',QUARTER(time))")
            elif period=="year":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="year(time)")

            # print(sql)

            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [line[0] for line in line_db]
            line_x = [line[1] if line[1] else 0 for line in line_db]
            line_chart = {'line_name': line_name, 'line_x': line_x}
            return JsonResponse(code="999999", msg="成功！", data=line_chart)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class Dynamic_Chart(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目动态统计信息
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if end_time:
            end_time=(datetime.datetime.strptime(end_time,'%Y-%m-%d')+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        period = request.GET.get("period","week") if not (start_time and end_time) or daysBetween(start_time,end_time) > 7 else "day"
        try:
            cursor = connection.cursor()
            sql="SELECT {date} as date,count(*) as num from api_test_projectdynamic where %s %s GROUP BY date having num>0 order by date" % ("project_id={projectId}" if project_id else "1=1","and time >='{startDate}' AND time < '{endDate}'" if start_time and end_time else "")
            if period=="day":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( time, '%Y-%m-%d')")
            elif period=="week":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="date_sub(DATE_FORMAT( time, '%Y-%m-%d'),interval WEEKDAY(time) day)")
            elif period=="month":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="DATE_FORMAT( time, '%Y-%m')")
            elif period=="quarter":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="concat(year(time),' Q',QUARTER(time))")
            elif period=="year":
                sql = sql.format(projectId=project_id,startDate=start_time,endDate=end_time,date="year(time)")

            # print(sql)

            cursor.execute(sql)

            # deal with in the line chart
            line_db = cursor.fetchall()
            line_name = [line[0] for line in line_db]
            line_x = [line[1] if line[1] else 0 for line in line_db]
            line_chart = {'line_name': line_name, 'line_x': line_x}
            return JsonResponse(code="999999", msg="成功！", data=line_chart)
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class UpdateResultFailDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("change_automation")
    def post(self, request):
        """
        更新执行结果失败详情
        :param request:
        :return:
        """
        data = request.data
        try:
            obj, created = AutomationResultFailDetail.objects.update_or_create(project_id=data["project_id"], result_id=data["result_id"],
               defaults={"type":data["type"],"severity":data["severity"],"cause":data["cause"],"detail":data["detail"],
                         "bug":data["bug"] if "bug" in data else None, "action":data["action"] if "action" in data else None})
            return JsonResponse(data={"id": obj.id}, code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

class UpdateApiAutomationCoverage(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        try:
            data = request.data
            projectId=data["projectId"] if "projectId" in data else None
            groupId=data["groupId"] if "groupId" in data else None
            updateApiAutomationCoverage(projectId,groupId)
            return JsonResponse(code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")

def updateApiAutomationCoverage(projectId=None,groupId=None):
    apiCoverageMap={}

    def updateApiCoverage(projectId,apiId,automationId):
        try:
            # coverage=ApiAutomationCoverage.objects.filter(project_id=projectId,api_id=apiId).first()
            if apiId in apiCoverageMap:
                apiAutomationSet=apiCoverageMap[apiId]
            else:
                apiAutomationSet=set()
            if automationId not in apiAutomationSet:
                apiAutomationSet.add(automationId)
                apiAutomations=list(apiAutomationSet)
                ApiAutomationCoverage.objects.update_or_create(project_id=projectId,api_id=apiId,defaults={"automations":json.dumps(apiAutomations),"num":len(apiAutomations)})
                apiCoverageMap[apiId]=apiAutomationSet
        except Exception as e:
            logging.info("项目Id:%s,接口ID:%s,用例ID:%s,异常: %s" % (projectId,apiId,automationId,str(e)))

    try:
        logging.info("开始更新接口自动化覆盖率")
        if projectId:
            if groupId:
                automations = Automation.objects.filter(project=projectId, group=groupId,type__in=["case","reuse","data","monitor"]).order_by("-id")
            else:
                automations = Automation.objects.filter(project=projectId, type__in=["case","reuse","data","monitor"]).order_by("-id")
        else:
            automations = Automation.objects.filter(type__in=["case","reuse","data","monitor"]).order_by("-id")

        for automation in automations:
            if automation.type in ["case","reuse","data"]:
                steps=automation.steps.all().filter(automation2step__status=True).order_by("automation2step__order")
                for step in steps:
                    actions=json.loads(step.steps)
                    ids=[action["actionId"] for action in actions if action["type"]=="api"]
                    for id in ids:
                        updateApiCoverage(automation.project.id,id,automation.id)
            elif automation.type=="monitor":
                for api in automation.apis.all():
                    updateApiCoverage(automation.project.id,api.id,automation.id)
        logging.info("完成更新接口自动化覆盖率")
    except:
        logging.error(traceback.format_exc())

class UpdatePublishResult(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        try:
            logging.info("开始更新发布项目执行结果")
            data = request.data
            projectId=data["projectId"] if "projectId" in data else None
            if projectId:
                results=AutomationResult.objects.filter(project=projectId,name__contains="上线单",automation__isnull=True).order_by("-id")
            else:
                results=AutomationResult.objects.filter(name__contains="上线单",automation__isnull=True).order_by("-id")
            for result in results:
                infos=result.name.split(',')
                if len(infos)==3:
                    result.name=infos[0]
                    result.description=infos[2]
                    result.save()
            logging.info("完成更新发布项目执行结果")
            return JsonResponse(code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")




