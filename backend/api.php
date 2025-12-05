<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

require_once 'config.php';

class CourseRecommendationAPI {
    private $conn;

    public function __construct() {
        $db = new Database();
        $this->conn = $db->getConnection();
    }

    private function jsonResponse($data) {
        echo json_encode($data);
        exit;
    }

    // ---------- USER REGISTRATION ----------
    public function register($data) {
        if (!isset($data['email'], $data['password'])) {
            return ['success' => false, 'message' => 'Missing fields'];
        }

        $check = $this->conn->prepare("SELECT id FROM students WHERE email=?");
        $check->execute([$data['email']]);
        if ($check->fetch()) {
            return ['success' => false, 'message' => 'Email already registered'];
        }

        $sql = "INSERT INTO students 
            (first_name, last_name, email, password, student_id, high_school_gpa, intended_major)
            VALUES (?, ?, ?, ?, ?, ?, ?)";

        $stmt = $this->conn->prepare($sql);
        $hashed = password_hash($data['password'], PASSWORD_DEFAULT);

        try {
            $stmt->execute([
                $data['first_name'] ?? '',
                $data['last_name'] ?? '',
                $data['email'],
                $hashed,
                $data['student_id'] ?? '',
                $data['gpa'] ?? 0,
                $data['major'] ?? 'Undecided'
            ]);
            return ['success' => true, 'message' => 'Registration successful'];
        } catch (PDOException $e) {
            return ['success' => false, 'message' => $e->getMessage()];
        }
    }

