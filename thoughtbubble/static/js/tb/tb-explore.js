var map = TB.Map.map();



$(document).ready(function() {
    map.on('ready', function() {
        $.get(
            '/api/v1/locations/.json',
            function(data) {
                // Set a custom icon on each marker based on feature properties
                map.markerLayer.on('layeradd', function(e) {
                    var marker = e.layer,
                        feature = marker.feature;

                    marker.setIcon(L.icon(feature.properties.icon));
                });
                //Add features to the map
                map.markerLayer.setGeoJSON(data.results);
            }
        );

        map.markerLayer.on('click', function(e) {
            map.panTo(e.layer.getLatLng());
        })
    });


});
//})