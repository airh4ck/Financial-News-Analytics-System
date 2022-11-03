import sys
import json

if __name__ == "__main__":
    # TODO: get article info from Apache Kafka

    articleInfo = None
    with open(sys.argv[1], 'r') as file:
        articleInfo = json.load(file)

    authorIDs = None
    with open("./author_ids.json", 'r+') as jsonFile:
        authorIDs = json.load(jsonFile)

        if authorIDs.get(articleInfo["author"], 0):
            articleInfo["id"] = authorIDs[articleInfo["author"]]
        else:
            articleInfo["id"] = authorIDs["next_id"]
            authorIDs[articleInfo["author"]] = authorIDs["next_id"]
            authorIDs["next_id"] += 1

        print(articleInfo["id"])

        jsonFile.seek(0)
        json.dump(authorIDs, jsonFile)
        jsonFile.truncate()

    # TODO: upload `articleInfo` to the database
