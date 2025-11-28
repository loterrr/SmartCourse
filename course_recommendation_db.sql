-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2025 at 06:36 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `course_recommendation_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `analytics`
--

CREATE TABLE `analytics` (
  `id` int(11) NOT NULL,
  `metric_name` varchar(100) DEFAULT NULL,
  `metric_value` decimal(10,2) DEFAULT NULL,
  `metric_category` varchar(50) DEFAULT NULL,
  `semester` varchar(50) DEFAULT NULL,
  `recorded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `course_name` varchar(255) NOT NULL,
  `department` varchar(100) NOT NULL,
  `credits` int(11) NOT NULL,
  `difficulty_level` int(11) DEFAULT NULL CHECK (`difficulty_level` between 1 and 5),
  `description` text DEFAULT NULL,
  `prerequisites` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`prerequisites`)),
  `career_relevance` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`career_relevance`)),
  `learning_styles` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`learning_styles`)),
  `workload_hours` int(11) DEFAULT NULL,
  `max_enrollment` int(11) DEFAULT NULL,
  `current_enrollment` int(11) DEFAULT 0,
  `semester_offered` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `course_code`, `course_name`, `department`, `credits`, `difficulty_level`, `description`, `prerequisites`, `career_relevance`, `learning_styles`, `workload_hours`, `max_enrollment`, `current_enrollment`, `semester_offered`, `is_active`, `created_at`) VALUES
