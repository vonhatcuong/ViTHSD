import json
import datetime as dt

from kafka import KafkaProducer, KafkaConsumer


def initProducer():
    # init an instance of KafkaProducer
    producer = KafkaProducer(
      bootstrap_servers='localhost:9092',
      value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer


def initConsumer(topic, timeout=1000):
    # init an instance of KafkaConsumer
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id=None,
        auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=timeout,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    return consumer


def produceRecord(data, producer, topic, partition=0):
    # act as a producer sending records on kafka
    producer.send(topic=topic, partition=partition, value=data)
    # debug \ message in prompt
    # print('Produce record to topic \'{0}\' at time {1}'.format(topic, dt.datetime.utcnow()))

def consumeRecord(consumer):
    rec_list = []
    # append to list any new records in consumer
    for rec in consumer:
        r = rec.value
        rec_list.append(r)
    # return list of new records
    return rec_list