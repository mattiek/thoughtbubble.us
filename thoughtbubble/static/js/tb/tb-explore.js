var has_map = $("#map").length > 0;
var is_drawable = has_map && $("#map").hasClass("drawable");

var neighborhoods = neighborhoods || {};

//var reg_icon =  L.icon({
//    "iconUrl": "/static/images/map-point.png",
//    "iconSize": [26, 33], // size of the icon
//    "iconAnchor": [13, 30], // point of the icon which will correspond to marker's location
//    "popupAnchor": [0, -25]  // point from which the popup should open relative to the iconAnchor
//    });
//


if(has_map){
    TB.Map.init();
    if(is_drawable){
        TB.Map.edit();
    }
}
var map = TB.Map.map();

var previous_layer = null;

function highlightFeature(layer) {

    if (previous_layer) {
        previous_layer.setStyle({
            stroke: false,
            fill: false,
            weight: 1,
            color: '#03f',
            dashArray: '',
            fillOpacity: 0
        });
    }

    layer.setStyle({
        stroke: true,
        fill: true,
        weight: 5,
        color: '#E27B05',
        dashArray: '',
        fillOpacity: 0.5
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
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
    url: '/api/v1/neighborhoods/.json?metro=columbus',
    dataType: 'json',
    success: function load(d) {

        // Set a custom icon on each marker based on feature properties
//        map.markerLayer.on('layeradd', function(e) {
//            var marker = e.layer,
//                feature = marker.feature;
//
//            marker.setIcon(L.icon(feature.properties.icon));
//        });

        var hoods = L.geoJson(d,{
            style: function (feature) {
                return {stroke: false, fill: false};
            },
            onEachFeature: function (feature, layer) {
               neighborhoods[feature.id] = layer;
        }
        }).addTo(map);

        var geoJson = [{
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-75.00, 40]
            },
            "properties": {
                "title": "Small kitten",
                "icon": {
                    "iconUrl": "http://placekitten.com/50/50",
                    "iconSize": [50, 50], // size of the icon
                    "iconAnchor": [25, 25], // point of the icon which will correspond to marker's location
                    "popupAnchor": [0, -25]  // point from which the popup should open relative to the iconAnchor
                }
            }
        }, {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-74.00, 40]
            },
            "properties": {
                "title": "Big kitten",
                "icon": {
                    "iconUrl": "http://placekitten.com/100/100",
                    "iconSize": [100, 100],
                    "iconAnchor": [50, 50],
                    "popupAnchor": [0, -55]
                }
            }
        }];

//        map.markerLayer.setGeoJSON(d.features);
//        hoods.on('click', function(e) {
////            console.log(e.layer.id);
//            highlightFeature(e);
//            map.fitBounds(e.layer._latlngs);
//        });
    }
});

$('#minisplore-wrapper').baron();

$('#minisplore a').on('click', function(e){
    e.preventDefault();
    var id = $(e.target).attr('data-id');
    var layer = neighborhoods[id];
    highlightFeature(layer);
    map.fitBounds(layer);

    // Rewrite idea create link
    var $i = $('#idea-nav');
    $i.attr('href', $i.attr('data-href') + '/' + id);

});


// Metro selection
$('#metrodifier').on('change', function(e) {
    $.ajax(
        {
            url: '/api/v1/cities/.json?city=' + e.target.value + '&state=oh',
            dataType: 'json',
            success: function goto(d) {
                console.log(d);
                var city = d.results[0];
                map.panTo([city.latitude, city.longitude]);
            }
        });
});
