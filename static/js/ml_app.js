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

// **************************************************
// *************** INITIALIZE PLOT *****************
// **************************************************

function initializeKNNPlot() {
  d3.json(data_source_url).then(function(data) {
    
    var plot_data = data;
    var case_x = plot_data["case8"]["x"];
    var case_test_scores = plot_data["case8"]["test_scores"];
    var case_train_scores = plot_data["case8"]["training_scores"];

    
    var trace1 = {
      marker: {'symbol': 27},
      type: "scatter",
      mode: "markers+lines",
      name: "Training Accuracy",
      showlegend: false,
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
      showlegend: false,
      x: case_x,
      y: case_test_scores,
      line: {
        color: "#17BECF"
      }
    };

    var plot_data = [trace1, trace2];

    var layout = { 
      title: "Comparison of Training and Test Accuracy as a function of the number of neighbors.",
      xaxis: { title: "Number of Nearest Neighbors" },
      yaxis: { title: "Accuracy", autorange: true, type: "linear"},
    };

    Plotly.plot("plot", plot_data, layout);
  });
}

function initializeRocCurve() {
  d3.json(data_source_url).then(function(data) {
    var plot_data = data;
    var fpr = plot_data["case8"]["fpr_array"];
    var tpr = plot_data["case8"]["tpr_array"];
    var colors = ['#00004d', '#000066', '#000080', '#000099', '#0000b3', '#0000cc', '#0000e6', '#0000ff', '#1a1aff', '#3333ff']

    ////////////////// PREPARE VARIABLES FOR PLOTING /////////////////
  
    var trace0_fpr = fpr[0];
    var trace0_tpr = tpr[0];
  
    var trace1_fpr = fpr[1];
    var trace1_tpr = tpr[1];
  
    var trace2_fpr = fpr[2];
    var trace2_tpr = tpr[2];
  
    var trace3_fpr = fpr[3];
    var trace3_tpr = tpr[3];
  
    var trace4_fpr = fpr[4];
    var trace4_tpr = tpr[4];
  
    var trace5_fpr = fpr[5];
    var trace5_tpr = tpr[5];
  
    var trace6_fpr = fpr[6];
    var trace6_tpr = tpr[6];
  
    var trace7_fpr = fpr[7];
    var trace7_tpr = tpr[7];
  
    var trace8_fpr = fpr[8];
    var trace8_tpr = tpr[8];
  
    var trace9_fpr = fpr[9];
    var trace9_tpr = tpr[9];
  
  
    var trace0 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 1",
      x: trace0_fpr,
      y: trace0_tpr,
      line: {
        color: colors[0]
      }
    };
  
    var trace1 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 2",
      x: trace1_fpr,
      y: trace1_tpr,
      line: {
        color: colors[1]
      }
    };
  
    var trace2 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 3",
      x: trace2_fpr,
      y: trace2_tpr,
      line: {
        color: colors[2]
      }
    };
  
    var trace3 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 4",
      x: trace3_fpr,
      y: trace3_tpr,
      line: {
        color: colors[3]
      }
    };
  
    var trace4 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 5",
      x: trace4_fpr,
      y: trace4_tpr,
      line: {
        color: colors[4]
      }
    };
  
    var trace5 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 6",
      x: trace5_fpr,
      y: trace5_tpr,
      line: {
        color: colors[5]
      }
    };
  
    var trace6 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 7",
      x: trace6_fpr,
      y: trace6_tpr,
      line: {
        color: colors[6]
      }
    };
  
    var trace7 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 8",
      x: trace7_fpr,
      y: trace7_tpr,
      line: {
        color: colors[7]
      }
    };
  
    var trace8 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 9",
      x: trace8_fpr,
      y: trace8_tpr,
      line: {
        color: colors[8]
      }
    };
  
    var trace9 = {
      marker: {'symbol': 1},
      type: "scatter",
      mode: "markers+lines",
      name: "neighbors = 10",
      x: trace9_fpr,
      y: trace9_tpr,
      line: {
        color: colors[9]
      }
    };
  
    var trace10 = {
      marker: {'symbol': 1},
      type: "scatter",
      x: [0,1],
      y: [0,1],
      mode: "markers+lines",
      showlegend: false,
      line: {
        color : "navy",
        width : 4,
        dash : 'dash',
      }
    };
    
    var layout = { 
      title: 'Receiver Operating Characteristic (ROC)',
      xaxis: { title: 'False Positive Rate' },
      yaxis: { title: "True Positive Rate", autorange: true, type: "linear"},
    };
  
    var roc_plot = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10];
  
    Plotly.plot("roc_plot", roc_plot, layout);

  });
}

