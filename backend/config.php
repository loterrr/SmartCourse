<?php
class Database {
    public function getConnection() {
        $host = getenv('MYSQLHOST') ?: 'localhost';
        $user = getenv('MYSQLUSER') ?: 'root';
        $pass = getenv('MYSQLPASSWORD') ?: '';
        $name = getenv('MYSQLDATABASE') ?: 'smartcourse_db';
        $port = getenv('MYSQLPORT') ?: 3306;

        try {
            $conn = new PDO("mysql:host=$host;port=$port;dbname=$name", $user, $pass);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            return $conn;
        } catch(PDOException $e) {
            // Return null or handle error silently so API can report it
            return null;
        }
    }
}
?>
