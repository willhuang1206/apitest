ps -ef | grep apitest | grep -v grep | awk '{print "kill -9 "$2}'|sh
nohup python3 manage.py runserver 0.0.0.0:8092 --settings=apitest.settings.prod &