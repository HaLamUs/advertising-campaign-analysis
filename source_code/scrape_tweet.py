import twint
import sys
from kafka import KafkaProducer
import json
module = sys.modules["twint.storage.write"]

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
if producer is not None:
  print('good it is not nil')

def Json(obj, config):
  tweet = obj.__dict__
  print(tweet)
  producer.send('lam-test-topic-rep3', tweet)
  producer.flush()

module.Json = Json

def fetch(hashtag):
  c = twint.Config()
  c.Search = hashtag
  c.Store_json = True
  c.Store_object = True
  c.Output = "tweets.json"
  c.Since = "2019-10-01"
  c.Hide_output = True
  twint.run.Search(c)

fetch('#WGDP')
