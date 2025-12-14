<?php

class Database {
    private $conn;
    
    public function __construct() {
        $host = getenv('MYSQLHOST');
        $port = getenv('MYSQLPORT');
        $user = getenv('MYSQLUSER');
        $pass = getenv('MYSQLPASSWORD');
        $dbname = getenv('MYSQLDATABASE');

        if (!$host) {
             $host = 'localhost';
             $port = '3306';
             $user = 'root';
             $pass = ''; 
             $dbname = 'course_recommendation_db';
        }

        try {
            $dsn = "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4";
            
            $this->conn = new PDO($dsn, $user, $pass);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
        } catch(PDOException $e) {
            error_log("Database Connection Error: " . $e->getMessage());
            
            throw new Exception("Database connection failed.");
        }
    }
    
    public function getConnection() {
        return $this->conn;
    }
}
?>
