/***********************************
* Step0: Get data from flask route *
***********************************/


//var url = 'http://127.0.0.1:5000/volcano_filter_viz'

d3.json("api/volcano_filter_viz").then(function (data) { 19
  
  var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

    data.forEach(function(d) { 
        //d.dtg   = dtgFormat(d.dtg.substr(0,19));
        //var formatDate = d3.timeFormat("%Y-%m-%d% %H:%M:%S");
        d.dtg   = parseDate(d.dtg);
        d.lat   = +d.lat;
        d.lng  = +d.lng;
        d.volcanic_index = +d.volcanic_index;
        d.death = +d.death;
        });

/******************************************************
* Step1: Create the dc.js chart objects & ling to div *
******************************************************/

  var volcanicIndex = dc.barChart("#dc-volcanic-index-chart");
  var deathChart = dc.barChart("#dc-death-chart");
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

  // for Volcanic Index
  var volcanicIndexValue = facts.dimension(function (d) {
    return d.volcanic_index;       // group or filter by Volcanic Index
  });
  var volcanicIndexValueGroupSum = volcanicIndexValue.group()
    .reduceSum(function(d) { return d.volcanic_index; });	// sums the Volcanic Indexs per Volcanic Index
  var volcanicIndexValueGroupCount = volcanicIndexValue.group()
    .reduceCount(function(d) { return d.volcanic_index; }) // counts the number of the facts by Volcanic Index

  // For datatable
  var timeDimension = facts.dimension(function (d) {
    return d3.timeYear(d.dtg);
  }); // group or filter by time

  // for death
  var deathValue = facts.dimension(function (d) {
    return d.death;
  });
  var deathValueGroup = deathValue.group();
  
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
* 	Step4: Create the Visualizations   *
***************************************/
  
  // Volcanic Index Bar Graph Summed
  volcanicIndex.width(480)
    .height(150)
    .margins({top: 10, right: 10, bottom: 20, left: 40})
    .dimension(volcanicIndexValue)								// the values across the x axis
    .group(volcanicIndexValueGroupSum)							// the values on the y axis
	.transitionDuration(500)
    .centerBar(true)	
	.gap(56)                                            // bar width Keep increasing to get right then back off.
    .x(d3.scaleLinear().domain([0.5, 7.5]))
	.elasticY(true)
	.xAxis().tickFormat(function(v) {return v;});	

  // death bar graph
  deathChart.width(500)
    .height(150)
    .margins({top: 10, right: 10, bottom: 20, left: 40})
    .dimension(deathValue)
    .group(deathValueGroup)
	.transitionDuration(500)
    .centerBar(true)	
	.gap(500)                    // bar width Keep increasing to get right then back off.
    .x(d3.scaleLinear().domain([0, 10000]))
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
    .x(d3.scaleTime().domain([new Date(1900, 1, 1), new Date(2019, 12, 31)])) // scale and domain of the graph
    .xAxis();

  // Table of volcano data
  dataTable.width(960).height(800)
    .dimension(timeDimension)
	.section(function(d) { return "List of all volcanoes corresponding to the filters"
	 })
	.size(500)							// number of rows to return
    .columns([
      function(d) { return d.dtg; },
      function(d) { return d.lat; },
      function(d) { return d.lng; },
      function(d) { return d.death; },
      function(d) { return d.volcanic_index; },
	  function(d) { return '<a href=\"http://maps.google.com/maps?z=11&t=m&q=loc:' + d.lat + '+' + d.lng +"\" target=\"_blank\">Google Map</a>"},
	  function(d) { return '<a href=\"http://www.openstreetmap.org/?mlat=' + d.lat + '&mlon=' + d.lng +'&zoom=11'+ "\" target=\"_blank\"> OSM Map</a>"}
    ])
    .sortBy(function(d){ return d.dtg; })
    .order(d3.ascending);

/****************************
* Step6: Render the Charts  *
****************************/
			
  dc.renderAll();
  
});
