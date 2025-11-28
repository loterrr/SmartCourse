<?php
require_once __DIR__ . '/config.php';
error_reporting(E_ALL);
ini_set('display_errors', 1);
try {
    $db = new Database();
    $conn = $db->getConnection();
    echo "DB connected\n";
} catch (Exception $e) {
    echo "Error creating DB: " . $e->getMessage() . "\n";
}
?>