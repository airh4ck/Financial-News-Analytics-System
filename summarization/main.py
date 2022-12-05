from json import loads
from kafka import KafkaConsumer

from summarize import summarize


def main():
    topics = ['investing-events', 'instaforex-events']
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=['kafka:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='summarization_consumer',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    print("Uploading received data...")
    for entry in consumer:
        articleInfo = entry.value
        print(articleInfo['link'])
        articleInfo['summary'] = summarize(articleInfo['text'])
        print(articleInfo['summary'])


        # print("Uploaded entry successfully! ")


if __name__ == "__main__":
    main()
