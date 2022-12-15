FROM ubuntu
COPY . /app

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "-u", "/app/src/main.py"]
