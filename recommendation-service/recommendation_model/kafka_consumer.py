from kafka import KafkaConsumer
from json import loads
import os

topic = 'movielog7'
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'],
    # Read from the start of the topic; Default is latest
    auto_offset_reset='latest',
)

counter = 0
print('Reading Kafka Broker')
for message in consumer:
    if counter > 10000:
        break
    decoded = message.value.decode()
    if "/rate/" in decoded:
        with open("rate.txt", "a") as f:
            f.write("\n")
            f.write(decoded)
    counter+=1