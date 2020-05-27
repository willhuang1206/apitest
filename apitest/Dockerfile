FROM python:3.6

MAINTAINER willhuang

ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai
# Install required packages and remove the apt packages cache when done.

WORKDIR /opt/workspace/ApiTest/

COPY . .

RUN  pip3 install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=100
#    ln -s /opt/workspace/ApiTest/nginx.conf /etc/nginx/sites-enabled/

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ENV JAVA_HOME=/opt/workspace/ApiTest/jdk8
ENV JRE_HOME=$JAVA_HOME/jre
ENV CLASSPATH=$JAVA_HOME/bin/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib:$CLASSPATH
ENV PATH=$JAVA_HOME/bin:$PATH

#CMD python3 manage.py runserver 0.0.0.0:8000
CMD sh start.sh