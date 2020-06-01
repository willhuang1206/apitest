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

SERVER_HOST="106.53.246.180"
SERVER_PORT="8092"

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

REPORT_URL = 'http://%s/#/report' % SERVER_HOST
AUTO_URL = 'http://%s:%s' % (SERVER_HOST,SERVER_PORT)

SCHEDULE_START=True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SSO_LOGIN=False
SSO_CLIENTID="apitest"
SSO_CLIENTSECRET=""
SSO_REDIRECTURL=AUTO_URL
SSO_NOTIFYURL="%s/ssologin" % AUTO_URL

SSO_GETTICKETURL=""
SSO_VALIDATEURL=""
SSO_LOGINURL=""
SSO_LOGOUTURL=""