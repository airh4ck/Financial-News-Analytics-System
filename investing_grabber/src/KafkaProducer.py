from json import dumps
from kafka import KafkaProducer


def uploadData(data):
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    for entry in data:
        producer.send('analytical-articles', value=entry)

    print("Uploaded data to Kafka topic.")
