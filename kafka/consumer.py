import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Starting consumer...")

for message in consumer:
    event = message.value
    print(f"Received event: {event}")
