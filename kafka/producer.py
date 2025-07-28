import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

users = ['user_1', 'user_2', 'user_3', 'user_4']
actions = ['click', 'view', 'purchase', 'logout']

def generate_event():
    return {
        'user_id': random.choice(users),
        'action': random.choice(actions),
        'timestamp': datetime.utcnow().isoformat()
    }

if __name__ == '__main__':
    while True:
        event = generate_event()
        print(f"Sending: {event}")
        producer.send('events', value=event)
        time.sleep(1)
