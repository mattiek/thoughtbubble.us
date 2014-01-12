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
    debugger

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
    debugger
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

// Set a custom icon on each marker based on feature properties
TB.Map.map().markerLayer.on('layeradd', function(e) {

    var marker = e.layer,
        feature = marker.feature;

    marker.setIcon(L.icon(feature.properties.icon));

    var popupContent;
    // Create custom popup content
    if (feature.properties.explore) {
        popupContent =  '<a class="popup" href="' + feature.properties.explore + '">' +
            '   <h3>' + feature.properties.title + '</h3>' +
            '</a>';
    } else {
        popupContent = '<h3>' + feature.properties.title + '</h3>';
    }

    // http://leafletjs.com/reference.html#popup
    marker.bindPopup(popupContent,{
        closeButton: false
    });
});

var experimentalMarkers = function(d) {
// Add features to the map
    TB.Map.map().markerLayer.setGeoJSON(d);
}

TB.Map.mapLayer.on('ready', function() {
//    $.ajax({
//        url:  '/api/v1/organizations/.json',
//        dataType: 'json',
//        success: function load(d) {
//
//            // Transform the regions to the centers
//            var dStuff = _.map(d.features, function(obj) {
//                return {
//                    id: obj.id,
//                    properties: obj.properties,
//                    type: obj.type,
//                    geometry: obj.center
//                }
//            });
//
//           var latestD = {
//                type: "FeatureCollection",
//                features: dStuff
//            }
//            experimentalMarkers(latestD);
//            getNeighborhoods();
//
//        }
//    });
    getNeighborhoods();
    TB.Map.map().on('moveend', function(e) {
        getNeighborhoods();
    })
});


var previous_layer = null;

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



var getNeighborhoods = function() {
    var center = map.getCenter();
    $.ajax({
        url: '/api/v1/cities/.json?lat=' + center.lat + '&lng=' + center.lng,
        dataType: 'json',
        success: function load(d) {
            // Transform the regions to the centers
            var cities = _.map(d, function(obj) {
                return {
                    id: obj.id,
                    properties: obj.properties,
                    type: obj.type,
                    geometry: obj.center
                }
            });
            var j = _.pluck(d, 'properties');
            j = _.pluck(j, 'orgs');

            j = _.flatten(j);

            map_features = _.union(cities,j);

            TB.Map.map().markerLayer.setGeoJSON(map_features);

            // Listen for individual marker clicks
            TB.Map.map().markerLayer.on('click',function(e) {
//                e.layer.unbindPopup();
                var feature = e.layer.feature;

                // Check to see that we are a city that would have orgs
                if (feature.properties.orgs) {
                    $('#minisplore-wrapper ul').html('');
                    _.each(feature.properties.orgs, function(e) {
                    $('#minisplore-wrapper ul').append('<li>' + e.title + '</li>');
                    });
                    $('#minisplore').fadeIn();

                    $.ajax({
                        url:  '/api/v1/organizations/.json?city=' + feature.properties.id,
                        dataType: 'json',
                        success: function load(d) {

                            if (window.organizationBoundaries) {
                                map.removeLayer(window.organizationBoundaries);
                                window.organizationBoundaries = null;
                            }

                             window.organizationBoundaries = L.geoJson(d);
                            window.organizationBoundaries.addTo(map);
                        }
                    });


                } else { // We are on an Organization
                    $('#minisplore').fadeOut();


                    $.ajax({
                        url:  '/api/v1/organizations/.json?org=' + feature.properties.id,
                        dataType: 'json',
                        success: function load(d) {

                            if (window.organizationBoundaries) {
                                map.removeLayer(window.organizationBoundaries);
                                window.organizationBoundaries = null;
                            }

                            window.organizationBoundaries = L.geoJson(d);
                            window.organizationBoundaries.addTo(map);
                        }
                    });


                }

            });

        }
    });
}


// Metro selection
$('#metrodifier').on('change', function(e) {
    window.location.href = $('[value=' + e.target.value +']', e.target).attr('data-href');
});


$('#anywhere-else').on('click', function(e){
    e.preventDefault();
    if ($('#anywhere-entry').length) {
        $('#anywhere-entry').remove();
        $('.twitter-typeahead').remove();
    }
    else {
        $('#minisplore').append('<input id="anywhere-entry" type="text" />');
        $('#anywhere-entry').typeahead(
            {
                name: 'name',
                valueKey: 'name',
                prefetch: '/api/v1/neighborhoods-typeahead/.json',
                remote: '/api/v1/neighborhoods-typeahead/.json?neighborhood=%QUERY&metro=' + window.exploringMetro
            }
        ).bind('typeahead:selected', function (obj, datum) {
                $('#id_city').val(datum.id);
            }).bind('typeahead:autocompleted', function (obj, datum) {
                $('#id_city').val(datum.id);
            });

    }


});