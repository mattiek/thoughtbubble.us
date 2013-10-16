if ("undefined" === typeof TB) {
    var TB = {};
}

(function($) {

    TB.Map = (function(){
        var drawn_object = [];

        var default_lat =  TB.exploring.lat || 39.961;
        var default_lng =  TB.exploring.lng || -82.998;
        var default_zoom = 13;
        var default_map = 'mattiej.map-5onab1gh';//'mlreed328.map-0chlhqvz';
        var map;

        var drawn_poly;
        var polyLineOptions = {
            color   : 'red',
            weight  : 1
        };


        var init = function(){
            map = L.mapbox.map('map', default_map, {zoomControl: false })
                .setView([default_lat, default_lng], default_zoom);

            new L.Control.Zoom({ position: 'topright' }).addTo(map);
            map.on('ready', function() {

            });
        };

        var edit = function(){

            map.setZoom(13);

            map.on('click', function(me) {
                // var lat = me.latlng.lat;
                // var lng = me.latlng.lng;

                drawn_object.push(me.latlng);
                if(drawn_object.length > 2){

                    if(map.hasLayer(drawn_poly)){
                        map.removeLayer(drawn_poly);
                    }
                    drawn_poly = new L.Polygon( drawn_object, polyLineOptions );
                    map.addLayer(drawn_poly);
                }

                $("#drawing").text(drawn_object);

            });
        };

        var undo = function(){

            if(drawn_object.length == 0) return;

            drawn_object.pop();
            map.removeLayer(drawn_poly);

            if(drawn_object.length > 2){
                drawn_poly = new L.Polygon( drawn_object, polyLineOptions );
                map.addLayer(drawn_poly);
            }
            $("#drawing").text(drawn_object);

        };

        var clear = function(){

            if(drawn_object.length == 0) return;

            drawn_object = [];
            map.removeLayer(drawn_poly);

            $("#drawing").text(drawn_object);

        };

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
            "edit"              : edit,
            "undo"              : undo,
            "clear"             : clear,
            "panTo"             : panTo
        };

    }());


//    $(document).ready(function(){


//    });

})(jQuery);