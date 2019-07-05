
// Create a map.
function createMap(tsunamiLayer) {

    // Create the tile layer that will be the background of the world map displaying historical tsunami data.
    var tsunamiMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.light",
        accessToken: API_KEY
    });

    // Create a map using the tsunamiMap tile layer and tsunamiLayer.
    var map = L.map("map-id", {
        center: [30.0, 0.0],
        zoom: 2,
        layers: [tsunamiMap].concat(tsunamiLayer)
    });
}


// Add tool tip information to each tsunami marker.
function addPopupInfo(feature, layer) {

    // If this feature has properties named 'country', 'locale' and 'date', add a Tool Tip.
    if (feature.properties && feature.properties.country &&
        feature.properties.locale && feature.properties.date) {
            layer.bindTooltip('<div align="center"><div>Country: '  + feature.properties.country +
                              '</div><div>Locale: ' + feature.properties.locale +
                              '</div><div>Date: ' + feature.properties.date +
                              '</div></div>');
    }
}



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// This function makes the API call that returns the historical tsuname data that's stored in the 'tsunamis' table
// in our database. It returns this data as a geojson object.
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function mapHistoricalTsunamis() {

    // Query the DB for the geojson historical tsunami data.
    d3.json('/api/tsunamis-geojson').then((geojsonData) => {
    
        // Create an overlay layer of tsunami markers.
        var tsunamiLayer = L.geoJSON(geojsonData.features, {
                    filter: function (feature) {
                        return (feature.properties.validity == 'definite tsunami' &&
                                feature.properties.source == 'Earthquake' &&
                                feature.properties.year >= 1900);
                    },
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, {
                        radius: +feature.properties.intensity * 5,
                        fillColor: '#00FF00',
                        color: '#000000',
                        weight: 1,
                        fillOpacity: 0.9,
                    });
                    },
                    onEachFeature: addPopupInfo,
                });
    
        // Pass the tsunami overlay layer to the createMap() function.
        //
        createMap(tsunamiLayer);

    }, (reason) => {
        console.log(reason);
    });
}

function init() {
    mapHistoricalTsunamis();
}

init();
