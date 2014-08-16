if ("undefined" === typeof TB) {
    var TB = {};
}

(function($) {

    TB.Map = (function(){
        var self = {}
        self.drawn_object = [];

        self.default_lat =  39.961;
        self.default_lng = -82.998;

        try {
            self.default_lat = region[1];
            self.default_lng = region[0];
        }
        catch (e) {

        }

        self.default_zoom = 11;
        self.default_map = 'mattiej.map-5onab1gh';//'mlreed328.map-0chlhqvz';
        self.map;
        self.featureLayer = null;
        self.mapLayer = null;

        var drawn_poly;
        var polyLineOptions = {
            color   : 'red',
            weight  : 1
        };


        self.init = function(){
            L.mapbox.accessToken = 'pk.eyJ1IjoibWF0dGllaiIsImEiOiJiaFJBdENBIn0.a3wsqqaNNEbR1_cq1SSZNA';
            self.map = L.mapbox.map('map','', {
                zoomControl: false
            })
                .setView([self.default_lat, self.default_lng], self.default_zoom);


            self.featureLayer = L.mapbox.featureLayer().addTo(self.map);
            self.mapLayer = L.mapbox.tileLayer(self.default_map);
            self.map.addLayer(self.mapLayer);
            new L.Control.Zoom({ position: 'topright' }).addTo(self.map);

        };

        self.get_map = function() {
            return self.map;
        }

        self.panTo = function(coords) {
            self.map.panTo(coords);
        }

        return self;
    }());


//    $(document).ready(function(){


//    });

})(jQuery);
var has_map = $("#map").length > 0;
if(has_map){
    TB.Map.init();
    //TB.Map.loadMapLayer();
}