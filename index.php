<?php

// Status endpoint
$statusEndpoint = "";
// Create endpoint
$createEndpoint = "";

function getStatus() {
    global $statusEndpoint;
    
    $response = file_get_contents($statusEndpoint);
    $data = json_decode($response, true);
    
    if ($data && isset($data['status'])) {
        return $data['status'];
    }
    
    return null;
}

function triggerCreate() {
    global $createEndpoint;
    echo "Create endpoint triggered!";
}

$status = getStatus();

if ($status === true) {
    echo "Status is true. Create endpoint will not be triggered.";
} elseif ($status === false) {
    triggerCreate();
} else {
    echo "Invalid or missing status from the status endpoint.";
}

?>

