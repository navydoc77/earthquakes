// **************************************************
// *************** UTILITY FUNCTIONS ****************
// **************************************************

function isEqual(a,b) {  
    if (a.length != b.length) {return false};
    for(var i=0; i<a.length; i++) 
      if(a[i]!=b[i]) {
        return "False"};  
    return "True";
  }

function buildplot(x, train, test) {
  var trace1 = {
    marker: {'symbol': 27},
    type: "scatter",
    mode: "markers+lines",
    name: "Training Accuracy",
    x: x,
    y: train,
    line: {
      color: "#FF8C00"
    }
  };

  var trace2 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "Test Accuracy",
    x: x,
    y: test,
    line: {
      color: "#17BECF"
    }
  };

  var plot_data = [trace1, trace2];

  var layout = { 
    title: "knnAnalysisPlot",
    xaxis: { title: "Number of Nearest Neighbors" },
    yaxis: { title: "Accuracy", autorange: true, type: "linear"},
  };
  Plotly.plot("plot", plot_data, layout);
}

function buildRocCurve(fpr, tpr) {

  var trace3 = {
    mode: lines,
    name: "Test Data",
    x: fpr,
    y: tpr,
    line: {
      color: "#281158"
    }
  };

  var trace4 = {
    x: [0,1],
    y: [0,1],
    mode: lines,
    line: {
      color : "navy",
      width : lw,
      dash : 'dash',
    }
  };
  
  var layout = { 
    title: 'ROC Curve (AUC)',
    xaxis: { title: 'False Positive Rate' },
    yaxis: { title: "True Positive Rate", autorange: true, type: "linear"},
  };

  var roc_plot_data = [trace3, trace4];

  Plotly.plot("roc_plot", roc_plot_data, layout);

}

// **************************************************
// *************** RESPONCE AND PLOT ****************
// **************************************************


function getCheckedAndPlot() {
  d3.json(data_source_url).then(function(data) {
    var plot_data = data;

    ////////  GET INFORMATION FROM CHECKED FIELD  //////////////
    var lng = document.getElementById("lng").checked;
    var depth = document.getElementById("depth").checked;
    var magnitude =  document.getElementById("magnitude").checked;
    console.log(lng);
    console.log(depth);
    console.log(magnitude);

    ////////  STORE CHECKED INFORMATION INTO AN ARRAY //////////////
    var check_array = [lng, depth, magnitude];


    ////////  POTENTIAL CHECKBOX PROFILES ON SUBMIT //////////////
    var case1 = [true, true, true];
    var case2 = [true, true, false];
    var case3 = [true, true, false];
    var case4 = [false, true, true];
    var case5 = [true, false, false];
    var case6 = [false, true, false];
    var case7 = [false, false, true];
    var case8 = [false, false, false];

    ////////  TEST TO CHECK IF CHECKED PROFILE MATCHES CASE //////////////
    var test_outcome= isEqual(check_array, case1);
    console.log(test_outcome);


    Plotly.deleteTraces("plot", 0);
    if (isEqual(check_array, case1) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case1"]["x"];
      var case_test_scores = plot_data["case1"]["test_scores"];
      var case_train_scores = plot_data["case1"]["training_scores"];
      console.log(case1);

      var fpr = [plot_data["case1"]["frp0"][0], plot_data["case1"]["frp0"][0], plot_data["case1"]["frp0"][0]];
      console.log(fpr);
      var tpr = [plot_data["case1"]["trp0"][0], plot_data["case1"]["trp1"][0], plot_data["case1"]["trp2"][0]];
      console.log(fpr);
      buildplot(case_x, case_train_scores, case_test_scores);
      buildRocCurve(fpr, tpr);
    } else if (isEqual(check_array, case2) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case2"]["x"];
      var case_test_scores = plot_data["case2"]["test_scores"];
      var case_train_scores = plot_data["case2"]["training_scores"];
      console.log(case2);

      var fpr = [plot_data["case2"]["frp0"][1], plot_data["case2"]["frp0"][1], plot_data["case2"]["frp0"][1]];
      console.log(fpr);
      var tpr = [plot_data["case2"]["trp0"][1], plot_data["case2"]["trp1"][1], plot_data["case2"]["trp2"][1]];
      console.log(fpr);
      buildplot(case_x, case_train_scores, case_test_scores);      
    } else if (isEqual(check_array, case3) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case3"]["x"];
      var case_test_scores = plot_data["case3"]["test_scores"];
      var case_train_scores = plot_data["case3"]["training_scores"];
      console.log(case3);

      buildplot(case_x, case_train_scores, case_test_scores);
    } else if (isEqual(check_array, case4) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case4"]["x"];
      var case_test_scores = plot_data["case4"]["test_scores"];
      var case_train_scores = plot_data["case4"]["training_scores"];
      console.log(case4);

      buildplot(case_x, case_train_scores, case_test_scores);
    } else if (isEqual(check_array, case5) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case5"]["x"];
      var case_test_scores = plot_data["case5"]["test_scores"];
      var case_train_scores = plot_data["case5"]["training_scores"];
      console.log(case5);

      buildplot(case_x, case_train_scores, case_test_scores);
    } else if (isEqual(check_array, case6) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case6"]["x"];
      var case_test_scores = plot_data["case6"]["test_scores"];
      var case_train_scores = plot_data["case6"]["training_scores"];
      console.log(case6);

      buildplot(case_x, case_train_scores, case_test_scores);
    } else if (isEqual(check_array, case7) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case7"]["x"];
      var case_test_scores = plot_data["case7"]["test_scores"];
      var case_train_scores = plot_data["case7"]["training_scores"];
      console.log(case7);

      buildplot(case_x, case_train_scores, case_test_scores);
    } else if (isEqual(check_array, case8) == "True") {
      Plotly.deleteTraces("plot", 0);
      var case_x = plot_data["case8"]["x"];
      var case_test_scores = plot_data["case8"]["test_scores"];
      var case_train_scores = plot_data["case8"]["training_scores"];
      console.log(case8);
      buildplot(case_x, case_train_scores, case_test_scores);
    } else {
      console.log("failed")
    }
  });
}


// **************************************************
// *************** RESPONCE AND PLOT ****************
// **************************************************


function initializePlot() {
  d3.json(data_source_url).then(function(data) {
    
    var plot_data = data;
    // console.log(plot_data);
    var case_x = plot_data["case1"]["x"];
    var case_test_scores = plot_data["case1"]["test_scores"];
    var case_train_scores = plot_data["case1"]["training_scores"];
    
    var trace1 = {
      marker: {'symbol': 27},
      type: "scatter",
      mode: "markers+lines",
      name: "Training Accuracy",
      x: case_x,
      y: case_train_scores,
      line: {
        color: "#FF8C00"
      }
    };

    var trace2 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "Test Accuracy",
      x: case_x,
      y: case_test_scores,
      line: {
        color: "#17BECF"
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

initializePlot();
Plotly.deleteTraces('plot', 0);
getCheckedAndPlot();
