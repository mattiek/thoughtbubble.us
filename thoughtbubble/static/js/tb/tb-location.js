var has_map = $("#map").length > 0;

if(has_map){
    TB.Map.init();
    TB.Map.loadMapLayer();
}

var map = TB.Map.map();
