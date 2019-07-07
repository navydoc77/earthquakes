
// Create a map.
function createMap(eqLayers) {

    // Create the tile layer that will be the background of the world map displaying earthquakes.
    var eqMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.light",
        accessToken: API_KEY
    });

    // Create a map using the eqMap tile layer and the earthquake layers (eqLayers).
    var map = L.map("map-id", {
        center: [25.0, 0.0],
        zoom: 2,
        layers: [eqMap].concat(d3.values(eqLayers))
    });

    // Create a baseMaps object to hold the tile layers (eqMap & tlMap).
    var baseMaps = {
        "World Map": eqMap,
    };

    // Create a layer control, passing in the baseMaps and eqLayers.
    // Add the layer control to the map.
    var layersControl = L.control.layers(baseMaps, {
        collapsed: false
    }).addTo(map);

    // Add the legend to the map.
    legend.addTo(map);
}


// Add tool tip and pop up information to each earthquake marker.
function addPopupInfo(feature, layer) {

    // If this feature has properties named 'mag', 'place' and 'time', add a Tool Tip.
    if (feature.properties && feature.properties.mag &&
        feature.properties.place && feature.properties.time) {
            layer.bindTooltip('<div align="center"><div>events: '  + feature.properties.events +
                              '</div><div>urgency: ' + feature.properties.urgency +
                              '</div><div>warning source: ' + new Date(+feature.properties.warning_source).toDateString() +
                              '</div><div>headlines</div></div>');
    }
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// This function makes the API call that returns the earthquake data that's stored in the 'earthquakes' table
// in our database. It returns this data as a geojson object.
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function mapWarnings() {

    // Query the DB for the geojson earthquake data.
    d3.json('/api/warnings').then((warningData) => {
    
        // Create a logarithmic color scale for filling the earthquake markers.
        var colorRange = ['#E5E4DA','#A11F22'],
            minMaxEQ   = d3.extent(warningData.features.map((f) => f.properties.mag)),
            range      = [0, warningData.features.length - 1];
    
        // Scale the magnitudes.
        var logScale =  d3.scaleLog().domain(minMaxEQ).range(range);
    
        // Map colors across the color range in equal intervals.
        var step        = (range[1] - range[0]) / (colorRange.length - 1),
            inversion   = d3.range(colorRange.length).map(function(d) {
                               return range[0] + d * step;
                           }),
            colorValues = inversion.map(logScale.invert);
    
        // Scale the colors.
        var colorScale  = d3.scaleLog().domain(colorValues).range(colorRange);
    
    
        // Create a legend.
        var legend  = L.control({position: 'topleft'}),
            magBins = d3.ticks(Math.floor(minMaxEQ[0]), minMaxEQ[1], Math.ceil(minMaxEQ[1] - minMaxEQ[0]));
    
        // Implement the 'onAdd()' function.
        legend.onAdd = function (map) {
    
            var div = L.DomUtil.create('div', 'info legend');
    
            for (var i = 0; i < magBins.length; i++) {
                div.innerHTML +=
                    '<i style="background: ' + colorScale(magBins[i]) + '"></i> ' +
                    magBins[i] + (magBins[i + 1] ? '&ndash;' + magBins[i + 1] + '<br>' : '+');
            }
    
            return div;
        }
    
    
        // Initialize an object used to hold the earthquake layers.
        var eqLayers = {};
    
        for (var i = 0; i < magBins.length; i++) {
    
            // Create an overlay layer of earthquake markers for quakes within a magnitude range.
            var eqLayer = L.geoJSON(warningData.features, {
                        filter: function (feature) {
                            return (i == magBins.length - 1 ?
                                    (+feature.properties.mag >= magBins[i]) :
                                    (+feature.properties.mag >= magBins[i])  &&
                                    (+feature.properties.mag < magBins[i + 1]));
                        },
                        pointToLayer: function (feature, latlng) {
                            return L.circleMarker(latlng, {
                            radius: +feature.properties.mag * 2,
                            fillColor: colorScale(+feature.properties.mag),
                            color: feature.properties.tsunami ? '#00FF00' : '#000000',
                            weight: feature.properties.tsunami ? 2 : 1,
                            fillOpacity: 0.9,
                        });
                        },
                        onEachFeature: addPopupInfo,
                    });
    
            // Create a label for the magnitude bin and add the layer to eqLayers.
            var lvlKey = magBins[i] + (magBins[i + 1] ? '-' + magBins[i + 1] : '+');
            eqLayers[lvlKey] = eqLayer;
        };
    
        // Create an overlay layer for the earthquake timeline.
        var timelineLayer = new L.Timeline(warningData, {
                    getInterval: function (quake) {
                        return ({
                            start: quake.properties.time,
                            end:   quake.properties.time + 86400000,
                                });
                    },
                    pointToLayer: function (quake, latlng) {
                        return L.circleMarker(latlng, {
                        radius: +quake.properties.mag * 2,
                        fillColor: colorScale(+quake.properties.mag),
                        color: quake.properties.tsunami ? '#00FF00' : '#000000',
                        weight: quake.properties.tsunami ? 2 : 1,
                        fillOpacity: 0.9,
                    });
                    },
                });
    
        // Pass the earthquake overlay layers, the timeline overlay layer and the
        // legend to the createMap() function.
        //
        createMap(eqLayers, timelineLayer, legend);

    }, (reason) => {
        console.log(reason);
    });
}

function init() {
    mapWarnings();
}

init();
