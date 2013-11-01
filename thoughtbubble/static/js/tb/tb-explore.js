var has_map = $("#map").length > 0;

var neighborhoods = neighborhoods || {};

if(has_map){
    TB.Map.init();
    TB.Map.loadMapLayer();
}
var map = TB.Map.map();

var previous_layer = null;

var section_source   = $("#section-template").html();
var section_template = Handlebars.compile(section_source);

function highlightFeature(layer) {

    if (previous_layer) {
        previous_layer.setStyle({
            stroke: false,
            fill: false,
            weight: 1,
//            color: '#03f',
            color: '#03f',
            dashArray: '',
            fillOpacity: 0
        });
    }

    layer.setStyle({
        stroke: false,
        fill: true,
        weight: 3,
//        color: '#E27B05',
        color: '#444',
        dashArray: '',
        fillOpacity: 0.2
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }


    previous_layer = layer;
}


var workingMarkers = function(d) {
    TB.Map.markers = L.mapbox.markerLayer(d.results).addTo(map);
    var newMap = L.mapbox;
    // Add features to the map
    // Set a custom icon on each marker based on feature properties


    //Add features to the map
//        map.markerLayer.setGeoJSON(d);

    TB.Map.markers.eachLayer(function(marker) {

        var feature = marker.feature;

        // Create custom popup content
        var popupContent =  '<a class="popup" href="' + feature.properties.link + '">' +
            '   <h3>' + feature.properties.title + '</h3>' +
            '</a>';

        // http://leafletjs.com/reference.html#popup
        marker.bindPopup(popupContent,{
            closeButton: false
//                minWidth: 320
        });
    });

    getNeighborhoods();
}

var experimentalMarkers = function(d) {
    // Set a custom icon on each marker based on feature properties
    TB.Map.map().markerLayer.on('layeradd', function(e) {
        var marker = e.layer,
            feature = marker.feature;

        marker.setIcon(L.icon(feature.properties.icon));
        // Create custom popup content
        var popupContent =  '<a class="popup" href="' + feature.properties.explore + '">' +
            '   <h3>' + feature.properties.title + '</h3>' +
            '</a>';

        // http://leafletjs.com/reference.html#popup
        marker.bindPopup(popupContent,{
            closeButton: false
//                minWidth: 320
        });
    });

// Add features to the map
    TB.Map.map().markerLayer.setGeoJSON(d);
}

TB.Map.mapLayer.on('ready', function() {
    $.ajax({
        url:  '/api/v1/communities/.json',
        dataType: 'json',
        success: function load(d) {

            // Transform the regions to the centers
            var dStuff = _.map(d.features, function(obj) {
                return {
                    id: obj.id,
                    properties: obj.properties,
                    type: obj.type,
                    geometry: obj.center
                }
            });

           var latestD = {
                type: "FeatureCollection",
                features: dStuff
            }
            experimentalMarkers(latestD);

        }
    });
});



var getNeighborhoods = function() {
    $.ajax({
        url: '/api/v1/neighborhoods/.json?metro=columbus',
        dataType: 'json',
        success: function load(d) {

            var geoJSON = TB.Map.markers.getGeoJSON();

            geoJSON = _.union(geoJSON, d);
            TB.Map.markers.setGeoJSON(geoJSON);

        }
    });
}


// Metro selection
$('#metrodifier').on('change', function(e) {
    window.location.href = $('[value=' + e.target.value +']', e.target).attr('data-href');
});


$('#anywhere-else').on('click', function(e){
    e.preventDefault();
    if ($('#anywhere-entry').length)
        $('#anywhere-entry').remove();
    else {
        $('#minisplore').append('<input id="anywhere-entry" type="text" />');
        $('#anywhere-entry').typeahead(
            {
                name: 'name',
                valueKey: 'name',
                prefetch: '/api/v1/cities-typeahead/.json',
                remote: '/api/v1/cities-typeahead/.json?city=%QUERY'
            }
        ).bind('typeahead:selected', function (obj, datum) {
                $('#id_city').val(datum.id);
            }).bind('typeahead:autocompleted', function (obj, datum) {
                $('#id_city').val(datum.id);
            });

    }


});


// load init
// Metro selection
//if (TB.exploring.city && TB.exploring.state) {
////    $.ajax(
////        {
////            url: '/api/v1/cities/.json?city=' + TB.exploring.city + '&state=' + TB.exploring.state,
////            dataType: 'json',
////            success: function goto(d) {
////                console.log(d);
////                var city = d.results[0];
////                map.panTo([city.latitude, city.longitude]);
////            }
////        });
//};