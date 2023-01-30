# Financial News Analytics System

## Description

This repository contains the source code for the aggregator of financial analytics in russian language. The following news sources are supported:

* investing.com
* instaforex.com

In addition to aggregating analytical articles, the following data is extracted from those articles:

* sentiment of the article
* summary of the article
* indices of authors

## Usage

The following `docker-compose.yml` file was used to start the application:

```yml
version: '3.6'
networks:
  default:
    name: fnap_network

services:
  kafka-client:
    image: 'bitnami/kafka:latest'
    command: sleep infinity
  zookeeper:
    image: 'bitnami/zookeeper:latest'
    ports:
      - '2181:2181'
    environment:
      ALLOW_ANONYMOUS_LOGIN: 'yes'
  kafka:
    image: 'bitnami/kafka:latest'
    ports:
      - '9092:9092'
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_LISTENERS=CLIENT://:29092,EXTERNAL://:9092
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka:29092,EXTERNAL://localhost:9092
      - KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
    depends_on:
      - zookeeper

  selenium:
    image: selenium/standalone-chrome
    container_name: selenium
    shm_size: 2g
    ports:
      - 4444:4444

  # Grabber for instaforex.com
  instaforex_parser:
    image: airh4ck/instaforex_parser
    depends_on:
      - zookeeper
      - kafka
      - selenium

  # Grabber for investing.com
  investing_parser:
    image: airh4ck/investing_parser
    depends_on:
      - zookeeper
      - kafka

  # Author indexing microservice
  indexer:
    restart: always
    image: airh4ck/indexer
    depends_on:
      - kafka
    environment:
      - DATABASE_NAME=${DATABASE_NAME}
      - DATABASE_USERNAME=${DATABASE_USERNAME}
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}

  # Sentiment analysis microservice
  sentiment_analysis:
    restart: always
    image: airh4ck/sentiment_analysis
    depends_on:
      - kafka
    environment:
      - DATABASE_NAME=${DATABASE_NAME}
      - DATABASE_USERNAME=${DATABASE_USERNAME}
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}

  # Summarization microservice
  summarization:
    restart: always
    image: airh4ck/summarization
    depends_on:
      - kafka
    environment:
      - DATABASE_NAME=${DATABASE_NAME}
      - DATABASE_USERNAME=${DATABASE_USERNAME}
      - DATABASE_PASSWORD=${DATABASE_PASSWORD}
```

All of the necessary images are available on [Docker Hub](https://hub.docker.com/u/airh4ck).
