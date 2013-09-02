var has_map = $("#map").length > 0;

if(has_map){
    TB.Map.init();
}

var map = TB.Map.map();

$(document).ready(function() {
    map.on('ready', function() {


    });
    var featureGroup = L.featureGroup().addTo(map);
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: featureGroup
        },
        draw: {
            polyline: false,
            polygon: false,
            rectangle: false,
            circle: false
        }
    }).addTo(map);

    map.on('draw:created', function(e) {
        if (featureGroup.getLayers().length > 0) {
            alert('Unstyled alert: Only one location allowed per feature. Remove the existing one first')
        }
        else
            featureGroup.addLayer(e.layer);
//            console.log(e.layer._latlng);
            var latlng = e.layer._latlng;
            $('#id_longitude').val(latlng.lng);
            $('#id_latitude').val(latlng.lat);
    });

    map.on('draw:deleted', function(e) {
        // done after save
    });


    // What kinds
    $('#id_what_kind_choicefield a').on('click', function(e) {
        e.preventDefault();
        $('#id_what_kind_choicefield a').each(function() {
           $(this).removeClass('selected');
        });
        $(e.currentTarget).addClass('selected');
    });

});