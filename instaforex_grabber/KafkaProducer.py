from json import dumps
from kafka import KafkaProducer


def uploadData(data):
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    
    currency = data['pair']
    data['pair'] = currency[:3] + "_" + currency[3:]
    
    producer.send('analytical-articles', value=data)

    print("Uploaded data to Kafka topic.")
