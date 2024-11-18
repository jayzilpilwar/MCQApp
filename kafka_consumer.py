from kafka import KafkaConsumer
import mysql.connector
import json

# MySQL connection
db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jayzilpilwar2706",
    database="mcq_test"
)
cursor = db_conn.cursor()

# Kafka consumer setup
consumer = KafkaConsumer(
    'test_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_event(event):
    event_type = event["type"]
    if event_type == "test_started":
        query = """
        INSERT INTO test_sessions (test_id, student_id, start_time)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (event["test_id"], event["student_id"], event["timestamp"]))

    elif event_type == "question_answered":
        query = """
        INSERT INTO question_responses (test_id, student_id, question_id, answer, is_correct, response_time_seconds, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (event["test_id"], event["student_id"], event["question_id"], event["answer"],
                               event["is_correct"], event["response_time_seconds"], event["timestamp"]))

    elif event_type == "test_completed":
        query = """
        UPDATE test_sessions
        SET end_time = %s, is_completed = TRUE
        WHERE test_id = %s AND student_id = %s
        """
        cursor.execute(query, (event["timestamp"], event["test_id"], event["student_id"]))

    db_conn.commit()

if __name__ == "__main__":
    for msg in consumer:
        process_event(msg.value)
