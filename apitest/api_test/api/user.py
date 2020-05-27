from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.conf import settings
import requests
import traceback
import logging
from api_test.serializers import TokenSerializer,UserSerializer
from api_test.common.api_response import JsonResponse
from api_test.common.auth import TokenAuthentication,permission_required
from api_test.common import MD5
from api_test.models import UserProfile

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

class Login(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        username=data["username"]
        password=data["password"]
        if not ssoLogin:
            user=User.objects.filter(username=username,password=password)
            if user:
                token,created= Token.objects.get_or_create(user=user[0])
                role="admin" if user[0].is_superuser else "staff"
                loginInfo={"username":username,"name":user[0].first_name,"role":role,"ticket":token.key,"userid":user[0].id,"expire":86400}
                return JsonResponse(data=loginInfo, code="999999", msg="成功")
            else:
                return JsonResponse(data="用户名或密码错误!", code="999995", msg="用户名或密码错误!")
        else:
            try:
                secret_key=MD5.encrypt("%s-%s-%s-%s" % (username,password,ssoClientId,ssoClientSecret))
                params={"cmd":"80010003","data":{"username":username,"password":password,"client_id":ssoClientId,"secret_key":secret_key}}
                response=requests.post(url=ssoValidateUrl,json=params).json()
                if response["code"]==0:
                    user=User.objects.filter(username=username)
                    role="admin" if user[0].is_superuser else "staff"
                    loginInfo={"username":username,"name":user[0].first_name,"role":role,"ticket":response["data"]["ticket"],"userid":response["data"]["identifier"],"expire":response["data"]["expire"]}
                    return JsonResponse(data=loginInfo, code="999999", msg="成功")
                else:
                    user=User.objects.filter(username=username,password=password)
                    if user:
                        token,created= Token.objects.get_or_create(user=user[0])
                        role="admin" if user[0].is_superuser else "staff"
                        loginInfo={"username":username,"name":user[0].first_name,"role":role,"ticket":token.key,"userid":user[0].id,"expire":86400}
                        return JsonResponse(data=loginInfo, code="999999", msg="成功")
                    else:
                        return JsonResponse(data="用户名或密码错误!", code="999995", msg="用户名或密码错误!")
            except:
                logging.error(traceback.format_exc())

class SSOLogin(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not ssoLogin:
            serializer = self.serializer_class(data=request.data,
                                               context={"request": request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            # token, created = Token.objects.get_or_create(user=user)
            data = TokenSerializer(Token.objects.get(user=user)).data
            data["userphoto"] = '/file/userphoto.jpg'
            return JsonResponse(data=data, code="999999", msg="成功")
        else:
            try:
                data = request.data
                username=data["username"]
                password=MD5.encrypt(data["password"])
                secret_key=MD5.encrypt("%s-%s-%s-%s" % (username,password,ssoClientId,ssoClientSecret))
                params={"cmd":"80010003","data":{"username":username,"password":password,"client_id":ssoClientId,"secret_key":secret_key}}
                response=requests.post(url=ssoValidateUrl,json=params).json()
                if response["code"]==0:
                    loginInfo={"username":username,"name":response["data"]["name"],"ticket":response["data"]["ticket"],"userid":response["data"]["identifier"],"expire":response["data"]["expire"]}
                    return JsonResponse(data=loginInfo, code="999999", msg="成功")
                else:
                    return JsonResponse(data=response["msg"], code="999995", msg=response["msg"])
            except:
                logging.error(traceback.format_exc())

class Logout(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            if ssoLogin:
                url="%s?redirect_uri=%s" % (ssoLogoutUrl,ssoRedirectUrl)
                requests.get(url=url)
            return JsonResponse(data={}, code="999999", msg="成功")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(data={}, code="999995", msg="失败")


class GetUsers(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")
        try:
            users=getUsers()
            users=list(filter(lambda user:len(UserProfile.objects.filter(user__username=user["user_name"]))==0,users))
            paginator = Paginator(users, page_size)  # paginator对象
            pages = paginator.num_pages  # 总页数
            total = len(users)
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        except:
            logging.error(traceback.format_exc())
        return JsonResponse(data={"data": obm.object_list,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")


class LinkUsers(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("")
    def post(self, request):
        """
        添加Config
        :param request:
        :return:
        """
        data = request.data
        with transaction.atomic():
            try:
                users=getUsers()
                for user in users:
                    if user["user_id"] in data["ids"]:
                        obj=User.objects.create(username=user["user_name"],first_name=user["name"],email=user["email"],is_staff=True)
                        UserProfile.objects.create(user=obj,phone=user["phone"],type="global")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999996", msg="执行失败！")
            return JsonResponse(code="999999", msg="成功！")

class UserList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用户列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999995", msg="page and page_size must be integer！")
        name = request.GET.get("name")
        if name:
            obis = UserProfile.objects.filter(user__username__contains=name).order_by("-id")
        else:
            obis = UserProfile.objects.filter().order_by("-id")
        paginator = Paginator(obis, page_size)  # paginator对象
        pages = paginator.num_pages  # 总页数
        total = len(obis)
        try:
            obm = paginator.page(page)
            serialize = UserSerializer(obm, many=True)
            data=serialize.data
            return JsonResponse(data={"data": data,
                                  "page": page,
                                  "pages": pages,
                                  "total": total
                                  }, code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")


class AddUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("")
    def post(self, request):
        """
        添加Config
        :param request:
        :return:
        """
        data = request.data
        try:
            with transaction.atomic():
                obj=User.objects.filter(username=data["username"])
                if obj:
                    return JsonResponse(code="999998", msg="该用户名已注册！")
                obj=User.objects.create(username=data["username"],password=data["password"],first_name=data["name"],email=data["email"],is_staff=True)
                UserProfile.objects.create(user=obj,phone=data["phone"],type="local")
                return JsonResponse(data={
                    "user_id": obj.id
                }, code="999999", msg="成功！")
        except:
            logging.error(traceback.format_exc())
            return JsonResponse(code="999998", msg="失败！")


class UpdateUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("")
    def post(self, request):
        """
        修改配置
        :param request:
        :return:
        """
        data = request.data
        try:
            obi = User.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="用户不存在！")
        username = User.objects.filter(username=data["username"]).exclude(id=data["id"])
        if len(username):
            return JsonResponse(code="999997", msg="存在相同用户名！")
        else:
            try:
                with transaction.atomic():
                    UserProfile.objects.filter(user=obi).update(phone=data["phone"])
                    obi.username=data["username"]
                    obi.password=data["password"]
                    obi.first_name=data["name"]
                    obi.email=data["email"]
                    obi.save()
                    return JsonResponse(code="999999", msg="成功！")
            except:
                logging.error(traceback.format_exc())
                return JsonResponse(code="999998", msg="失败！")

class DelUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @permission_required("")
    def post(self, request):
        """
        删除配置
        :param request:
        :return:
        """
        data =request.data
        try:
            for j in data["ids"]:
                obj = User.objects.filter(id=j)
                if obj:
                    obj.delete()
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="不存在！")

def getUsers():
    users=[]
    secret_key=MD5.encrypt("%s-%s" % (ssoClientId,ssoClientSecret))
    params={"cmd":"80010005","data":{"client_id":ssoClientId,"secret_key":secret_key}}
    try:
        response=requests.post(url=ssoValidateUrl,json=params).json()
        if response["code"]==0:
            users=response["data"]
    except:
        logging.error(traceback.format_exc())
    finally:
        return users