    // ---------- LOGIN ----------
    public function login($data) {
        $sql = "SELECT * FROM students WHERE email=?";
        $stmt = $this->conn->prepare($sql);
        $stmt->execute([$data['email'] ?? '']);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && password_verify($data['password'], $user['password'])) {
            unset($user['password']);
            return ['success' => true, 'student' => $user];
        }
        return ['success' => false, 'message' => 'Invalid credentials'];
    }

    // ---------- PROFILE ----------
    public function getProfile($studentId) {
        $stmt = $this->conn->prepare("SELECT * FROM students WHERE id=?");
        $stmt->execute([$studentId]);
        $p = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($p) {
            unset($p['password']);
            $p['career_interests'] = !empty($p['career_interests']) ? json_decode($p['career_interests'], true) : [];
            $p['extracurricular_interests'] = !empty($p['extracurricular_interests']) ? json_decode($p['extracurricular_interests'], true) : [];
        }
        return $p;
    }

    public function saveProfile($data) {
        $sql = "UPDATE students SET
            career_interests=?, learning_style=?, study_hours_preference=?,
            extracurricular_interests=?, profile_completed=1 WHERE id=?";
        $stmt = $this->conn->prepare($sql);

        try {
            $stmt->execute([
                json_encode($data['career_interests']),
                $data['learning_style'],
                $data['study_hours'],
                json_encode($data['extracurricular']),
                $data['student_id']
            ]);
            return ['success' => true, 'message' => 'Profile updated successfully'];
        } catch (PDOException $e) {
            return ['success' => false, 'message' => $e->getMessage()];
        }
    }

    // ---------- COURSES ----------
    public function getCourses() {
        $stmt = $this->conn->query("SELECT * FROM courses ORDER BY department, course_code");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // ---------- RECOMMENDATIONS ----------
    public function getRecommendations($studentId) {
        $profile = $this->getProfile($studentId);
        if (!$profile) return ['success' => false, 'message' => 'Student not found'];

        $input = json_encode([
            'student_id' => $studentId,
            'gpa' => $profile['high_school_gpa'],
            'major' => $profile['intended_major'],
            'career_interests' => $profile['career_interests'],
            'learning_style' => $profile['learning_style'],
            'study_hours' => $profile['study_hours_preference']
        ]);

        $tmp = tempnam(sys_get_temp_dir(), 'student_');
        file_put_contents($tmp, $input);

        // Try multiple python executables (Windows commonly has 'python' or 'py')
        $pythonBins = ['python3', 'python', 'py'];
        $rawOutput = null;
        $lastCmd = '';
        $validJsonFound = false;
        foreach ($pythonBins as $bin) {
            $script = escapeshellarg(__DIR__ . DIRECTORY_SEPARATOR . 'recommendation_algorithm.py');
            $arg = escapeshellarg($tmp);
            // Redirect stderr to stdout so we capture errors as well
            $cmd = "$bin $script $arg 2>&1";
            $lastCmd = $cmd;
            // Suppress warnings if shell_exec is disabled; we will log failures below
            $out = @shell_exec($cmd);
            if ($out === null || trim($out) === '') continue;
            // If output decodes as valid JSON, accept it
            $decoded = json_decode($out, true);
            if ($decoded !== null && json_last_error() === JSON_ERROR_NONE) {
                $rawOutput = $out;
                $validJsonFound = true;
                break;
            }
            // Otherwise record the output and continue trying other binaries (handles MS Store message)
            // keep last non-empty output just in case
            $rawOutput = $out;
        }
        // remove temp file
        @unlink($tmp);

        if (!$rawOutput) {
            $logMsg = date('Y-m-d H:i:s') . " No output when running recommendation engine. Command tried: $lastCmd\n";
            file_put_contents(__DIR__ . '/logs/error.log', $logMsg, FILE_APPEND);
            return ['success' => false, 'message' => 'No recommendations generated (engine failed). Ensure Python is installed and available as "python" or "py" in PATH.'];
        }

        // DEBUG: record raw output from python (base64 to preserve binary/whitespace)
        @file_put_contents(__DIR__ . '/logs/recommendation_debug.log', date('Y-m-d H:i:s') . " BASE64_OUTPUT: " . base64_encode($rawOutput) . "\n", FILE_APPEND);

        if (!$validJsonFound) {
            // We received output but it wasn't valid JSON
            file_put_contents(__DIR__ . '/logs/error.log', date('Y-m-d H:i:s') . " Invalid JSON: $rawOutput\n", FILE_APPEND);
            return ['success' => false, 'message' => 'Error in algorithm'];
        }

        $recs = json_decode($rawOutput, true);

        return ['success' => true, 'recommendations' => $recs];
    }

    // ---------- ENROLLMENT (simple logger) ----------
    public function enroll($data) {
        $student_id = $data['student_id'] ?? 0;
        $course_id = $data['course_id'] ?? 0;
        $semester = $data['semester'] ?? '';

        // Try to persist to DB when connection is available
        if ($this->conn) {
            try {
                $stmt = $this->conn->prepare("INSERT INTO enrollments (student_id, course_id, semester) VALUES (?, ?, ?)");
                $stmt->execute([$student_id, $course_id, $semester]);
                return ['success' => true, 'message' => 'Enrollment saved to database'];
            } catch (PDOException $e) {
                // Fall through to file logging
                file_put_contents(__DIR__ . '/logs/error.log', date('Y-m-d H:i:s') . " DB enroll failed: " . $e->getMessage() . "\n", FILE_APPEND);
            }
        }

        // Fallback: log to file
        $logLine = date('Y-m-d H:i:s') . " | ENROLL | student_id={$student_id} | course_id={$course_id} | semester={$semester}\n";
        $logFile = __DIR__ . '/logs/enrollments.log';
        file_put_contents($logFile, $logLine, FILE_APPEND);

        return ['success' => true, 'message' => 'Enrollment recorded (logged)'];
    }

    // ---------- FEEDBACK (simple logger) ----------
    public function submitFeedback($data) {
        $student_id = $data['student_id'] ?? 0;
        $course_id = $data['course_id'] ?? 0;
        $rating = $data['rating'] ?? null;
        $comments = $data['comments'] ?? '';

        $payload = [
            'timestamp' => date('c'),
            'student_id' => $student_id,
            'course_id' => $course_id,
            'rating' => $rating,
            'comments' => $comments
        ];

        // Try to persist to DB when connection available. We'll try to link feedback to recommendations if possible.
        if ($this->conn) {
            try {
                // If there's a matching recommendation for this student-course, link it
                $recStmt = $this->conn->prepare("SELECT id FROM recommendations WHERE student_id = ? AND course_id = ? ORDER BY created_at DESC LIMIT 1");
                $recStmt->execute([$student_id, $course_id]);
                $rec = $recStmt->fetch(PDO::FETCH_ASSOC);
                $recommendation_id = $rec ? $rec['id'] : null;

                $stmt = $this->conn->prepare("INSERT INTO feedback (student_id, recommendation_id, rating, comments) VALUES (?, ?, ?, ?)");
                $stmt->execute([$student_id, $recommendation_id, $rating, $comments]);
                return ['success' => true, 'message' => 'Feedback saved to database'];
            } catch (PDOException $e) {
                file_put_contents(__DIR__ . '/logs/error.log', date('Y-m-d H:i:s') . " DB feedback failed: " . $e->getMessage() . "\n", FILE_APPEND);
            }
        }

        // Fallback to file log
        $logFile = __DIR__ . '/logs/feedback.log';
        file_put_contents($logFile, json_encode($payload, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND);

        return ['success' => true, 'message' => 'Feedback submitted (logged)'];
    }
}

// Handle API routing only when executed via web server (not CLI). This avoids
// attempting a DB connection when the file is included by CLI test scripts.
// ... existing code above ...

// Handle API routing
if (php_sapi_name() !== 'cli') {
    try {
        $api = new CourseRecommendationAPI();
        
        // 1. Get the JSON Body (if any)
        $inputJSON = file_get_contents('php://input');
        $data = json_decode($inputJSON, true) ?? [];

        // 2. SMARTER ACTION DETECTION
        // Check URL first (?action=...), then Check JSON body ({action:...}), then default to empty
        $action = $_GET['action'] ?? $data['action'] ?? '';

        // Debugging: If action is missing, tell us what we received
        if (empty($action)) {
            echo json_encode([
                'error' => 'Invalid action', 
                'debug_received_get' => $_GET,
                'debug_received_json' => $data
            ]);
            exit;
        }

        switch ($action) {
            case 'register': 
                echo json_encode($api->register($data)); 
                break;
            case 'login': 
                echo json_encode($api->login($data)); 
                break;
            case 'profile':
                if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                    echo json_encode($api->saveProfile($data));
                } else {
                    $lookupId = $_GET['id'] ?? $_GET['student_id'] ?? 0;
                    $profile = $api->getProfile($lookupId);                    
                    if ($profile === false) {
                         echo json_encode(['success' => false, 'message' => 'User not found']);
                    } else {
                         echo json_encode($profile);
                    }
                }
                break;
            case 'courses': 
                echo json_encode($api->getCourses()); 
                break;
            case 'recommendations': 
                $recId = $_GET['id'] ?? $_GET['student_id'] ?? 0;
                echo json_encode($api->getRecommendations($recId)); 
                break;
            case 'enroll':
                echo json_encode($api->enroll($data));
                break;
            case 'feedback':
                echo json_encode($api->submitFeedback($data));
                break;
            default: 
                echo json_encode(['error' => 'Unknown action: ' . $action]);
        }
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => $e->getMessage()]);
    }
}
?>
