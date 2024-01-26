<?php

$status_url = "";
$create_url = "";

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $status_url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
$status_data = curl_exec($curl);

$status_data_array = json_decode($status_data, true);

if ($status_data_array && isset($status_data_array['statusCode']) && $status_data_array['statusCode'] == 500) {
    echo "run create_url";
    $create_curl = curl_init();
    curl_setopt($create_curl, CURLOPT_URL, $create_url);
    curl_setopt($create_curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($create_curl, CURLOPT_HEADER, false);
    $create_response = curl_exec($create_curl);
    curl_close($create_curl);
    echo $create_response;
}

curl_close($curl);

?>
