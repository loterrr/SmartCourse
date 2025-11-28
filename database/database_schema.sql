-- Database Schema for Smart Course Recommendation System

CREATE DATABASE IF NOT EXISTS course_recommendation_db;
USE course_recommendation_db;

-- Students Table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    high_school_gpa DECIMAL(3,2),
    intended_major VARCHAR(100),
    career_interests JSON,
    learning_style VARCHAR(50),
    study_hours_preference INT,
    extracurricular_interests JSON,
    profile_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_student_id (student_id)
);

-- Courses Table
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 5),
    description TEXT,
    prerequisites JSON,
    career_relevance JSON,
    learning_styles JSON,
    workload_hours INT,
    max_enrollment INT,
    current_enrollment INT DEFAULT 0,
    semester_offered VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_course_code (course_code),
    INDEX idx_department (department)
);

-- Course Preferences Table
CREATE TABLE course_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    preference_level INT CHECK (preference_level BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_preference (student_id, course_id)
);

-- Recommendations Table
CREATE TABLE recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    confidence_score DECIMAL(5,2),
    reasoning TEXT,
    algorithm_version VARCHAR(20) DEFAULT '1.0',
    is_accepted BOOLEAN DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_confidence (confidence_score)
);

-- Enrollments Table
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    final_grade VARCHAR(5),
    status VARCHAR(20) DEFAULT 'enrolled',
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, course_id, semester)
);

-- Feedback Table
CREATE TABLE feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    recommendation_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    helpful BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (recommendation_id) REFERENCES recommendations(id) ON DELETE SET NULL,
    INDEX idx_rating (rating)
);

-- System Logs Table
CREATE TABLE system_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    action_type VARCHAR(100),
    action_details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL,
    INDEX idx_action (action_type),
    INDEX idx_date (created_at)
);

-- Analytics Table
CREATE TABLE analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    metric_name VARCHAR(100),
    metric_value DECIMAL(10,2),
    metric_category VARCHAR(50),
    semester VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric (metric_name),
    INDEX idx_category (metric_category)
);

-- Sample Data Insertion

-- Insert Sample Courses
INSERT INTO courses (course_code, course_name, department, credits, difficulty_level, 
    description, prerequisites, career_relevance, learning_styles, workload_hours, 
    max_enrollment, semester_offered) VALUES

('CS101', 'Introduction to Computer Science', 'Computer Science', 3, 2,
    'Fundamental concepts of programming and computational thinking',
    '[]', '["Software Engineering", "Data Science", "IT"]', 
    '["Visual", "Hands-on"]', 8, 50, 'Fall,Spring'),

('MATH151', 'Calculus I', 'Mathematics', 4, 4,
    'Limits, derivatives, and introduction to integration',
    '[]', '["Engineering", "Data Science", "Finance"]',
    '["Analytical", "Practice-based"]', 12, 40, 'Fall,Spring'),

('ENG101', 'English Composition', 'English', 3, 2,
    'Academic writing and critical reading skills',
    '[]', '["All"]', '["Reading", "Writing"]', 6, 30, 'Fall,Spring'),

('PHYS101', 'General Physics I', 'Physics', 4, 4,
    'Mechanics, waves, and thermodynamics',
    '["MATH151"]', '["Engineering", "Science", "Medical"]',
    '["Visual", "Analytical"]', 10, 35, 'Fall,Spring'),

('BIO101', 'Introduction to Biology', 'Biology', 4, 3,
    'Cell biology, genetics, and evolution',
    '[]', '["Medical", "Research", "Healthcare"]',
    '["Visual", "Reading"]', 9, 45, 'Fall,Spring'),

('ECON101', 'Principles of Economics', 'Economics', 3, 3,
    'Microeconomics and macroeconomics fundamentals',
    '[]', '["Business", "Finance", "Policy"]',
    '["Analytical", "Reading"]', 7, 40, 'Fall,Spring'),

('CHEM101', 'General Chemistry', 'Chemistry', 4, 4,
    'Atomic structure, bonding, and chemical reactions',
    '[]', '["Medical", "Engineering", "Research"]',
    '["Hands-on", "Analytical"]', 11, 35, 'Fall,Spring'),

('PSYCH101', 'Introduction to Psychology', 'Psychology', 3, 2,
    'Human behavior, cognition, and mental processes',
    '[]', '["Healthcare", "Education", "Research"]',
    '["Reading", "Discussion"]', 6, 50, 'Fall,Spring'),

('HIST101', 'World History', 'History', 3, 2,
    'Major civilizations and historical developments',
    '[]', '["Education", "Law", "Policy"]',
    '["Reading", "Writing"]', 7, 35, 'Fall,Spring'),

('ART101', 'Introduction to Visual Arts', 'Art', 3, 2,
    'Elements of design and art history',
    '[]', '["Design", "Media", "Education"]',
    '["Visual", "Hands-on"]', 8, 25, 'Fall,Spring');

-- Create Admin User
INSERT INTO students (student_id, first_name, last_name, email, password, 
    high_school_gpa, intended_major, profile_completed) VALUES
('ADMIN001', 'System', 'Administrator', 'admin@university.edu', 
    '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 
    4.00, 'Administration', TRUE);

-- Create Views for Analytics

CREATE VIEW student_enrollment_summary AS
SELECT 
    s.id AS student_id,
    s.student_id AS student_number,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    s.intended_major,
    COUNT(e.id) AS total_enrollments,
    AVG(CASE WHEN e.final_grade IS NOT NULL THEN 
        CASE e.final_grade
            WHEN 'A' THEN 4.0
            WHEN 'B' THEN 3.0
            WHEN 'C' THEN 2.0
            WHEN 'D' THEN 1.0
            ELSE 0.0
        END
    END) AS current_gpa
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
GROUP BY s.id;

CREATE VIEW recommendation_accuracy AS
SELECT 
    r.algorithm_version,
    COUNT(*) AS total_recommendations,
    SUM(CASE WHEN r.is_accepted = TRUE THEN 1 ELSE 0 END) AS accepted_count,
    AVG(r.confidence_score) AS avg_confidence,
    (SUM(CASE WHEN r.is_accepted = TRUE THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS acceptance_rate
FROM recommendations r
GROUP BY r.algorithm_version;

CREATE VIEW course_popularity AS
SELECT 
    c.course_code,
    c.course_name,
    c.department,
    COUNT(e.id) AS enrollment_count,
    AVG(f.rating) AS avg_rating,
    c.max_enrollment,
    (COUNT(e.id) / c.max_enrollment) * 100 AS fill_rate
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
LEFT JOIN recommendations r ON c.id = r.course_id
LEFT JOIN feedback f ON r.id = f.recommendation_id
GROUP BY c.id
ORDER BY enrollment_count DESC;