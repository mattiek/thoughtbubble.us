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

$('#login-overlay .submit').click(function(e) {
    e.preventDefault();
    $('#login-error').html('');
    var url = $('#overlay-login-form').attr('action');
    $.post(url, $('#overlay-login-form').serialize(),
    function(response) {
        if (response.success) {
            window.location = window.location;
        } else {
            $('#login-error').html('Incorrect user/password credentials.');
        }
    }
    )
});

$('.logged-out #primary-add').click(function(e){
    e.preventDefault();
    $('#login').click();
});
//$('#footer-logout').click(function(e){
//
//
//});

$('#footer-logout').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});