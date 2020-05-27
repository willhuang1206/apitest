#nohup java -jar api-service-1.0.0.jar --spring.profiles.active=docker --server.ip=127.0.0.1 --server.port=8091 &
nohup python3 manage.py runserver 0.0.0.0:8092 --settings=autotest.settings.prod &