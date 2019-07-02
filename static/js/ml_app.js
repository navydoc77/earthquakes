// # ************************************
// # CREATE DROPDOWN MENU
// # ************************************
var CheckboxHandler = new Object();

function createDropDown() {
    var selector = d3.select("#selDataset");
    d3.json("/magnitudes").then((data) => {
        data.forEach((d) => {
          console.log(d);
          selector
            .append("option")
            .text(d)
            .property("value", d);
        });
    });
}

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


function knnAnalysisPlot(data_source_url) {
    console.log(data_source_url);
    d3.json(data_source_url).then(function (response) {
        var sightings = response.test_accuracy;
        sightings.forEach(function (s) {
            console.log(s);
        });
    });
}


function init() {
    knnAnalysisPlot(data_source_url);
}

init();