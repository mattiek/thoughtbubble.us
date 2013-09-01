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
    });

    map.on('draw:deleted', function(e) {
        // done after save
    });

});
//})