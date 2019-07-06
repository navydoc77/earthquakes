/***********************************
* Step0: Get data from flask route *
***********************************/


<<<<<<< HEAD
var url = 'http://127.0.0.1:5000/tornadoes'

d3.json(url).then(function (data) { 
  
=======
//var url = 'http://127.0.0.1:5000/tornadoes'

d3.json("/api/tornadoes").then(function (data) { 

>>>>>>> b6fb19551a4f734019eec02497a89c0ac77642a0
  var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

    data.forEach(function(d) { 
        //d.dtg   = dtgFormat(d.dtg.substr(0,19));
        //var formatDate = d3.timeFormat("%Y-%m-%d% %H:%M:%S");
        d.dtg   = parseDate(d.dtg);
        d.s_lat   = +d.s_lat;
        d.s_lng  = +d.s_lng;
        d.mag   = +d.mag;
        d.width = +d.width;
        });

/******************************************************
* Step1: Create the dc.js chart objects & ling to div *
******************************************************/

  var magnitudeChart = dc.barChart("#dc-magnitude-chart");
  var widthChart = dc.barChart("#dc-width-chart");
  var timeChart = dc.lineChart("#dc-time-chart");
  var dataTable = dc.dataTable("#dc-table-graph");

/****************************************
* 	Run the data through crossfilter    *
****************************************/

  var facts = crossfilter(data);  // Gets our 'facts' into crossfilter

/******************************************************
* Create the Dimensions                               *
* A dimension is something to group or filter by.     *
* Crossfilter can filter by exact value, or by range. *
******************************************************/

  // for Magnitude
  var magValue = facts.dimension(function (d) {
    return d.mag;       // group or filter by magnitude
  });
  var magValueGroupSum = magValue.group()
    .reduceSum(function(d) { return d.mag; });	// sums the magnitudes per magnitude
  var magValueGroupCount = magValue.group()
    .reduceCount(function(d) { return d.mag; }) // counts the number of the facts by magnitude

  // For datatable
  var timeDimension = facts.dimension(function (d) {
    return d3.timeYear(d.dtg);
  }); // group or filter by time

  // for width
  var widthValue = facts.dimension(function (d) {
    return d.width;
  });
  var widthValueGroup = widthValue.group();
  
  // define a daily volume Dimension
  var volumeByYear = facts.dimension(function(d) {
    return d3.timeYear(d.dtg);
    //return d3.time.hour(d.dtg);
    //console.log(d3.timeHour(d.dtg));
  });
  // map/reduce to group sum
  var volumeByYearGroup = volumeByYear.group()
    .reduceCount(function(d) { return d.dtg; });

/***************************************
* 	Step4: Create the Visualisations   *
***************************************/
  
  // Magnitude Bar Graph Summed
  magnitudeChart.width(480)
    .height(150)
    .margins({top: 10, right: 10, bottom: 20, left: 40})
    .dimension(magValue)								// the values across the x axis
    .group(magValueGroupSum)							// the values on the y axis
	.transitionDuration(500)
    .centerBar(true)	
	.gap(56)                                            // bar width Keep increasing to get right then back off.
    .x(d3.scaleLinear().domain([0.5, 7.5]))
	.elasticY(true)
	.xAxis().tickFormat(function(v) {return v;});	

  // width bar graph
  widthChart.width(480)
    .height(150)
    .margins({top: 10, right: 10, bottom: 20, left: 40})
    .dimension(widthValue)
    .group(widthValueGroup)
	.transitionDuration(1000)
    .centerBar(true)	
	.gap(50)                    // bar width Keep increasing to get right then back off.
    .x(d3.scaleLinear().domain([0, 4600]))
	.elasticY(true)
	.xAxis().tickFormat(function(v) {return v;});

  // time graph
  timeChart.width(960)
    .height(100)
    .margins({top: 10, right: 10, bottom: 20, left: 40})
    .dimension(volumeByYear)
    .group(volumeByYearGroup)
    .transitionDuration(500)
	.elasticY(true)
    .x(d3.scaleTime().domain([new Date(1950, 1, 1), new Date(2018, 12, 31)])) // scale and domain of the graph
    .xAxis();

  // Table of tornado data
  dataTable.width(960).height(800)
    .dimension(timeDimension)
	.section(function(d) { return "List of all tornadoes corresponding to the filters"
	 })
	.size(500)							// number of rows to return
    .columns([
      function(d) { return d.dtg; },
      function(d) { return d.s_lat; },
      function(d) { return d.s_lng; },
      function(d) { return d.width; },
      function(d) { return d.mag; },
	  function(d) { return '<a href=\"http://maps.google.com/maps?z=11&t=m&q=loc:' + d.s_lat + '+' + d.s_lng +"\" target=\"_blank\">Google Map</a>"},
	  function(d) { return '<a href=\"http://www.openstreetmap.org/?mlat=' + d.s_lat + '&mlon=' + d.s_lng +'&zoom=11'+ "\" target=\"_blank\"> OSM Map</a>"}
    ])
    .sortBy(function(d){ return d.dtg; })
    .order(d3.ascending);

/****************************
* Step6: Render the Charts  *
****************************/
			
  dc.renderAll();
  
});