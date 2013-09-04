var has_map = $("#map").length > 0;
var is_drawable = has_map && $("#map").hasClass("drawable");

if(has_map){
    TB.Map.init();
    if(is_drawable){
        TB.Map.edit();
    }
}
var map = TB.Map.map();

var doit = function() {
    $.get(
        '/api/v1/locations/.json',
        function(data) {
            //Add features to the map
            map.markerLayer.setGeoJSON(data.results);
        }
    );
}

//$(document).ready(function() {
//    map.on('ready', function() {
//        setTimeout(doit, 100);
//        map.markerLayer.on('click', function(e) {
//            map.panTo(e.layer.getLatLng());
//        });
//    });
//
//
//});

$.ajax({
    url:  '/api/v1/locations/.json',
    dataType: 'json',
    success: function load(d) {
        var markers = L.mapbox.markerLayer(d.results).addTo(map);
        markers.on('click', function(e) {
            map.panTo(e.layer.getLatLng());
        });
    }
});