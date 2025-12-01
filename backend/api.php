<?php
// backend/api.php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle Pre-flight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

require_once 'config.php';

// --- DEBUG HELPER ---
function get_request_action() {
    // 1. Check URL parameters (GET)
    if (isset($_GET['action']) && !empty($_GET['action'])) {
        return $_GET['action'];
    }
    // 2. Check Form Data (POST)
    if (isset($_POST['action']) && !empty($_POST['action'])) {
        return $_POST['action'];
    }
    // 3. Check JSON Body (fetch)
    $json = json_decode(file_get_contents('php://input'), true);
    if (isset($json['action']) && !empty($json['action'])) {
        return $json['action'];
    }
    return null;
}

// ... Keep your Class CourseRecommendationAPI definition here ...
// (Paste your class code here, or leave it if you just update the bottom part)
class CourseRecommendationAPI {
    // ... [PASTE YOUR EXISTING CLASS METHODS HERE] ...
    // Note: Ensure your Database connection uses getenv() variables!
    private $conn;

    public function __construct() {
        // Simple DB Connection for debugging
        $host = getenv('MYSQLHOST') ?: 'localhost';
        $user = getenv('MYSQLUSER') ?: 'root';
        $pass = getenv('MYSQLPASSWORD') ?: '';
        $name = getenv('MYSQLDATABASE') ?: 'railway';
        $port = getenv('MYSQLPORT') ?: 3306;

        try {
            $this->conn = new PDO("mysql:host=$host;port=$port;dbname=$name", $user, $pass);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            // If DB fails, we will know immediately
            echo json_encode(['success' => false, 'message' => 'DB Connection Failed: ' . $e->getMessage()]);
            exit;
        }
    }
    // ... [REST OF YOUR FUNCTIONS: register, login, etc.] ...
    public function getProfile($studentId) {
        // Basic profile fetch
        $stmt = $this->conn->prepare("SELECT * FROM students WHERE id=?");
        $stmt->execute([$studentId]);
        return $stmt->fetch(PDO::FETCH_ASSOC) ?: ['error' => 'Student not found'];
    }
}

// --- MAIN EXECUTION ---
if (php_sapi_name() !== 'cli') {
    try {
        $api = new CourseRecommendationAPI();
        $action = get_request_action();
        
        // GET DATA (Support both Query Params and JSON Body)
        $jsonInput = json_decode(file_get_contents('php://input'), true) ?? [];
        $data = array_merge($_GET, $_POST, $jsonInput);

        if (!$action) {
            // THIS IS THE DIAGNOSTIC PART
            echo json_encode([
                'error' => 'Invalid action',
                'debug_message' => 'Server received request but could not find action parameter.',
                'received_get' => $_GET,
                'received_post' => $_POST,
                'received_json' => $jsonInput
            ]);
            exit;
        }

        // Routing
        switch ($action) {
            case 'register': echo json_encode($api->register($data)); break;
            case 'login': echo json_encode($api->login($data)); break;
            case 'profile': echo json_encode($api->getProfile($data['student_id'] ?? 1)); break;
            // Add other cases here...
            default: echo json_encode(['error' => 'Unknown action: ' . $action]);
        }

    } catch (Exception $e) {
        echo json_encode(['success' => false, 'message' => $e->getMessage()]);
    }
}
?>
