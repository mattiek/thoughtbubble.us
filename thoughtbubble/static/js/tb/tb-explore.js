var has_map = $("#map").length > 0;
var is_drawable = has_map && $("#map").hasClass("drawable");

var neighborhoods = neighborhoods || {};

if(has_map){
    TB.Map.init();
    if(is_drawable){
        TB.Map.edit();
    }
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

$.ajax({
    url:  '/api/v1/locations/.json',
    dataType: 'json',
    success: function load(d) {
        var markers = L.mapbox.markerLayer(d.results).addTo(map);
        // Add features to the map
        markers.eachLayer(function(marker) {

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
               neighborhoods[feature.id] = {layer: layer,
                                            feature: feature};
        }
        }).addTo(map);

        hoods.eachLayer(function(e) {
            var marker = e;
//            var feature = marker.feature;
//            marker.setIcon(L.icon(feature.properties.icon));
        });
    }
});

//$('#minisplore-wrapper').baron();


var minmin = function(id, cid, href, communityName) {

    var layer = neighborhoods[id].layer,
        feature = neighborhoods[id].feature;

    highlightFeature(layer);
    //    map.fitBounds(layer);
    map.setView([feature.center.coordinates[1],feature.center.coordinates[0]] , 16);

    // Rewrite idea create link
//    var $i = $('#idea-nav');
//    $i.attr('href', $i.attr('data-href') + '/' + id);

    // Get to Explore 2
    // TODO: Animate this

    $('#minisplore').hide();

    var context = {
        name: communityName,
        link: href,
        longitude: feature.center.coordinates[0],
        latitude: feature.center.coordinates[1]
    }
    var html    = section_template(context);

    $section = $(html).addClass('header active');

    $('#communisplore').empty().append($section).show();

    $.ajax(
        {
            url: '/api/v1/locations/.json?community=' + id,
            dataType: 'json',
            success: function(data) {
                for (x in data.results) {
                    var loc = data.results[x];

                    var context = {
                                    name: loc.name,
                                    link: loc.properties.link,
                                    longitude: loc.geometry.coordinates[0],
                                    latitude: loc.geometry.coordinates[1],
                                    description: loc.properties.about
                    }
                    var html    = section_template(context);

                    $('#communisplore').append($(html));
                }
                $v = $('<div/>').addClass('ending');
                $('#communisplore').append($v);
                setScrollExplore();
                map.dragging.disable();
                map.touchZoom.disable();
                map.doubleClickZoom.disable();
                map.scrollWheelZoom.disable();
            }
        }
    );
}

$('#minisplore a.community').on('click', function(e){
    e.preventDefault();

    var id = $(e.target).attr('data-id'),
        cid = $(e.target).attr('data-community');
    minmin(
        id,
        cid,
        $(e.target).attr('href'),
        $(e.target).text()
    );
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



var setScrollExplore = function() {
    // Array of story section elements.
    var sections = document.getElementsByTagName('section');

    // Helper to set the active section.
    var setActive = function(index, ease) {
        _(sections).each(function(s) { s.className = s.className.replace(' active', '') });
        sections[index].className += ' active';
        $section = $(sections[index]);
        //map.panTo([$section.attr('data-latitude'), $section.attr('data-longitude')]);
        map.setView([$section.attr('data-latitude'), $section.attr('data-longitude')],14);
        return true;
    };

    // Bind to scroll events to find the active section.
    $('#communisplore').on( "scroll",function(e) {
//        _(function() {
        // IE 8
        if (window.pageYOffset === undefined) {
            var y = document.documentElement.scrollTop;
            var h = document.documentElement.clientHeight;
        } else {
            var y = window.pageYOffset;
            var h = window.innerHeight;
        }

        var y = $(e.target).scrollTop(),
            h = $(e.target).height();


        // If scrolled to the very top of the page set the first section active.
        if (y === 0) return setActive(0, true);

        // Otherwise, conditionally determine the extent to which page must be
        // scrolled for each section. The first section that matches the current
        // scroll position wins and exits the loop early.
        var memo = 0;
        var buffer = (h * 0.3333);
        var active = _(sections).any(function(el, index) {
            memo += el.offsetHeight;
            return y < (memo-buffer) ? setActive(index, true) : false;
        });

        // If no section was set active the user has scrolled past the last section.
        // Set the last section active.
        if (!active) setActive(sections.length - 1, true);
//    }).debounce(10);
    });
}


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