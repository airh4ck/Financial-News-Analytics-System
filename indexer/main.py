import os

from json import loads, load, dump
from kafka import KafkaConsumer


if __name__ == "__main__":
    topics = ['investing-events', 'instaforex-events']
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=['kafka:29092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='indexer_consumer',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    print("Uploading received data...")
    for entry in consumer:
        articleInfo = entry.value
        authorIDs = None
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'author_ids.json')
        with open(filename, 'r+') as jsonFile:
            authorIDs = load(jsonFile)

            if authorIDs.get(articleInfo["author"], 0):
                articleInfo["author_id"] = authorIDs[articleInfo["author"]]
            else:
                articleInfo["author_id"] = authorIDs["next_id"]
                authorIDs[articleInfo["author"]] = authorIDs["next_id"]
                authorIDs["next_id"] += 1

            print(articleInfo["author_id"])

            jsonFile.seek(0)
            dump(authorIDs, jsonFile)
            jsonFile.truncate()

        print("Uploaded entry successfully!")