(1, 'CS101', 'Introduction to Computer Science', 'Computer Science', 3, 2, 'Fundamental concepts of programming and computational thinking', '[]', '[\"Software Engineering\", \"Data Science\", \"IT\"]', '[\"Visual\", \"Hands-on\"]', 8, 50, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(2, 'MATH151', 'Calculus I', 'Mathematics', 4, 4, 'Limits, derivatives, and introduction to integration', '[]', '[\"Engineering\", \"Data Science\", \"Finance\"]', '[\"Analytical\", \"Practice-based\"]', 12, 40, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(3, 'ENG101', 'English Composition', 'English', 3, 2, 'Academic writing and critical reading skills', '[]', '[\"All\"]', '[\"Reading\", \"Writing\"]', 6, 30, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(4, 'PHYS101', 'General Physics I', 'Physics', 4, 4, 'Mechanics, waves, and thermodynamics', '[\"MATH151\"]', '[\"Engineering\", \"Science\", \"Medical\"]', '[\"Visual\", \"Analytical\"]', 10, 35, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(5, 'BIO101', 'Introduction to Biology', 'Biology', 4, 3, 'Cell biology, genetics, and evolution', '[]', '[\"Medical\", \"Research\", \"Healthcare\"]', '[\"Visual\", \"Reading\"]', 9, 45, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(6, 'ECON101', 'Principles of Economics', 'Economics', 3, 3, 'Microeconomics and macroeconomics fundamentals', '[]', '[\"Business\", \"Finance\", \"Policy\"]', '[\"Analytical\", \"Reading\"]', 7, 40, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(7, 'CHEM101', 'General Chemistry', 'Chemistry', 4, 4, 'Atomic structure, bonding, and chemical reactions', '[]', '[\"Medical\", \"Engineering\", \"Research\"]', '[\"Hands-on\", \"Analytical\"]', 11, 35, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(8, 'PSYCH101', 'Introduction to Psychology', 'Psychology', 3, 2, 'Human behavior, cognition, and mental processes', '[]', '[\"Healthcare\", \"Education\", \"Research\"]', '[\"Reading\", \"Discussion\"]', 6, 50, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(9, 'HIST101', 'World History', 'History', 3, 2, 'Major civilizations and historical developments', '[]', '[\"Education\", \"Law\", \"Policy\"]', '[\"Reading\", \"Writing\"]', 7, 35, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28'),
(10, 'ART101', 'Introduction to Visual Arts', 'Art', 3, 2, 'Elements of design and art history', '[]', '[\"Design\", \"Media\", \"Education\"]', '[\"Visual\", \"Hands-on\"]', 8, 25, 0, 'Fall,Spring', 1, '2025-11-24 07:05:28');

-- --------------------------------------------------------

--
-- Stand-in structure for view `course_popularity`
-- (See below for the actual view)
--
CREATE TABLE `course_popularity` (
`course_code` varchar(20)
,`course_name` varchar(255)
,`department` varchar(100)
,`enrollment_count` bigint(21)
,`avg_rating` decimal(14,4)
,`max_enrollment` int(11)
,`fill_rate` decimal(27,4)
);

-- --------------------------------------------------------

--
-- Table structure for table `course_preferences`
--

CREATE TABLE `course_preferences` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `preference_level` int(11) DEFAULT NULL CHECK (`preference_level` between 1 and 5),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

CREATE TABLE `enrollments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `semester` varchar(50) NOT NULL,
  `enrollment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `final_grade` varchar(5) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'enrolled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrollments`
--

INSERT INTO `enrollments` (`id`, `student_id`, `course_id`, `semester`, `enrollment_date`, `final_grade`, `status`) VALUES
(1, 1, 10, 'Fall 2025', '2025-11-24 08:56:57', NULL, 'enrolled'),
(3, 1, 5, 'Fall 2025', '2025-11-24 08:57:03', NULL, 'enrolled');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `recommendation_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL CHECK (`rating` between 1 and 5),
  `comments` text DEFAULT NULL,
  `helpful` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `confidence_score` decimal(5,2) DEFAULT NULL,
  `reasoning` text DEFAULT NULL,
  `algorithm_version` varchar(20) DEFAULT '1.0',
  `is_accepted` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `recommendation_accuracy`
-- (See below for the actual view)
--
CREATE TABLE `recommendation_accuracy` (
`algorithm_version` varchar(20)
,`total_recommendations` bigint(21)
,`accepted_count` decimal(22,0)
,`avg_confidence` decimal(9,6)
,`acceptance_rate` decimal(29,4)
);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `student_id` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `high_school_gpa` decimal(3,2) DEFAULT NULL,
  `intended_major` varchar(100) DEFAULT NULL,
  `career_interests` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`career_interests`)),
  `learning_style` varchar(50) DEFAULT NULL,
  `study_hours_preference` int(11) DEFAULT NULL,
  `extracurricular_interests` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`extracurricular_interests`)),
  `profile_completed` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `student_id`, `first_name`, `last_name`, `email`, `password`, `high_school_gpa`, `intended_major`, `career_interests`, `learning_style`, `study_hours_preference`, `extracurricular_interests`, `profile_completed`, `created_at`, `updated_at`) VALUES
(1, 'ADMIN001', 'System', 'Administrator', 'admin@university.edu', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 4.00, 'Administration', NULL, NULL, NULL, NULL, 1, '2025-11-24 07:05:28', '2025-11-24 07:05:28'),
(2, '1', 'luther', 'concepcion', 'student@gmail.com', '$2y$10$jrLWcS4bpeW6XGwLOf95WORCMFlmAwInZ0KdVziuGtbz43ucpToAa', 4.00, 'Mathematics', '[\"Medical\",\"Healthcare\"]', 'Reading', 20, '[\"biology\"]', 1, '2025-11-24 07:06:50', '2025-11-27 09:00:44');

-- --------------------------------------------------------

--
-- Stand-in structure for view `student_enrollment_summary`
-- (See below for the actual view)
--
CREATE TABLE `student_enrollment_summary` (
`student_id` int(11)
,`student_number` varchar(50)
,`student_name` varchar(201)
,`intended_major` varchar(100)
,`total_enrollments` bigint(21)
,`current_gpa` decimal(6,5)
);

-- --------------------------------------------------------

--
-- Table structure for table `system_logs`
--

CREATE TABLE `system_logs` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `action_type` varchar(100) DEFAULT NULL,
  `action_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`action_details`)),
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure for view `course_popularity`
--
DROP TABLE IF EXISTS `course_popularity`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `course_popularity`  AS SELECT `c`.`course_code` AS `course_code`, `c`.`course_name` AS `course_name`, `c`.`department` AS `department`, count(`e`.`id`) AS `enrollment_count`, avg(`f`.`rating`) AS `avg_rating`, `c`.`max_enrollment` AS `max_enrollment`, count(`e`.`id`) / `c`.`max_enrollment` * 100 AS `fill_rate` FROM (((`courses` `c` left join `enrollments` `e` on(`c`.`id` = `e`.`course_id`)) left join `recommendations` `r` on(`c`.`id` = `r`.`course_id`)) left join `feedback` `f` on(`r`.`id` = `f`.`recommendation_id`)) GROUP BY `c`.`id` ORDER BY count(`e`.`id`) DESC ;

-- --------------------------------------------------------

--
-- Structure for view `recommendation_accuracy`
--
DROP TABLE IF EXISTS `recommendation_accuracy`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `recommendation_accuracy`  AS SELECT `r`.`algorithm_version` AS `algorithm_version`, count(0) AS `total_recommendations`, sum(case when `r`.`is_accepted` = 1 then 1 else 0 end) AS `accepted_count`, avg(`r`.`confidence_score`) AS `avg_confidence`, sum(case when `r`.`is_accepted` = 1 then 1 else 0 end) / count(0) * 100 AS `acceptance_rate` FROM `recommendations` AS `r` GROUP BY `r`.`algorithm_version` ;

-- --------------------------------------------------------

--
-- Structure for view `student_enrollment_summary`
--
DROP TABLE IF EXISTS `student_enrollment_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `student_enrollment_summary`  AS SELECT `s`.`id` AS `student_id`, `s`.`student_id` AS `student_number`, concat(`s`.`first_name`,' ',`s`.`last_name`) AS `student_name`, `s`.`intended_major` AS `intended_major`, count(`e`.`id`) AS `total_enrollments`, avg(case when `e`.`final_grade` is not null then case `e`.`final_grade` when 'A' then 4.0 when 'B' then 3.0 when 'C' then 2.0 when 'D' then 1.0 else 0.0 end end) AS `current_gpa` FROM (`students` `s` left join `enrollments` `e` on(`s`.`id` = `e`.`student_id`)) GROUP BY `s`.`id` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analytics`
--
ALTER TABLE `analytics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_metric` (`metric_name`),
  ADD KEY `idx_category` (`metric_category`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `course_code` (`course_code`),
  ADD KEY `idx_course_code` (`course_code`),
  ADD KEY `idx_department` (`department`);

--
-- Indexes for table `course_preferences`
--
ALTER TABLE `course_preferences`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_preference` (`student_id`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_enrollment` (`student_id`,`course_id`,`semester`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `recommendation_id` (`recommendation_id`),
  ADD KEY `idx_rating` (`rating`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `idx_student` (`student_id`),
  ADD KEY `idx_confidence` (`confidence_score`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id` (`student_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_student_id` (`student_id`);

--
-- Indexes for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `idx_action` (`action_type`),
  ADD KEY `idx_date` (`created_at`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analytics`
--
ALTER TABLE `analytics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `course_preferences`
--
ALTER TABLE `course_preferences`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course_preferences`
--
ALTER TABLE `course_preferences`
  ADD CONSTRAINT `course_preferences_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `course_preferences_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`recommendation_id`) REFERENCES `recommendations` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD CONSTRAINT `recommendations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `recommendations_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `system_logs`
--
ALTER TABLE `system_logs`
  ADD CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
