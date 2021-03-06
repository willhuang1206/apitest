from django.conf.urls import url

from api_test.api import api, automation, user,global_config,project,imports,automationReport as Report
from api_test import scheduletask

urlpatterns = [
    url(r'project/project_list', project.ProjectList.as_view()),
    url(r'project/add_project', project.AddProject.as_view()),
    url(r'project/update_project', project.UpdateProject.as_view()),
    url(r'project/del_project', project.DelProject.as_view()),
    url(r'project/disable_project', project.DisableProject.as_view()),
    url(r'project/enable_project', project.EnableProject.as_view()),
    url(r'title/project_info', project.ProjectInfo.as_view()),
    url(r'project/config_list', project.ConfigList.as_view()),
    url(r'project/add_config', project.AddConfig.as_view()),
    url(r'project/update_config', project.UpdateConfig.as_view()),
    url(r'project/del_config', project.DelConfig.as_view()),
    url(r'project/disable_config', project.DisableConfig.as_view()),
    url(r'project/enable_config', project.EnableConfig.as_view()),
    url(r'global/config_list', global_config.GlobalConfigList.as_view()),
    url(r'global/publish_list', global_config.PublishList.as_view()),
    url(r'global/add_config', global_config.AddGlobalConfig.as_view()),
    url(r'global/update_config', global_config.UpdateGlobalConfig.as_view()),
    url(r'global/del_config', global_config.DelGlobalConfig.as_view()),
    url(r'global/disable_config', global_config.DisableGlobalConfig.as_view()),
    url(r'global/enable_config', global_config.EnableGlobalConfig.as_view()),
    url(r'api/group', api.Group.as_view()),
    url(r'api/add_group', api.AddGroup.as_view()),
    url(r'api/update_name_group', api.UpdateNameGroup.as_view()),
    url(r'api/del_group', api.DelGroup.as_view()),
    url(r'api/api_list', api.ApiList.as_view()),
    url(r'api/add_api', api.AddApi.as_view()),
    url(r'api/updateMock', api.UpdateApiMockStatus.as_view()),
    url(r'api/lead_swagger', api.LeadSwagger.as_view()),
    url(r'api/update_api', api.UpdateApi.as_view()),
    url(r'api/del_api', api.DelApi.as_view()),
    url(r'api/run_api', api.RunApi.as_view()),
    url(r'api/jybdecode', api.JybDecode.as_view()),
    url(r'api/update_group', api.UpdateGroup.as_view()),
    url(r'api/api_info', api.ApiInfoDetail.as_view()),
    url(r'api/add_history', api.AddHistory.as_view()),
    url(r'api/history_list', api.HistoryList.as_view()),
    url(r'api/del_history', api.DelHistory.as_view()),
    url(r'api/operation_history', api.OperationHistory.as_view()),
    url(r'api/Download', api.DownLoad.as_view()),
    url(r'api/download_doc', api.download_doc),
    url(r'automation/group', automation.GroupList.as_view()),
    url(r'automation/add_group', automation.AddGroup.as_view()),
    url(r'automation/del_group', automation.DelGroup.as_view()),
    url(r'automation/update_name_group', automation.UpdateNameGroup.as_view()),
    url(r'automation/update_automation_group', automation.UpdateGroup.as_view()),
    url(r'automation/automation_list', automation.AutomationList.as_view()),
    url(r'automation/add_automation', automation.AddAutomation.as_view()),
    url(r'automation/update_automation', automation.UpdateAutomation.as_view()),
    url(r'automation/del_automation', automation.DelAutomation.as_view()),
    # url(r'automation/DownloadAutomation', automation.DownLoadAutomation.as_view()),
    url(r'automation/step_list', automation.StepList.as_view()),
    url(r'automation/step_info', automation.StepInfo.as_view()),
    url(r'automation/add_step', automation.AddStep.as_view()),
    url(r'automation/add_reuse_steps', automation.AddReuseStep.as_view()),
    url(r'automation/link_automation', automation.LinkAutomation.as_view()),
    url(r'automation/unlink_automation', automation.UnlinkAutomation.as_view()),
    url(r'automation/link_api', automation.LinkApi.as_view()),
    url(r'automation/unlink_api', automation.UnlinkApi.as_view()),
    url(r'automation/stepstatus_update', automation.StepStatusUpdate.as_view()),
    url(r'automation/update_step', automation.UpdateStep.as_view()),
    url(r'automation/del_step', automation.DelStep.as_view()),
    url(r'automation/run', automation.RunAutomation.as_view()),
    url(r'automation/command_list', automation.CommandList.as_view()),
    url(r'automation/getresult', automation.ResultList.as_view()),
    url(r'automation/task_list', automation.TaskList.as_view()),
    url(r'automation/add_task', automation.AddTask.as_view()),
    url(r'automation/update_task', automation.UpdateTask.as_view()),
    url(r'automation/del_task', automation.DelTask.as_view()),
    url(r'automation/stop_task', automation.StopTask.as_view()),
    url(r'automation/start_task', automation.StartTask.as_view()),
    url(r'automation/execute_task', automation.RunTask.as_view()),
    url(r'automation/publish_list', automation.PublishConfigList.as_view()),
    url(r'automation/add_publish', automation.AddPublishConfig.as_view()),
    url(r'automation/update_publish', automation.UpdatePublishConfig.as_view()),
    url(r'automation/del_publish', automation.DelPublishConfig.as_view()),
    url(r'automation/disable_publish', automation.DisablePublishConfig.as_view()),
    url(r'automation/enable_publish', automation.EnablePublishConfig.as_view()),
    url(r'automation/test_publish', automation.RunPublishTest.as_view()),
    url(r'report/automation_summary', Report.Automation_Summary.as_view()),
    url(r'report/automation_result', Report.Automation_Result.as_view()),
    url(r'report/automations_result', Report.Automations_Result.as_view()),
    url(r'report/apiautomatedcoverage', Report.ApiAutomatedCoverage.as_view()),
    url(r'report/automation_chart', Report.Automation_Chart.as_view()),
    url(r'report/api_chart', Report.Api_Chart.as_view()),
    url(r'report/publish_chart', Report.Publish_Chart.as_view()),
    url(r'report/dynamic_chart', Report.Dynamic_Chart.as_view()),
    url(r'report/automation_detail', Report.Automation_Detail.as_view()),
    url(r'report/updateresultfaildetail', Report.UpdateResultFailDetail.as_view()),
    url(r'report/updateapicoverage', Report.UpdateApiAutomationCoverage.as_view()),
    url(r'report/updatepublishresult', Report.UpdatePublishResult.as_view()),
    url(r'member/update', project.UpdateMembers.as_view()),
    url(r'member/project_member', project.ProjectMemberList.as_view()),
    url(r'dynamic/dynamic', project.Dynamic.as_view()),
    url(r'user/login', user.Login.as_view()),
    url(r'user/ssologin', user.SSOLogin.as_view()),
    url(r'user/logout', user.Logout.as_view()),
    url(r'global/get_users', user.GetUsers.as_view()),
    url(r'global/link_users', user.LinkUsers.as_view()),
    url(r'global/user_list', user.UserList.as_view()),
    url(r'global/add_user', user.AddUser.as_view()),
    url(r'global/update_user', user.UpdateUser.as_view()),
    url(r'global/del_user', user.DelUser.as_view()),
    url(r'global/del_user', user.DelUser.as_view()),
    url(r'imports/devapi_grouplist', imports.DevApiGroupList.as_view()),
    url(r'imports/devapi_import', imports.ImportDevApi.as_view()),
    url(r'imports/apidomainlist', imports.ApiDomainList.as_view()),
    url(r'imports/autodomainlist', imports.ActionDomainList.as_view()),
    # url(r'imports/api_import', imports.ImportApi.as_view()),
    url(r'imports/api_importfrompostman', imports.ImportApiFromPostman.as_view()),
    url(r'imports/uploadfile', imports.UploadFile.as_view()),
    url(r'imports/automation_importfromexcel', imports.ImportAutomationFromExcel.as_view()),
    url(r'imports/downloadtemplate', imports.downloadAutoTemplate)
]
