//$('#login').on('click', function(e){
//    e.preventDefault();
//    var url = $(e.target).attr('href');
//    $('#login-overlay').lightbox_me({
//        centered: true,
//        onLoad: function() {
//        }
//    });
//});

$('#login').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});
