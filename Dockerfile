FROM python:3.7
RUN apt-get update -y
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /opt/code
WORKDIR /opt/code

ENTRYPOINT ["./run.sh"]
CMD ["nop"]
