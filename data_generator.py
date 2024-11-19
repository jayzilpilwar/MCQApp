import random
import time
from datetime import datetime
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_test_events():
    test_id = random.randint(1, 10)
    student_id = random.randint(1, 100)
    event_type = random.choice(["test_started", "question_answered", "test_completed"])

    if event_type == "test_started":
        return {
            "type": event_type,
            "test_id": test_id,
            "student_id": student_id,
            "timestamp": str(datetime.now())
        }
    elif event_type == "question_answered":
        question_id = random.randint(1, 50)
        is_correct = random.choice([True, False])
        response_time = random.randint(5, 60)
        return {
            "type": event_type,
            "test_id": test_id,
            "student_id": student_id,
            "question_id": question_id,
            "answer": random.choice(["A", "B", "C", "D"]),
            "is_correct": is_correct,
            "response_time_seconds": response_time,
            "timestamp": str(datetime.now())
        }
    elif event_type == "test_completed":
        return {
            "type": event_type,
            "test_id": test_id,
            "student_id": student_id,
            "timestamp": str(datetime.now())
        }

def produce_events():
    while True:
        event = generate_test_events()
        producer.send('test_events', event)
        print(f"Produced event: {event}")
        time.sleep(5)

if __name__ == "__main__":
    produce_events()