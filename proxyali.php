<?php
// Simple PHP Proxy Script with Authentication and Security

// Define author information
$author = 'Ali Essam';

// Access control: Basic Authentication (for security)
$allowed_username = 'admin';
$allowed_password = 'password';
if (!isset($_SERVER['PHP_AUTH_USER']) || $_SERVER['PHP_AUTH_USER'] !== $allowed_username || $_SERVER['PHP_AUTH_PW'] !== $allowed_password) {
    header('WWW-Authenticate: Basic realm="Restricted Area"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Unauthorized access. Please provide valid credentials.';
    exit;
}

// Handle the request
if(isset($_GET['url'])) {
    $url = $_GET['url']; // Get the URL to proxy

    // Validate the URL (basic validation)
    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        die('<div class="error">Invalid URL. Please provide a valid URL.</div>');
    }

    // Whitelist: Only allow URLs from trusted sources
    $whitelist = ['example.com', 'anotherdomain.com'];
    $parsed_url = parse_url($url);
    if (!in_array($parsed_url['host'], $whitelist)) {
        die('<div class="error">Access to this URL is not allowed. Please try another one.</div>');
    }

    // Initialize cURL to fetch the content from the target URL
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);  // Return the response as a string
    curl_setopt($ch, CURLOPT_HEADER, 0);          // Exclude headers from the response
    $response = curl_exec($ch);
    
    // Error handling
    if(curl_errno($ch)) {
        echo '<div class="error">Curl error: ' . curl_error($ch) . '</div>';
    }

    // Close cURL
    curl_close($ch);

    // Output the response
    echo '<div class="response">' . htmlspecialchars($response) . '</div>';
} else {
    echo '<div class="info">No URL provided. Please provide a URL in the query string (e.g., ?url=http://example.com).</div>';
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Proxy by Ali Essam</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f7f7;
            color: #333;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
        }
        header h1 {
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .input-box {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            font-size: 16px;
            border-radius: 4px;
        }
        .button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 4px;
        }
        .button:hover {
            background-color: #218838;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            margin: 15px 0;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
        }
        .info {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            margin: 15px 0;
            border: 1px solid #bee5eb;
            border-radius: 4px;
        }
        .response {
            background-color: #e9ecef;
            padding: 15px;
            margin-top: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            white-space: pre-wrap;
        }
        footer {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            margin-top: 20px;
        }
        footer a {
            color: #ff9f1c;
            text-decoration: none;
        }
        footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
                width: 90%;
            }
            .input-box, .button {
                width: 100%;
            }
        }
    </style>
</head>
<body>

<header>
    <h1>PHP Proxy by Ali Essam</h1>
    <p>Access external websites securely via this proxy.</p>
</header>

<div class="container">
    <form action="" method="GET">
        <label for="url">Enter URL to Proxy:</label>
        <input type="text" id="url" name="url" class="input-box" placeholder="e.g., http://example.com" value="<?php echo isset($_GET['url']) ? $_GET['url'] : ''; ?>" required>
        <button type="submit" class="button">Proxy URL</button>
    </form>

    <div class="footer-info">
        <p>Author: <strong>Ali Essam</strong></p>
        <p>For security reasons, only whitelisted URLs are allowed.</p>
    </div>
</div>

<footer>
    <p>Created by <a href="https://www.example.com" target="_blank">Ali Essam</a> | All rights reserved</p>
</footer>

</body>
</html>