function initialStackedPlot() {
  d3.json(data_source_url).then(function(data) {
  var plot_data = data;

  ////////////////// PREPARE VARIABLES FOR PLOTING /////////////////
  var x = plot_data["case8"]["x"];
  var prefix = plot_data["case8"]["confusion_matrix_arrays"];
  var tn_array = [prefix[0][0], prefix[1][0], prefix[2][0], prefix[3][0], prefix[4][0], prefix[5][0], prefix[6][0], prefix[7][0], prefix[8][0], prefix[9][0]];
  var fp_array = [prefix[0][1], prefix[1][1], prefix[2][1], prefix[3][1], prefix[4][1], prefix[5][1], prefix[6][1], prefix[7][1], prefix[8][1], prefix[9][1]];
  var fn_array = [prefix[0][2], prefix[1][2], prefix[2][2], prefix[3][2], prefix[4][2], prefix[5][2], prefix[6][2], prefix[7][2], prefix[8][2], prefix[9][2]];
  var tp_array = [prefix[0][3], prefix[1][3], prefix[2][3], prefix[3][3], prefix[4][3], prefix[5][3], prefix[6][3], prefix[7][3], prefix[8][3], prefix[9][3]];
  
  
  var trace1 = {
    x: x,
    y: tn_array,
    name: 'True Negative',
    type: 'bar'
  };
  
  var trace2 = {
    x: x,
    y: fp_array,
    name: 'False Positive',
    type: 'bar'
  };

  var trace3 = {
    x: x,
    y: fn_array,
    name: 'False Neagative',
    type: 'bar'
  };

  var trace4 = {
    x: x,
    y: tp_array,
    name: 'True Positive',
    type: 'bar'
  };
  
  var data = [trace1, trace2, trace3, trace4];
  
  var layout = {barmode: 'stack', title : 'Confusion Matrix Analysis by Number of Nearest Neighbor'};

  Plotly.newPlot('stack', data, layout);
  });
}

function constructTable() {
  d3.json(data_source_url).then(function(data) {
  var table_data = data["case8_df"];
  var toArray = JSON.parse("[" + table_data + "]");

  // Select the table header tag
  var thead = d3.select('thead');
  thead.html("");

  // Append info for each warning to the table body
  const header_keys = Object.keys(Object.values(toArray[0])[0]);
  Object.entries(header_keys).forEach(function([key, value]) {
    //Append all values of the event to the row
    var th = thead.append("th").text(value);
  });


  // Select the table body tag
  var tbody = d3.select("tbody");
  tbody.html("");    
    
  toArray[0].forEach(event => {
    //Create new row for each event
    var row = tbody.append("tr");
    Object.entries(event).forEach(function([key, value]) {
      //Append all values of the event to the row
      var td = row.append("td").text(value);
      });
  });
  });
}

// **************************************************
// ******* RESPONCE AND REPLOT FUNCTIONS ************
// **************************************************

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
    title: "Comparison of Training and Test Accuracy as a function of the number of neighbors.",
    xaxis: { title: "Number of Nearest Neighbors" },
    yaxis: { title: "Accuracy", autorange: true, type: "linear"},
  };

  Plotly.deleteTraces('plot', [0,1]);
  Plotly.plot("plot", plot_data, layout);
}

