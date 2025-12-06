// ---------- RECOMMENDATIONS ----------
public function getRecommendations($studentId) {
    $profile = $this->getProfile($studentId);
    if (!$profile) return ['success' => false, 'message' => 'Student not found'];

    // Prepare input data with proper defaults
    $input = [
        'student_id' => $studentId,
        'gpa' => floatval($profile['high_school_gpa'] ?? 3.0),
        'major' => $profile['intended_major'] ?? 'Undecided',
        'career_interests' => is_array($profile['career_interests']) ? $profile['career_interests'] : [],
        'learning_style' => $profile['learning_style'] ?? 'Visual',
        'study_hours' => floatval($profile['study_hours_preference'] ?? 10)
    ];

    $inputJson = json_encode($input);
    
    // Create temp file with proper error handling
    $tmpDir = sys_get_temp_dir();
    if (!is_writable($tmpDir)) {
        return ['success' => false, 'message' => 'Cannot write to temp directory'];
    }
    
    $tmp = tempnam($tmpDir, 'student_');
    if ($tmp === false) {
        return ['success' => false, 'message' => 'Failed to create temp file'];
    }
    
    file_put_contents($tmp, $inputJson);

    // Get the Python script path
    $scriptPath = __DIR__ . DIRECTORY_SEPARATOR . 'recommendation_algorithm.py';
    
    if (!file_exists($scriptPath)) {
        @unlink($tmp);
        return ['success' => false, 'message' => 'Recommendation script not found'];
    }

    // Try Python executables in order of preference
    $pythonBins = ['python3', 'python', 'py'];
    $rawOutput = null;
    $errorOutput = null;
    
    foreach ($pythonBins as $bin) {
        // Use absolute paths and proper escaping
        $script = escapeshellarg($scriptPath);
        $arg = escapeshellarg($tmp);
        
        // Execute with both stdout and stderr capture
        $descriptors = [
            0 => ["pipe", "r"],  // stdin
            1 => ["pipe", "w"],  // stdout
            2 => ["pipe", "w"]   // stderr
        ];
        
        $process = @proc_open("$bin $script $arg", $descriptors, $pipes);
        
        if (is_resource($process)) {
            fclose($pipes[0]); // Close stdin
            
            $stdout = stream_get_contents($pipes[1]);
            $stderr = stream_get_contents($pipes[2]);
            
            fclose($pipes[1]);
            fclose($pipes[2]);
            
            $returnCode = proc_close($process);
            
            // Check if we got valid output
            if ($returnCode === 0 && !empty($stdout)) {
                $decoded = json_decode($stdout, true);
                if ($decoded !== null && json_last_error() === JSON_ERROR_NONE) {
                    $rawOutput = $stdout;
                    break;
                }
            }
            
            // Store error for debugging
            if (!empty($stderr)) {
                $errorOutput = $stderr;
            }
        }
    }
    
    // Cleanup temp file
    @unlink($tmp);

    // Check if we got valid output
    if (!$rawOutput) {
        // Log the error
        $logMsg = date('Y-m-d H:i:s') . " Recommendation engine failed\n";
        $logMsg .= "Input: " . $inputJson . "\n";
        if ($errorOutput) {
            $logMsg .= "Error: " . $errorOutput . "\n";
        }
        @file_put_contents(__DIR__ . '/logs/error.log', $logMsg, FILE_APPEND);
        
        return [
            'success' => false, 
            'message' => 'Unable to generate recommendations. Please ensure Python is installed.',
            'debug' => $errorOutput
        ];
    }

    // Parse recommendations
    $recs = json_decode($rawOutput, true);
    
    if (!is_array($recs)) {
        return ['success' => false, 'message' => 'Invalid recommendation format'];
    }

    return ['success' => true, 'recommendations' => $recs];
}// ---------- RECOMMENDATIONS ----------
public function getRecommendations($studentId) {
    $profile = $this->getProfile($studentId);
    if (!$profile) return ['success' => false, 'message' => 'Student not found'];

    // Prepare input data with proper defaults
    $input = [
        'student_id' => $studentId,
        'gpa' => floatval($profile['high_school_gpa'] ?? 3.0),
        'major' => $profile['intended_major'] ?? 'Undecided',
        'career_interests' => is_array($profile['career_interests']) ? $profile['career_interests'] : [],
        'learning_style' => $profile['learning_style'] ?? 'Visual',
        'study_hours' => floatval($profile['study_hours_preference'] ?? 10)
    ];

    $inputJson = json_encode($input);
    
    // Create temp file with proper error handling
    $tmpDir = sys_get_temp_dir();
    if (!is_writable($tmpDir)) {
        return ['success' => false, 'message' => 'Cannot write to temp directory'];
    }
    
    $tmp = tempnam($tmpDir, 'student_');
    if ($tmp === false) {
        return ['success' => false, 'message' => 'Failed to create temp file'];
    }
    
    file_put_contents($tmp, $inputJson);

    // Get the Python script path
    $scriptPath = __DIR__ . DIRECTORY_SEPARATOR . 'recommendation_algorithm.py';
    
    if (!file_exists($scriptPath)) {
        @unlink($tmp);
        return ['success' => false, 'message' => 'Recommendation script not found'];
    }

    // Try Python executables in order of preference
    $pythonBins = ['python3', 'python', 'py'];
    $rawOutput = null;
    $errorOutput = null;
    
    foreach ($pythonBins as $bin) {
        // Use absolute paths and proper escaping
        $script = escapeshellarg($scriptPath);
        $arg = escapeshellarg($tmp);
        
        // Execute with both stdout and stderr capture
        $descriptors = [
            0 => ["pipe", "r"],  // stdin
            1 => ["pipe", "w"],  // stdout
            2 => ["pipe", "w"]   // stderr
        ];
        
        $process = @proc_open("$bin $script $arg", $descriptors, $pipes);
        
        if (is_resource($process)) {
            fclose($pipes[0]); // Close stdin
            
            $stdout = stream_get_contents($pipes[1]);
            $stderr = stream_get_contents($pipes[2]);
            
            fclose($pipes[1]);
            fclose($pipes[2]);
            
            $returnCode = proc_close($process);
            
            // Check if we got valid output
            if ($returnCode === 0 && !empty($stdout)) {
                $decoded = json_decode($stdout, true);
                if ($decoded !== null && json_last_error() === JSON_ERROR_NONE) {
                    $rawOutput = $stdout;
                    break;
                }
            }
            
            // Store error for debugging
            if (!empty($stderr)) {
                $errorOutput = $stderr;
            }
        }
    }
    
    // Cleanup temp file
    @unlink($tmp);

    // Check if we got valid output
    if (!$rawOutput) {
        // Log the error
        $logMsg = date('Y-m-d H:i:s') . " Recommendation engine failed\n";
        $logMsg .= "Input: " . $inputJson . "\n";
        if ($errorOutput) {
            $logMsg .= "Error: " . $errorOutput . "\n";
        }
        @file_put_contents(__DIR__ . '/logs/error.log', $logMsg, FILE_APPEND);
        
        return [
            'success' => false, 
            'message' => 'Unable to generate recommendations. Please ensure Python is installed.',
            'debug' => $errorOutput
        ];
    }

    // Parse recommendations
    $recs = json_decode($rawOutput, true);
    
    if (!is_array($recs)) {
        return ['success' => false, 'message' => 'Invalid recommendation format'];
    }

    return ['success' => true, 'recommendations' => $recs];
}
