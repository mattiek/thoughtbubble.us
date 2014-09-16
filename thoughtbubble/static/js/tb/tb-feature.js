//var has_map = $("#map").length > 0;
//
//if(has_map){
//    TB.Map.init();
//    TB.Map.loadMapLayer();
//}

//var map = TB.Map.map();


(function($) {

    TB.Map.Draw = (function(){

        var map = TB.Map.get_map();
         TB.Map.featureGroup = L.featureGroup().addTo(map);
        var drawControl = new L.Control.Draw({
            edit: {
                featureGroup: TB.Map.featureGroup
            },
            draw: {
                polyline: false,
                polygon: false,
                rectangle: false,
                circle: false
//                marker: {
//                    icon: false
//                }
            }
        }).addTo(map);

        map.on('draw:created', function(e) {
            if (TB.Map.featureGroup.getLayers().length > 0) {
//                alert('Unstyled alert: Only one location allowed per feature. Remove the existing one first')
                while (TB.Map.featureGroup.getLayers().length > 0) {
                    var i = TB.Map.featureGroup.getLayers()[0];
                    TB.Map.featureGroup.removeLayer(i);
                }
            }
//            else
            TB.Map.featureGroup.addLayer(e.layer);
//            console.log(e.layer._latlng);
            var latlng = e.layer._latlng;
            $('#id_longitude').val(latlng.lng);
            $('#id_latitude').val(latlng.lat);
        });

        map.on('draw:deleted', function(e) {
            // done after save
        });

        return {
            "featureGroup"               : TB.Map.featureGroup
        };
    }());


})(jQuery);

$(document).ready(function() {
    // What kinds
    $('#id_what_kind_choicefield a').on('click', function(e) {
        e.preventDefault();
        $('#id_what_kind_choicefield a').each(function() {
           $(this).removeClass('selected');
        });
        var $target = $(e.currentTarget);
        $target.addClass('selected');
        $('#id_what_kind').val($target.attr('data-value'));
    });

});