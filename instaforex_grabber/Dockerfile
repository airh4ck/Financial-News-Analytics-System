FROM python:3.9.15
COPY . /app

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "-u", "run.py"]
