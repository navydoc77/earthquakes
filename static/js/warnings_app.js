function initializeTable() {
    d3.json("/api/warnings").then(function(data) {
    var table_data = data;
    console.log(table_data);
    var event = table_data.map(row => row["events"]);
    var lat = table_data.map(row => row["lat"]);
    var lng = table_data.map(row => row["lng"]);
    var severity = table_data.map(row => row["severity"]);
    var urgency = table_data.map(row => row["urgency"]);
    var source = table_data.map(row => row["warning_source"]);
    var description = table_data.map(row => row["warning_description"]);
    console.log(description);


    var values = [event, lat, lng, severity, urgency, source, description]
  
    var data = [{
      type: 'table',
      header: {
        values: [["<b>Event</b>"], ["<b>Latitude/b>"], ["<b>Longtidude</b>"], ["<b>Severity</b>"], ["<b>Urgency</b>"], ["<b>Source</b>"], ["<b>Description</b>"]],
        align: "center",
        line: {width: 1, color: 'black'},
        fill: {color: "grey"},
        font: {family: "Arial", size: 12, color: "white"}
      },
      cells: {
        values: values,
        align: "center",
        line: {color: "black", width: 1},
        font: {family: "Arial", size: 11, color: ["black"]}
      }
    }]
  
  Plotly.plot('table', data);
  
    });
  }

  initializeTable();