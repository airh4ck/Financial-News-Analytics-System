from json import loads
from kafka import KafkaConsumer

import analyze
import uploader

if __name__ == "__main__":
    topics = ['analytical-articles']
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=['kafka:29092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='sentiment_consumer',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    tokenizer = analyze.create_tokenizer()
    model = analyze.create_model()

    for entry in consumer:
        articleInfo = entry.value
        print(articleInfo['link'])
        articleInfo['sentiment'] = analyze.predict(articleInfo['text'], tokenizer, model)[0]
        uploader.update_row(articleInfo)
