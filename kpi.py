import mysql.connector
import json
from datetime import datetime



#import mysql.connector

# Connect to MySQL
db_connection = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="root",       # Replace with your MySQL username
    password="jayzilpilwar2706",  # Replace with your MySQL password
    database="mcq_test"  # Replace with your database name
)

cursor = db_connection.cursor()

def fetch_kpis():
    # KPI 1: How many tests were started?
    cursor.execute("""
        SELECT COUNT(DISTINCT test_id) AS tests_started
        FROM test_sessions
        WHERE start_time IS NOT NULL AND is_completed = FALSE;
    """)
    tests_started = cursor.fetchone()[0]

    # KPI 2: How many tests were completed?
    cursor.execute("""
        SELECT COUNT(DISTINCT test_id) AS tests_completed
        FROM test_sessions
        WHERE end_time IS NOT NULL AND is_completed = TRUE;
    """)
    tests_completed = cursor.fetchone()[0]

    # KPI 3: How many tests were not completed and reasons for it
    cursor.execute("""
        SELECT COUNT(DISTINCT test_id) AS tests_not_completed
        FROM test_sessions
        WHERE end_time IS NULL AND is_completed = FALSE;
    """)
    tests_not_completed = cursor.fetchone()[0]

    # KPI 4: Timeline for each action (question) taken by the student
    cursor.execute("""
        SELECT 
            test_id,
            student_id,
            question_id,
            timestamp,
            response_time_seconds,
            TIMESTAMPDIFF(SECOND, 
                (SELECT timestamp 
                 FROM question_responses 
                 WHERE test_id = q.test_id AND student_id = q.student_id AND question_id = q.question_id 
                 ORDER BY timestamp ASC LIMIT 1), q.timestamp) AS time_to_reach_question
        FROM question_responses q
        ORDER BY test_id, student_id, timestamp;
    """)
    question_timeline = cursor.fetchall()

    # KPI 5: Funnel view to show the test performance
    cursor.execute("""
        SELECT 
            test_id,
            COUNT(DISTINCT question_id) AS total_questions,
            SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) AS correct_answers,
            SUM(CASE WHEN NOT is_correct THEN 1 ELSE 0 END) AS incorrect_answers
        FROM question_responses
        GROUP BY test_id;
    """)
    funnel_view = cursor.fetchall()

    # KPI 6: Session-level stats
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT session_id) AS total_sessions,
            AVG(TIMESTAMPDIFF(SECOND, start_time, end_time)) AS average_session_duration
        FROM test_sessions
        WHERE end_time IS NOT NULL;
    """)
    session_stats = cursor.fetchone()

    # KPI 7: Question-level stats (Most time-consuming question)
    cursor.execute("""
        SELECT 
            question_id,
            SUM(response_time_seconds) AS total_time_spent,
            COUNT(DISTINCT student_id) AS times_answered
        FROM question_responses
        GROUP BY question_id
        ORDER BY total_time_spent DESC
        LIMIT 1;
    """)
    most_time_consuming_question = cursor.fetchone()

    # Most answered questions
    cursor.execute("""
        SELECT 
            question_id,
            COUNT(DISTINCT student_id) AS times_answered,
            SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) AS correct_answers
        FROM question_responses
        GROUP BY question_id
        ORDER BY correct_answers DESC
        LIMIT 1;
    """)
    most_answered_question = cursor.fetchone()

    # Mostly revisited question
    cursor.execute("""
        SELECT 
            question_id,
            COUNT(DISTINCT response_id) AS response_count
        FROM question_responses
        GROUP BY question_id
        ORDER BY response_count DESC
        LIMIT 1;
    """)
    most_revisited_question = cursor.fetchone()

    # Mostly answered wrong question
    cursor.execute("""
        SELECT 
            question_id,
            COUNT(DISTINCT student_id) AS times_answered,
            SUM(CASE WHEN NOT is_correct THEN 1 ELSE 0 END) AS wrong_answers
        FROM question_responses
        GROUP BY question_id
        ORDER BY wrong_answers DESC
        LIMIT 1;
    """)
    most_wrong_answered_question = cursor.fetchone()

    # Print all KPIs
    print(f"Tests Started: {tests_started}")
    print(f"Tests Completed: {tests_completed}")
    print(f"Tests Not Completed: {tests_not_completed}")
    
    print("\nQuestion Action Timeline:")
    for row in question_timeline:
        print(f"Test ID: {row[0]}, Student ID: {row[1]}, Question ID: {row[2]}, Timestamp: {row[3]}, Time to Reach Question: {row[5]} seconds")

    print("\nFunnel View (Test Performance):")
    for row in funnel_view:
        print(f"Test ID: {row[0]}, Total Questions: {row[1]}, Correct Answers: {row[2]}, Incorrect Answers: {row[3]}")

    print(f"\nSession Level Stats: Total Sessions: {session_stats[0]}, Average Session Duration: {session_stats[1]} seconds")
    
    print("\nMost Time-Consuming Question:")
    print(f"Question ID: {most_time_consuming_question[0]}, Total Time Spent: {most_time_consuming_question[1]} seconds, Times Answered: {most_time_consuming_question[2]}")

    print("\nMost Answered Question:")
    print(f"Question ID: {most_answered_question[0]}, Times Answered: {most_answered_question[1]}, Correct Answers: {most_answered_question[2]}")

    print("\nMost Revisited Question:")
    print(f"Question ID: {most_revisited_question[0]}, Response Count: {most_revisited_question[1]}")

    print("\nMost Wrong Answered Question:")
    print(f"Question ID: {most_wrong_answered_question[0]}, Wrong Answers: {most_wrong_answered_question[1]}")

fetch_kpis()

# Close the database connection
cursor.close()
db_connection.close()
