FROM pytorch/pytorch
COPY . /app
# COPY ./database/database.db /app/database/database.db


# RUN apt-get update -y
RUN pip install --no-cache-dir -r /app/requirements.txt

SHELL [ "/bin/bash", "-c" ]
RUN  python3 -c $'from transformers import MBartTokenizer, MBartForConditionalGeneration \n\
modelName = "IlyaGusev/mbart_ru_sum_gazeta" \n\
tokenizer = MBartTokenizer.from_pretrained(modelName) \n\
model = MBartForConditionalGeneration.from_pretrained(modelName)'

CMD ["python3", "-u", "/app/main.py"]
