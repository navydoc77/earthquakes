// # ************************************
// # CREATE DROPDOWN MENU
// # ************************************
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


function init() {
    createDropDown();
}

init();