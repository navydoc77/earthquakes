<?php 
    $username = "root"; 
    $password = "root"; 
    $database = "natural_disastersdb"; 
    $mysqli = new mysqli("localhost", $username, $password, $database); 
    $query = "SELECT * FROM warnings";
    
    
    echo '<table border="0" cellspacing="2" cellpadding="2"> 
          <tr> 
              <td> <font face="Arial">events</font> </td> 
              <td> <font face="Arial">urgency</font> </td> 
              <td> <font face="Arial">warning source</font> </td> 
              <td> <font face="Arial">headlines</font> </td> 
          </tr>';
    
    if ($result = $mysqli->query($query)) {
        while ($row = $result->fetch_assoc()) {
            $events = $row["col1"];
            $urgency = $row["col2"];
            $warning_source = $row["col3"];
            $headlines = $row["col4"];
    
            echo '<tr> 
                      <td>'.$events.'</td> 
                      <td>'.$urgency.'</td> 
                      <td>'.$warning_source.'</td> 
                      <td>'.$headlines.'</td> 
                  </tr>';
        }
        $result->free();
    } 
?>