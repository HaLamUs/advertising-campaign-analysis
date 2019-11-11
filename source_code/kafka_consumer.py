from kafka import KafkaConsumer
import json
import pymongo

# consumer = KafkaConsumer('test', auto_offset_reset='earliest', value_deserializer=lambda value: json.loads(value))

# mongo
client = pymongo.MongoClient("localhost", 27017)
db = client.lam_db
# kafka consumer
consumer = KafkaConsumer('lam-test-topic-rep3', value_deserializer=lambda value: json.loads(value))

for msg in consumer:
  tweet_content: dict = msg.value
  # msg = {"id": 1181304064644177922, "id_str": '1181304064644177922'}
# print(msg["id_str"])
  id_str = tweet_content["id_str"]
  tweet = db.test_table.find_one({"id_str":id_str})
  if tweet is not None:
	print('it existed')
  else:
	print('ok save it, comrade')
	tweet_content["fetching_hashtag"] = "#WGDP"
	id = tweet_content["id"]
	if id % 2 == 0:
  	tweet_content["sentiment"] = "positive"
	else:  
  	tweet_content["sentiment"] = "negative"
	print(tweet_content)
	db.test_table.insert_one(tweet_content)
  #print(tweet_content)
