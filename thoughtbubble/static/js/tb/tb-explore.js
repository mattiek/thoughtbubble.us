var has_map = $("#map").length > 0;
var is_drawable = has_map && $("#map").hasClass("drawable");

if(has_map){
    TB.Map.init();
    if(is_drawable){
        TB.Map.edit();
    }
}
var map = TB.Map.map();

var previous_layer = null;

function highlightFeature(e) {
    var layer = e.layer;

    layer.setStyle({
        weight: 5,
        color: '#E27B05',
        dashArray: '',
        fillOpacity: 0.5
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }

    if (previous_layer) {
        previous_layer.setStyle({
            weight: 5,
            color: '#03f',
            dashArray: '',
            fillOpacity: 0.2
        });
    }
    previous_layer = layer;
}

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

$.ajax({
    url: '/api/v1/neighborhoods/.json?city=columbus',
    dataType: 'json',
    success: function load(d) {
        var states = L.geoJson(d).addTo(map);
        states.on('click', function(e) {
            highlightFeature(e);
            map.fitBounds(e.layer._latlngs);
        });
    }
});