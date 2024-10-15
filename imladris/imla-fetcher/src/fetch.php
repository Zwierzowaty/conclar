<?php
require '../vendor/autoload.php';

use Google\Client;
use Google\Service\Drive;


$superSecretToken = '05e52d3e-77fa-4125-b0d3-9c55a5f169b4';

if (! array_key_exists('token', $_GET)) {
    die('No token provided');
}

if ($_GET['token'] != $superSecretToken) {
    die('Invalid token');
}

$participantSavePath = '/home/yavi/domains/program.imladris.pl/public_html/participants.json';
$scheduleSavePath = '/home/yavi/domains/program.imladris.pl/public_html/schedule.json';

// Set up the client
$client = new Client();
$client->setAuthConfig('/home/yavi/domains/program.imladris.pl/conclar/imladris/imla-fetcher/imla-fetcher-secret.json');
$client->addScope(Drive::DRIVE_READONLY);

// Create the Drive service
$driveService = new Drive($client);

// Function to get a file by ID
function getFileById($driveService, $fileId) {
    try {
        $file = $driveService->files->get($fileId, array( "supportsAllDrives" => true));
        return $file;
    } catch (Exception $e) {
        echo 'An error occurred: ' . $e->getMessage();
        return null;
    }
}

function downloadFileContent($driveService, $fileId) {
    try {
        $response = $driveService->files->get($fileId, array('alt' => 'media',  "supportsAllDrives" => true));
        return $response->getBody()->getContents();
    } catch (Exception $e) {
        echo 'An error occurred: ' . $e->getMessage();
        return null;
    }
}

$participantsFileId = '1OPulR4VCdEXQJy6OYbYDW0kfN-8kQh3d';
$scheduleFileId = '1NA5_q7SaIBowTqzu297EP_gkB9CoYVa4';

$participantFsile = getFileById($driveService, $participantsFileId);
$scheduleFile = getFileById($driveService, $scheduleFileId);

file_put_contents($participantSavePath, downloadFileContent($driveService, $participantsFileId));
file_put_contents($scheduleSavePath, downloadFileContent($driveService, $scheduleFileId));

echo 'Files downloaded';

// This magic lists all files including shared drives
// echo "<pre>";
// print_r($driveService->files->listFiles(array('supportsAllDrives' => true,
// 'includeItemsFromAllDrives' => true)));
// echo "</pre>";
