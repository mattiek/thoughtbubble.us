$('#login').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});

$('#login-overlay .submit.login').click(function(e) {
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

$('#login-with-email').click(function(e){
    e.preventDefault();
    $('#login-overlay').addClass('reveal-email');
});

$('.logged-out #primary-add').click(function(e){
    e.preventDefault();
    $('#login').click();
});


$('#join').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});

$('#footer-logout').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});

$('#create-an-account').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});

