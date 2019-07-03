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


// Data structure from app.py
// all_knn_analysis_data = {
//   "case1" : all_data,
//   "case2" : lng_depth_data,
//   "case3" : lng_magnitude_data,
//   "case4" : depth_magnitude_data,
//   "case5" : lng_data,
//   "case6" : depth_data, 
//   "case7" : magnitude_data,
//   "case8" : lat_data
// }

function knnAnalysisPlot() {
  d3.json(data_source_url).then(function(data) {
    var data = [data];
    console.log(data)
    var test = data.map(row=>row.all_knn_analysis_data)
    console.log(test[0])
    var case_one = data.map(row => row.all_knn_analysis_data.case1.x);
    console.log(case_one[0]);

    var x = [];
    var test_accuracy = [];
    var training_accuracy = [];

    // var x = data.map(row => row.all_data.x);
    // var test_accuracy = data.map(row => row.all_data.y1);
    // var training_accuracy = data.map(row => row.all_data.y2);

    var trace2 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "Test Accuracy",
      x: x[0],
      y: test_accuracy[0],
      line: {
        color: "#17BECF"
      }
    };

    var trace1 = {
      marker: {'symbol': 27},
      type: "scatter",
      mode: "markers+lines",
      name: "Training Accuracy",
      x: x[0],
      y: training_accuracy[0],
      line: {
        color: "#FF8C00"
      }
    };

    var plot_data = [trace1, trace2];

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