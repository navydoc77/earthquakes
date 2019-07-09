<?php
include_once('connection.php');
$query="SELECT event, urgency, severity, warning_source, headlines FROM  natural_disasterdb";
$result=mysql_query($query);
?>

<!DOCTYPE html>
<!-- CSS Stylesheets with Relative Paths -->
<html lang="en-us">
<head>
  <meta charset="UTF-8">
  <title>Weather Warning Alerts </title>

  <!-- v1.5.1 Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
  integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
  crossorigin=""/>

  <!-- v1.2.1 Leaflet.timeline CSS -->
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/leaflet.timeline.css') }}">

  <!-- Bootcamp CSS -->
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
  <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/eq-map-style.css') }}">
</head>

<body>

  <header>
    <div class="navbar">
        <a class="active" href="{{ url_for('index') }}">Home</a>
        <div class="dropdown">
            <button class="dropbtn">Natural Disasters 
              <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-content">
              <a class="active" href="{{ url_for('sig_earthquake') }}">Historical Earthquakes</a>
              <a href="{{ url_for('tsunamis_landing') }}">Historical Tsunamis</a>
              <a href="{{ url_for('volcanoes_landing') }}">Volcanoes</a>  
            </div>
        </div> 
        <div class="dropdown">
            <button class="dropbtn">Extreme Weather 
              <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-content">
              <a href="{{ url_for('tornadoes_landing') }}">Tornadoes</a>
              <a href="{{ url_for('wind_landing') }}">Wind</a>
              <a href="{{ url_for('hail_landing') }}">Hail</a>
              <a href="{{ url_for('warnings_landing') }}">Weather Warnings</a>
            </div>
        </div>
        <div class="dropdown">
            <button class="dropbtn">Machine Learning 
              <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-content">
              <a class="drop-link" href="{{ url_for('ml_machine') }}">Machine Learning</a>
              <a class="drop-link" href="{{ url_for('sentiment_analysis') }}">Sentiment Analysis</a>
            </div>
        </div> 
    </div>
  </header>

  <!-- v5+ D3 -->
  <script src="https://d3js.org/d3.v5.min.js"></script>

  <!-- v1.5.1 Leaflet JavaScript -->
  <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
  integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
  crossorigin=""></script>

  <!-- v1.2.1 Leaflet.timeline & v0.3.2 diesal JavaScript. -->
  <!-- Place IntervalTree.js before the Timeline JavaScripts. Timeline is a Leaflet Plugin.       -->
  <!-- IntervalTree.js (https://github.com/skeate/diesal/tree/master/src/ds) is used by Timeline. -->
  <script type="text/javascript" src="{{ url_for('static', filename='plugins/leaflet/timeline/IntervalTree.js') }}"></script>

  <!-- API Key -->
  <script type="text/javascript" src="{{ url_for('static', filename='js/config.js') }}"></script>

  <!-- JavaScript -->
  <script type="text/javascript" src="{{ url_for('static', filename='js/warnings_app.js') }}"></script>
</body>

</html>