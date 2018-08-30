FROM python:3

LABEL maintainer="pablo@sequel.ninja"
ARG VERSION=filebeat-5.6.0-linux-x86_64 

RUN wget https://artifacts.elastic.co/downloads/beats/filebeat/$VERSION.tar.gz --quiet
RUN tar -xvzf $VERSION.tar.gz
RUN mv $VERSION /opt/filebeat
RUN rm -rf $VERSION.tar.gz
RUN mkdir -p /templates
ADD templates/filebeat.j2 /templates/filebeat.j2
ADD resend.py /resend.py
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt 

ENTRYPOINT ["/resend.py"]
