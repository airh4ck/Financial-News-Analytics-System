FROM pytorch/pytorch
COPY . /app
# COPY ./database/database.db /app/database/database.db

RUN apt update
RUN apt upgrade -y
RUN apt -y install libpq-dev gcc

RUN pip3 install --default-timeout=900 -r /app/requirements.txt

CMD ["python3", "-u", "/app/main.py"]
