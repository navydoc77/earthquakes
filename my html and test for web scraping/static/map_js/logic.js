var myMap = L.map("map", {
    center: [37.09, -95.71],
    zoom: 4,
    layers: [outdoormap]
});

// Create a layer control containing our baseMaps
L.control.layers(baseMaps, null, {
    collapsed: false
}).addTo(myMap);

var eventLayer = new L.LayerGroup();

// If selector changes, add new events
window.addEventListener('storage', function (object) {
    eventLayer.clearLayers();

    var lat_lng = object.newValue;

    url = `/warnings/` + `${warnings}`;

    var eventMarker = [];

    d3.json(url, function (data) {
        var events = data;

        var warningMarker = L.ExtraMarkers.icon({
            icon: 'marker',
            markerColor: 'blue',
            shape: 'square',
            prefix: 'fas'
        });

        for (var i = 0; i < events.length; i++) {
            var event = events[i];

            var lat = event.Latitude;
            var lng = event.Longitude;

            eventMarker.push(new L.marker([lat, lng], { icon: warningMarker })
                .bindPopup("<h2 align='center'>Game " + parseInt(i + 1) + "</h2><hr><h3>" + event.Event + "</h3><ul><li><b>High Price:</b> $" + parseInt(event.High_price) + "</li><li><b>Low Price:</b> $" + parseInt(event.Low_price) + "</li></ul>"));

            eventLayer.addLayer(eventMarker[i]);
        }
    });

    eventLayer.addTo(myMap);

    let counter = 0;
    var start_button = true;

    d3.select("#button-1").on("click", function () {
        if (counter > 0) {
            counter--
            myMap.flyTo(eventMarker[counter]._latlng, 10);
            eventMarker[counter].openPopup();
            console.log(redMarker);
        }
    });

    d3.select("#button-2").on("click", function () {
        if (start_button) {
            myMap.flyTo(eventMarker[counter]._latlng, 10);
            eventMarker[counter].openPopup();
            start_button = false;
        }

        else if (counter < eventMarker.length) {
            counter++;
            myMap.flyTo(eventMarker[counter]._latlng, 10);
            eventMarker[counter].openPopup();
        }
    });
});

