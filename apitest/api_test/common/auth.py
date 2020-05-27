from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from django.conf import settings
import requests
from api_test.common import MD5
from api_test.models import ProjectMember
from django.contrib.auth.models import User,Group
from rest_framework.authtoken.models import Token

ssoLogin=settings.SSO_LOGIN
ssoClientId=settings.SSO_CLIENTID
ssoClientSecret=settings.SSO_CLIENTSECRET
ssoRedirectUrl=settings.SSO_REDIRECTURL
ssoNotifyUrl=settings.SSO_NOTIFYURL
ssoGetTicketUrl=settings.SSO_GETTICKETURL
#sso的token的校验地址
ssoValidateUrl=settings.SSO_VALIDATEURL
ssoLoginUrl=settings.SSO_LOGINURL
ssoLogoutUrl=settings.SSO_LOGOUTURL

class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst=Dict()
    for k,v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst

class TokenAuthentication(BaseAuthentication):
    '''认证类'''
    def authenticate(self, request):

        ticket = request.META.get('HTTP_AUTHORIZATION')
        if ticket:
            if ssoLogin:
                params={"cmd":"80010002","data":{"ticket":ticket,"client_secret":ssoClientSecret,"secret_key":MD5.encrypt("%s-%s" % (ticket,ssoClientSecret))}}
                response=requests.post(url=ssoValidateUrl,json=params).json()
                if response["code"]==0:
                    user_id=response["data"]["identifier"]
                    expire=response["data"]["expire"]
                    params={"cmd":"80010004","data":{"user_id":user_id,"client_secret":ssoClientSecret,"secret_key":MD5.encrypt("%s-%s" % (user_id,ssoClientSecret))}}
                    response=requests.post(url=ssoValidateUrl,json=params).json()
                    if response["code"]==0:
                        user=User.objects.get(username=response["data"]["user_name"])
                        if not user:
                            response["data"]["pk"]=user_id
                            user=dict_to_object(response["data"])
                        return (user,ticket)
                    else:
                        raise exceptions.AuthenticationFailed('用户认证失败')
                else:
                    token= Token.objects.get(key=ticket)
                    if token:
                        user=User.objects.get(id=token.user.id)
                        return (user,ticket)
                    else:
                        raise exceptions.AuthenticationFailed('用户认证失败')
            else:
                token= Token.objects.get(key=ticket)
                if token:
                    user=User.objects.get(id=token.user.id)
                    return (user,ticket)
                else:
                    raise exceptions.AuthenticationFailed('用户认证失败')
        else:
            secretKey=MD5.encrypt("%s-%s-%s-%s" % (ssoRedirectUrl,ssoNotifyUrl,ssoClientId,ssoClientSecret))
            url="%s?redirect_uri=%s&notify_uri=%s&client_id=%s&secret_key=%s" % (ssoGetTicketUrl,ssoRedirectUrl,ssoNotifyUrl,ssoClientId,secretKey)
            requests.get(url=url)

    def authenticate_header(self, request):
        pass

def permission_required(*permissions):
    '''自定义 权限验证 装饰器'''
    def wrapper(func):
        def check_permission(self,request):
            check=True
            if len(permissions)>0:
                project_id=""
                if request.method=="GET":
                    project_id=request.GET.get("project_id","")
                if request.method=="POST":
                    data = request.data
                    project_id=data["project_id"] if "project_id" in data else ""
                if project_id:
                    projectMember=ProjectMember.objects.filter(project_id=project_id,user_id=request.user.id)
                    user=User.objects.get(id=request.user.id)
                    if len(projectMember)>0:
                        groupId=projectMember[0].group.id
                        group=Group.objects.get(id=groupId)
                        for permission in permissions:
                            if permission and len(group.permissions.filter(codename=permission))==0:
                                check=False
                                break
                            if not permission and not user.is_superuser:
                                check=False
                                break
                    else:
                        check=False
                else:
                    user=User.objects.get(id=request.user.id)
                    if not user:
                        check=False
                    elif not user.is_superuser:
                        check=False
            if check:
                return func(self,request)
            else:
                raise exceptions.NotAcceptable('用户没有该权限!')
        return check_permission
    return wrapper