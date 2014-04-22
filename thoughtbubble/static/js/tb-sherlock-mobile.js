var tiles = mapbox.layer().tilejson({
    tiles: [ "http://a.tiles.mapbox.com/v3/mattiej.map-5onab1gh/{z}/{x}/{y}.png" ]
});
var spotIndex = 0;
var spots = mapbox.markers.layer()
    // Load up markers from geojson data.
    .features(geojson)
    // Define a new factory function. Takes geojson input and returns a
    // DOM element that represents the point.
    .factory(function(f) {

        var el = document.createElement('div');
        if (f.properties.id != geojson[0].properties.id) {
            el.className = 'spot spot-' + f.properties.id;
        }
        return el;

    });

// Creates the map with tile and marker layers and
// no input handlers (mouse drag, scrollwheel, etc).
var map = mapbox.map('map', [tiles, spots], null, []);

// Array of story section elements.
var communisplore = document.getElementById('communisplore-mobile')
var sections = communisplore.getElementsByTagName('li');

// Array of marker elements with order matching section elements.
var markers = _(sections).map(function(section) {
    return _(spots.markers()).find(function(m) {
        return m.data.properties.id === section.id;
    });
});

// Helper to set the active section.
var setActive = function(index, ease) {
    // Set active class on sections, markers.
//    _(sections).each(function(s) { s.className = s.className.replace(' active', '') });
    _(markers).each(function(m) { m.element.className = m.element.className.replace(' active', '') });
    $(sections).removeClass('active');
    $(sections[index]).addClass('active');
    markers[index].element.className += ' active';

    // Set a body class for the active section.
    document.body.className = 'section-' + index;

    // Ease map to active marker.
    if (!ease) {
        map.centerzoom(markers[index].location, markers[index].data.properties.zoom||14);
    } else {
        map.ease.location(markers[index].location).zoom(markers[index].data.properties.zoom||14).optimal(0.5, 1.00);
    }

    return true;
};

// Set map to first section.
setActive(0, false);

var getIntersect = function() {
    var padding = 10;
   var intersection =  $('#communisplore-mobile')[0].getBoundingClientRect().top;
    var children = _.filter($('#communisplore-mobile li'), function(el) { return (el.getBoundingClientRect().top - padding) <= intersection; });
    var last = $('#communisplore-mobile li').last()[0];
    $('#sherlock-end').css('height',(last.clientHeight - padding) /3 );
    var active = _.last(children) || $('#communisplore-mobile').children().first();
    $(active).nextAll().removeClass('active');
//    $(active).prevAll().addClass('active');

    setActive($(active).attr('data-index'),true);
}

$('#communisplore-mobile').on('scroll',  getIntersect);


$(document).ready( function() {
    var height = $('#communisplore-mobile').height();

    $('#communisplore-mobile').slimscroll({
        color: '#00f',
        size: '0px',
        width: '100%',
        height: height,
        wheelStep: 40
    });

});

