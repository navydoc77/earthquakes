// # ************************************
// # CREATE DROPDOWN MENU
// # ************************************
function getChecked() {
    var lat = document.getElementById("lat").checked;
    var lng = document.getElementById("lng").checked;
    var depth =  document.getElementById("depth").checked;

    if (document.getElementById("lat").checked) {
        var lat = lat;
        var lng = lng;
        var depth = depth;
    };
}

// function knnAnalysisPlot(data_source_url) {
function knnAnalysisPlot() {
  d3.json(data_source_url).then(function(data) {
    var data = [data];
    console.log(data);
    var x = [];
    var test_accuracy = [];
    var training_accuracy = [];

    var x = data.map(row => row.x);
    var test_accuracy = data.map(row => row.y1);
    var training_accuracy = data.map(row => row.y2);
    console.log(x);
    console.log(test_accuracy);
    console.log(training_accuracy);
    

    var trace2 = {
      type: "scatter",
      mode: "lines",
      name: "Test Accuracy",
      // x: data.map(row => row.x),
      // y: data.map(row => row.y1),
      x: [1,2,3,4,5,6,7,9,10],
      y: [1, 0.9983209402734469, 0.998201007435836, 0.9973614775725593, 0.9974814104101704, 0.9972415447349484, 0.9972415447349484, 0.9972415447349484, 0.9972415447349484,  0.9972415447349484],
      line: {
        color: "#17BECF"
      }
    };

    var trace1 = {
      type: "scatter",
      mode: "lines",
      name: "Training Accuracy",
      // x: data.map(row => row.x),
      // y: data.map(row => row.y2),
      x: [1,2,3,4,5,6,7,9,10],
      y: [0.99568345323741, 0.9971223021582734, 0.9978417266187051, 0.9964028776978417, 0.9974820143884892, 0.9971223021582734, 0.9971223021582734,0.9967625899280576, 0.9971223021582734, 0.9967625899280576],
      line: {
        color: "#FF8C00"
      }
    };

    var plot_data = [trace1, trace2];

    // var layout = { margin: { t: 30, b: 100 } };
    var layout = { 
      title: "knnAnalysisPlot",
      xaxis: { title: "Number of Nearest Neighbors" },
      yaxis: { title: "Accuracy", autorange: true, type: "linear"},
    };

    Plotly.plot("plot", plot_data, layout);
  });
}

// function init() {
//     // knnAnalysisPlot(data_source_url);
//     knnAnalysisPlot();
// }

// init();
knnAnalysisPlot();



// d3.json(data_source_url).then(function (response) {
//   var sightings = response.test_accuracy;
//   sightings.forEach(function (s) {
//       console.log(s);