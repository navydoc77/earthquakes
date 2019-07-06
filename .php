<?php
$servername = "Final";
$username = "root";
$password = "root";
$dbname = "natural_disasterdb";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "SELECT events, warning_source, headlines FROM Warnings";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    // output data of each row
    while($row = mysqli_fetch_assoc($result)) {
        echo "events: " . $row["events"]. " - warning_source: " . $row["warning_source"]. "headlines" . $row["headlines"]. "<br>";
    }
} else {
    echo "0 results";
}

mysqli_close($conn);
?>