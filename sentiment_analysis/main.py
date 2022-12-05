from json import loads
from kafka import KafkaConsumer

import analyze
import uploader

if __name__ == "__main__":
    topics = ['investing-events', 'instaforex-events']
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=['kafka:29092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='sentiment_consumer',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    for entry in consumer:
        articleInfo = entry.value
        print(articleInfo['link'])
        articleInfo['sentiment'] = analyze.predict(articleInfo['text'])[0]
        uploader.update_row(articleInfo)
