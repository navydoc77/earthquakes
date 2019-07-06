function createMap(eqLayers) {

    var eqMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.light",
        accessToken: API_KEY
    });

    var map = L.map("map-id", {
        center: [30.0, 0.0],
        zoom: 2,
        layers: [eqMap].concat(d3.values(eqLayers))
    });

    var baseMaps = {
        "World Map": eqMap,
    };

    var layersControl = L.control.layers(baseMaps, eqLayers, {
        collapsed: false
    }).addTo(map);
    
    // Add tool tip and pop up information to each earthquake marker.
    function addPopupInfo(feature, layer) {

        if (feature.properties && feature.properties.mag &&
            feature.properties.place && feature.properties.time) {
                layer.bindTooltip('<div align="center"><div>Description: '  + feature.properties.mag);
        }
    }


function mapWarnings() {

    // Query the DB for the geojson earthquake data.
    d3.json('/api/warnings').then((warningsData) => {
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
            var eqLayer = L.geoJSON(warningsData.features, {
                        filter: function (feature) {
                            return (i == magBins.length - 1 ?
                                    (+feature.properties.event >= magBins[i]) :
                                    (+feature.properties.senderName >= magBins[i])  &&
                                    (+feature.properties.description < magBins[i]));
                        },
                        pointToLayer: function (feature, latlng) {
                            return L.circleMarker(latlng, {
                            fillColor: colorScale(+feature.geometry),
                            color: '#000',
                            weight: 1,
                            opacity: 1,
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
        var timelineLayer = new L.Timeline(geojsonData, {
                    getInterval: function (quake) {
                        return ({
                            start: quake.properties.time,
                            end:   quake.properties.time + 86400000,
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
