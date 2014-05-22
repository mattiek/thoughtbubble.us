if ("undefined" === typeof TB) {
    var TB = {};
}

(function($) {

    TB.Map = (function(){
        var drawn_object = [];

        var default_lat =  39.961;
        var default_lng = -82.998;

        if (region) {
            default_lat = region[1];
            default_lng = region[0];
        }

        var default_zoom = 11;
        var default_map = 'mattiej.map-5onab1gh';//'mlreed328.map-0chlhqvz';
//        var default_map = 'mattiej.map-wodu25gx';//'mlreed328.map-0chlhqvz';
        var map;
        var mapLayer = null;

        var drawn_poly;
        var polyLineOptions = {
            color   : 'red',
            weight  : 1
        };


        var init = function(){
            map = L.mapbox.map('map','', {zoomControl: false })
                .setView([default_lat, default_lng], default_zoom);


            new L.Control.Zoom({ position: 'topright' }).addTo(map);

        };

        var loadMapLayer = function() {
            TB.Map.mapLayer = L.mapbox.tileLayer(default_map);
            map.addLayer(TB.Map.mapLayer);
        }

        var get_map = function() {
            return map;
        }

        var panTo = function(coords) {
            map.panTo(coords);
        }

        return {
            "map"               : get_map,
            "drawn_object"      : drawn_object,
            "default_lat"       : default_lat,
            "default_lng"       : default_lng,
            "default_zoom"      : default_zoom,
            "default_map"       : default_map,
            "init"              : init,
            "panTo"             : panTo,
            "loadMapLayer"      : loadMapLayer,
            "mapLayer"          : mapLayer
        };

    }());


//    $(document).ready(function(){


//    });

})(jQuery);