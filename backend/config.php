<?php
// config.php - Database Configuration

class Database {
    private $conn;
    
    public function __construct() {
        // Read credentials from Railway Environment Variables
        // These match the variables shown in your screenshot (Image 2)
        $host = getenv('MYSQLHOST');
        $port = getenv('MYSQLPORT');
        $user = getenv('MYSQLUSER');
        $pass = getenv('MYSQLPASSWORD');
        $dbname = getenv('MYSQLDATABASE');

        // Fallback for local testing (optional, remove if not needed)
        if (!$host) {
             // You can keep your hardcoded values here ONLY for local testing
             $host = 'localhost';
             $port = '3306';
             $user = 'root';
             $pass = ''; 
             $dbname = 'course_recommendation_db';
        }

        try {
            // Updated Connection String: Includes PORT
            $dsn = "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4";
            
            $this->conn = new PDO($dsn, $user, $pass);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
        } catch(PDOException $e) {
            // Log the specific error to your internal logs
            error_log("Database Connection Error: " . $e->getMessage());
            
            // Throw generic error to frontend
            throw new Exception("Database connection failed.");
        }
    }
    
    public function getConnection() {
        return $this->conn;
    }
}
?>
