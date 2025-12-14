<?php
require_once __DIR__ . '/api.php';

$rc = new ReflectionClass('CourseRecommendationAPI');
$api = $rc->newInstanceWithoutConstructor();

$res1 = $api->enroll(['student_id' => 1, 'course_id' => 2, 'semester' => 'Fall 2025']);
$res2 = $api->submitFeedback(['student_id' => 1, 'course_id' => 2, 'rating' => 5, 'comments' => 'Great suggestion']);

header('Content-Type: text/plain');
print_r($res1);
print_r($res2);
echo "\nLogs written to backend/logs/enrollments.log and backend/logs/feedback.log if writable.\n";
?>
