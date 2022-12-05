FROM python:3.9.15
COPY . /app
# COPY ./database/database.db /app/database/database.db

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "-u", "/app/main.py"]
