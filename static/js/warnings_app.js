function createMap(eqLayers, timelineLayer, legend) {

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

    // Add tool tip and pop up information to each earthquake marker.
    function addPopupInfo(feature, layer) {

        if (feature.properties && feature.properties.mag &&
            feature.properties.place && feature.properties.time) {
                layer.bindTooltip('<div align="center"><div>Description: '  + feature.properties.mag);
        }
    }

    function mapWarnings() {

        d3.json('/api/warnings').then((warningsData) => {
        
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
}