// Generated by CoffeeScript 1.7.1
$('#login').magnificPopup({
  type: 'inline',
  midClick: true
});

$('#login-overlay .submit.login').click(function(e) {
  var url;
  e.preventDefault();
  $('#login-error').html('');
  url = $('#overlay-login-form').attr('action');
  return $.post(url, $('#overlay-login-form').serialize(), function(response) {
    if (response.success) {
      return window.location = window.location;
    } else {
      return $('#login-error').html('Incorrect user/password credentials.');
    }
  });
});

$('#login-with-email').click(function(e) {
  e.preventDefault();
  return $('#login-overlay').addClass('reveal-email');
});

$('[data-view=logged-out] #primary-add').click(function(e) {
  e.preventDefault();
  return $('#login').click();
});

$('#join').magnificPopup({
  type: 'inline',
  midClick: true
});

$('#footer-logout').magnificPopup({
  type: 'inline',
  midClick: true
});

$('#create-an-account').magnificPopup({
  type: 'inline',
  midClick: true
});

$(document).on("click", ".message-box", function(e) {
  return $(this).remove();
});

$(document).on("click", "[data-view=logged-out] .login-required", function(e) {
  e.preventDefault();
  return $.magnificPopup.open({
    items: {
      src: '#login-overlay',
      type: 'inline'
    }
  });
});

$(document).on("click", ".dislike", function(e) {
  e.preventDefault();
  return $.magnificPopup.open({
    items: {
      src: '#login-overlay',
      type: 'inline'
    }
  });
});


