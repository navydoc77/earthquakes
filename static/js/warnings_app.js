function createDropDown() {
  var selector = d3.select("#selDataset");
  d3.json("/warnings_categories").then((sampleNames) => {
      sampleNames.forEach((sample) => {
        console.log(sample);
        selector
          .append("option")
          .text(sample)
          .property("value", sample);
      });
  });
}


function initializeTable() {
  d3.json("/warnings_categories").then(function (data) {
    console.log(data)
    var warning_category = data[0];
    console.log(warning_category);
    contructTable(warning_category);
  });
}

function contructTable(warning_category) {
  d3.json(`/api/warnings/${warning_category}`).then(function (data) {
    console.log(data)
    var tableData = data;
    console.log(tableData);

    // Select the table body tag
    var tbody = d3.select("tbody");

    // Append info for each warning to the table body
    tableData.forEach(warning => {
        //Create new row for each warning
        var row = tbody.append("tr");
        Object.entries(warning).forEach(function([key, value]) {
            //Append all values of the warning to the row
            var td = row.append("td").text(value);
        });
    });
});
}

function updateTable(warning_category) {
  d3.json(`/api/warnings/${warning_category}`).then(function (data) {
    console.log(data);
    console.log(data[0]);

    var tableData = data;

    // Select the table body tag
    var tbody = d3.select("tbody");
    tbody.html("");

    // Append info for each warning to the table body
    tableData.forEach(warning => {
        //Create new row for each warning
        var row = tbody.append("tr");
        Object.entries(warning).forEach(function([key, value]) {
            //Append all values of the warning to the row
            var td = row.append("td").text(value);         
        });
    });
  });
}

function init() {
  createDropDown();
  initializeTable();
}

  // Fetch new data each time a new sample is selected
function optionChanged(newSelection) {
  console.log(newSelection);
  updateTable(newSelection);
}

init();
