<?php

$status_url = getenv('STATUS_URL');
$create_url = getenv('CREATE_URL');

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $status_url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
$status_data = curl_exec($curl);

$status_data_array = json_decode($status_data, true);

if ($status_data_array && isset($status_data_array['statusCode']) && $status_data_array['statusCode'] == 500) {
    $create_curl = curl_init();
    curl_setopt($create_curl, CURLOPT_URL, $create_url);
    curl_setopt($create_curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($create_curl, CURLOPT_HEADER, false);
    $create_response = curl_exec($create_curl);
    curl_close($create_curl);
#    echo $create_response;
    $create_response_array = json_decode($create_response, true);

    $ip_address_from_create_response = isset($create_response_array['body']) ? $create_response_array['body'] : null;

    if ($ip_address_from_create_response !== null) {
        echo $ip_address_from_create_response;
    } else {
        echo "Not Found.";
    }
}

curl_close($curl);

?>
