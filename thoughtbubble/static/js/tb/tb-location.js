var has_map = $("#map").length > 0;

if(has_map){
    TB.Map.init();
}

var map = TB.Map.map();


$(document).ready(function() {
    map.on('ready', function() {


    });




});