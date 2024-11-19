CREATE database if not   EXISTS mcq_test;
USE mcq_test;

-- Table to track tests
CREATE TABLE tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(255),
    total_questions INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to track test sessions
CREATE TABLE test_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    student_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP NULL,
    is_completed BOOLEAN DEFAULT FALSE
);

-- Table to store question responses
CREATE TABLE question_responses (
    response_id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT,
    student_id INT,
    question_id INT,
    answer VARCHAR(10),
    is_correct BOOLEAN,
    response_time_seconds INT,
    timestamp TIMESTAMP
);