function buildRocCurve(case_fpr, case_tpr) {
  Plotly.deleteTraces('roc_plot', [0,1,2,3,4,5,6,7,8,9,10]);

  var fpr = case_fpr;
  var tpr = case_tpr;
  var colors = ['#00004d', '#000066', '#000080', '#000099', '#0000b3', '#0000cc', '#0000e6', '#0000ff', '#1a1aff', '#3333ff']

  ////////////////// PREPARE VARIABLES FOR PLOTING /////////////////

  var trace0_fpr = fpr[0];
  var trace0_tpr = tpr[0];

  var trace1_fpr = fpr[1];
  var trace1_tpr = tpr[1];

  var trace2_fpr = fpr[2];
  var trace2_tpr = tpr[2];

  var trace3_fpr = fpr[3];
  var trace3_tpr = tpr[3];

  var trace4_fpr = fpr[4];
  var trace4_tpr = tpr[4];

  var trace5_fpr = fpr[5];
  var trace5_tpr = tpr[5];

  var trace6_fpr = fpr[6];
  var trace6_tpr = tpr[6];

  var trace7_fpr = fpr[7];
  var trace7_tpr = tpr[7];

  var trace8_fpr = fpr[8];
  var trace8_tpr = tpr[8];

  var trace9_fpr = fpr[9];
  var trace9_tpr = tpr[9];


  var trace0 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 1",
    x: trace0_fpr,
    y: trace0_tpr,
    line: {
      color: colors[0]
    }
  };

  var trace1 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 2",
    x: trace1_fpr,
    y: trace1_tpr,
    line: {
      color: colors[1]
    }
  };

  var trace2 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 3",
    x: trace2_fpr,
    y: trace2_tpr,
    line: {
      color: colors[2]
    }
  };

  var trace3 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 4",
    x: trace3_fpr,
    y: trace3_tpr,
    line: {
      color: colors[3]
    }
  };

  var trace4 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 5",
    x: trace4_fpr,
    y: trace4_tpr,
    line: {
      color: colors[4]
    }
  };

  var trace5 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 6",
    x: trace5_fpr,
    y: trace5_tpr,
    line: {
      color: colors[5]
    }
  };

  var trace6 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 7",
    x: trace6_fpr,
    y: trace6_tpr,
    line: {
      color: colors[6]
    }
  };

  var trace7 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 8",
    x: trace7_fpr,
    y: trace7_tpr,
    line: {
      color: colors[7]
    }
  };

  var trace8 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 9",
    x: trace8_fpr,
    y: trace8_tpr,
    line: {
      color: colors[8]
    }
  };

  var trace9 = {
    marker: {'symbol': 1},
    type: "scatter",
    mode: "markers+lines",
    name: "neighbors = 10",
    x: trace9_fpr,
    y: trace9_tpr,
    line: {
      color: colors[9]
    }
  };

  var trace10 = {
    marker: {'symbol': 1},
    type: "scatter",
    x: [0,1],
    y: [0,1],
    mode: "markers+lines",
    showlegend: false,
    line: {
      color : "navy",
      width : 4,
      dash : 'dash',
    }
  };
  
  var layout = { 
    title: 'Receiver Operating Characteristic (ROC)',
    xaxis: { title: 'False Positive Rate' },
    yaxis: { title: "True Positive Rate", autorange: true, type: "linear"},
  };

  var roc_plot = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10];

  Plotly.plot("roc_plot", roc_plot, layout);
}

