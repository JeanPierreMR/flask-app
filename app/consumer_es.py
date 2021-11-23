from kafka import KafkaConsumer
from json import loads
from time import sleep
from elasticsearch import Elasticsearch

# connect to our cluster Elastic Search
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.delete(index='houses_index', ignore=[400, 404])
es.indices.delete(index='citas_index', ignore=[400, 404])

consumer = KafkaConsumer(
    'topic_es',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for event in consumer:
    event_data = event.value
    try:
        metercita(event_data)
    except:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


