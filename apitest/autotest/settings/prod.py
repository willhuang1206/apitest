"""
Django settings for autotest project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
1570035295418200523859
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from .base import *

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',     # 数据库类型，mysql
        'NAME':'apitest',            #  database名
        'USER':'apitest',               # 登录用户
        'PASSWORD':'123456',        #  登录用户名
        'HOST':'127.0.0.1',        # 数据库地址
        'PORT':'3306'              # 数据库端口
    }
}

REPORT_URL = 'http://106.53.246.180/#/report'
AUTO_URL = 'http://106.53.246.180:8092'
PUBLISH_TEST_URL= ''
PUBLISH_LIST_URL= ''

SCHEDULE_START=True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SSO_LOGIN=False
SSO_CLIENTID="apitest"
SSO_CLIENTSECRET="4587feb504e6e92758a3801335e8a5d5"
SSO_REDIRECTURL="http://106.53.246.180:8092"
SSO_NOTIFYURL="http://106.53.246.180:8092/ssologin"

SSO_GETTICKETURL="http://xyz.com/system/getTicket"
SSO_VALIDATEURL="http://xyz.com/out"
SSO_LOGINURL="http://xyz.com/site/setLoginState"
SSO_LOGOUTURL="http://xyz.com/site/setLogOutState"