function reStackPlot(case_x) {
  d3.json(data_source_url).then(function(data) {
  var plot_data = data;
  Plotly.deleteTraces('stack', [0,1,2,3]);

  ////////////////// PREPARE VARIABLES FOR PLOTING /////////////////
  var x = plot_data[case_x]["x"];
  var prefix = plot_data[case_x]["confusion_matrix_arrays"];
  var tn_array = [prefix[0][0], prefix[1][0], prefix[2][0], prefix[3][0], prefix[4][0], prefix[5][0], prefix[6][0], prefix[7][0], prefix[8][0], prefix[9][0]];
  var fp_array = [prefix[0][1], prefix[1][1], prefix[2][1], prefix[3][1], prefix[4][1], prefix[5][1], prefix[6][1], prefix[7][1], prefix[8][1], prefix[9][1]];
  var fn_array = [prefix[0][2], prefix[1][2], prefix[2][2], prefix[3][2], prefix[4][2], prefix[5][2], prefix[6][2], prefix[7][2], prefix[8][2], prefix[9][2]];
  var tp_array = [prefix[0][3], prefix[1][3], prefix[2][3], prefix[3][3], prefix[4][3], prefix[5][3], prefix[6][3], prefix[7][3], prefix[8][3], prefix[9][3]];
  
  
  var trace1 = {
    x: x,
    y: tn_array,
    name: 'True Negative',
    type: 'bar'
  };
  
  var trace2 = {
    x: x,
    y: fp_array,
    name: 'False Positive',
    type: 'bar'
  };

  var trace3 = {
    x: x,
    y: fn_array,
    name: 'False Negative',
    type: 'bar'
  };

  var trace4 = {
    x: x,
    y: tp_array,
    name: 'True Positive',
    type: 'bar'
  };
  
  var data = [trace1, trace2, trace3, trace4];
  
  var layout = {barmode: 'stack', title : 'Confusion Matrix Analysis by Number of Nearest Neighbor'};
  
  Plotly.newPlot('stack', data, layout);
  });
}

function reBuildTable(toArray) {

  // Select the table header tag
  var thead = d3.select('thead');
  thead.html("");

  // Append info for each warning to the table body
  const header_keys = Object.keys(Object.values(toArray[0])[0]);
  Object.entries(header_keys).forEach(function([key, value]) {
    //Append all values of the event to the row
    var th = thead.append("th").text(value);
  });

  // Select the table body tag
  var tbody = d3.select("tbody");
  tbody.html("");    
    
  toArray[0].forEach(event => {
    //Create new row for each event
    var row = tbody.append("tr");
    Object.entries(event).forEach(function([key, value]) {
      //Append all values of the event to the row
      var td = row.append("td").text(value);
      });
  });


}

function getCheckedAndPlot() {
  d3.json(data_source_url).then(function(data) {
    var plot_data = data;

    ////////  GET INFORMATION FROM CHECKED FIELD  //////////////
    var lng = document.getElementById("lng").checked;
    var depth = document.getElementById("depth").checked;
    var magnitude =  document.getElementById("magnitude").checked;

    ////////  STORE CHECKED INFORMATION INTO AN ARRAY //////////////
    var check_array = [lng, depth, magnitude];


    ////////  POTENTIAL CHECKBOX PROFILES ON SUBMIT //////////////
    var case1 = [true, true, true];
    var case2 = [true, true, false];
    var case3 = [true, false, true];
    var case4 = [false, true, true];
    var case5 = [true, false, false];
    var case6 = [false, true, false];
    var case7 = [false, false, true];
    var case8 = [false, false, false];

    ////////  TEST TO CHECK IF CHECKED PROFILE MATCHES CASE //////////////
    var test_outcome= isEqual(check_array, case1);


    if (isEqual(check_array, case1) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ///////////////////
      var case_x = plot_data["case1"]["x"];
      var case_test_scores = plot_data["case1"]["test_scores"];
      var case_train_scores = plot_data["case1"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////
      var case1_fpr = plot_data["case1"]["fpr_array"];
      var case1_tpr = plot_data["case1"]["tpr_array"];
      buildRocCurve(case1_fpr, case1_tpr);

      //////////////// STACKED BAR PLOT  ///////////////////////      
      var casex = 'case1';    
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case1_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case2) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////
      var case_x = plot_data["case2"]["x"];
      var case_test_scores = plot_data["case2"]["test_scores"];
      var case_train_scores = plot_data["case2"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////
      var case2_fpr = plot_data["case2"]["fpr_array"];
      var case2_tpr = plot_data["case2"]["tpr_array"];
      buildRocCurve(case2_fpr, case2_tpr);

      //////////////// STACKED BAR PLOT  ////////////////////  
      var casex = 'case2';    
      reStackPlot(casex);
    
      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case2_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case3) == "True") {


      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////      
      var case_x = plot_data["case3"]["x"];
      var case_test_scores = plot_data["case3"]["test_scores"];
      var case_train_scores = plot_data["case3"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////      
      var case3_fpr = plot_data["case3"]["fpr_array"];
      var case3_tpr = plot_data["case3"]["tpr_array"];
      buildRocCurve(case3_fpr, case3_tpr);

      //////////////// STACKED BAR PLOT  ////////////////////  
      var casex = 'case3';
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case3_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case4) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////  
      var case_x = plot_data["case4"]["x"];
      var case_test_scores = plot_data["case4"]["test_scores"];
      var case_train_scores = plot_data["case4"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////
      var case4_fpr = plot_data["case4"]["fpr_array"];
      var case4_tpr = plot_data["case4"]["tpr_array"];
      buildRocCurve(case4_fpr, case4_tpr);

      //////////////// STACKED BAR PLOT  //////////////////// 
      var casex = 'case4';
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case4_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case5) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////       
      var case_x = plot_data["case5"]["x"];
      var case_test_scores = plot_data["case5"]["test_scores"];
      var case_train_scores = plot_data["case5"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////      
      var case5_fpr = plot_data["case5"]["fpr_array"];
      var case5_tpr = plot_data["case5"]["tpr_array"];
      buildRocCurve(case5_fpr, case5_tpr);

      //////////////// STACKED BAR PLOT  ////////////////////       
      var casex = 'case5';
      reStackPlot(casex);
      
      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case5_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case6) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////      
      var case_x = plot_data["case6"]["x"];
      var case_test_scores = plot_data["case6"]["test_scores"];
      var case_train_scores = plot_data["case6"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////         
      var case6_fpr = plot_data["case6"]["fpr_array"];
      var case6_tpr = plot_data["case6"]["tpr_array"];
      buildRocCurve(case6_fpr, case6_tpr);

      //////////////// STACKED BAR PLOT  //////////////////// 
      var casex = 'case6';
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case6_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case7) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  //////////////////// 
      var case_x = plot_data["case7"]["x"];
      var case_test_scores = plot_data["case7"]["test_scores"];
      var case_train_scores = plot_data["case7"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////       
      var case7_fpr = plot_data["case7"]["fpr_array"];
      var case7_tpr = plot_data["case7"]["tpr_array"];
      buildRocCurve(case7_fpr, case7_tpr);

      //////////////// STACKED BAR PLOT  //////////////////// 
      var casex = 'case7';
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case7_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);

    } else if (isEqual(check_array, case8) == "True") {

      //////////////// KNN vs N_NEIGHBOR PLOT  ////////////////////       
      var case_x = plot_data["case8"]["x"];
      var case_test_scores = plot_data["case8"]["test_scores"];
      var case_train_scores = plot_data["case8"]["training_scores"];
      buildplot(case_x, case_train_scores, case_test_scores);

      //////////////// ROC PLOT  ////////////////////
      var case8_fpr = plot_data["case8"]["fpr_array"];
      var case8_tpr = plot_data["case8"]["tpr_array"];
      buildRocCurve(case8_fpr, case8_tpr);

      //////////////// STACKED BAR PLOT  //////////////////// 
      var casex = 'case8';
      reStackPlot(casex);

      //////////////////////  TABLE  ////////////////////////////
      var table_data = data["case8_df"];
      var toArray = JSON.parse("[" + table_data + "]");
      reBuildTable(toArray);
      
    } else {
      console.log("failed")
    }
  });
}


// **************************************************
// *************** INITIALIZE ***********************
// **************************************************

function init() {
  initializeKNNPlot();
  initializeRocCurve();
  initialStackedPlot();
  // initializeTable();
  constructTable();
}

// **************************************************
// ********************** RUN ***********************
// **************************************************


init();
getCheckedAndPlot();
