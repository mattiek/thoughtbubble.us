$('#login').magnificPopup
  type:'inline'
  midClick: true

$('#login-overlay .submit.login').click (e) ->
  e.preventDefault()
  $('#login-error').html ''
  url = $('#overlay-login-form').attr 'action'
  $.post url, $('#overlay-login-form').serialize(), (response) ->
      if (response.success)
        window.location = window.location;
      else
        $('#login-error').html 'Incorrect user/password credentials.'


$('#login-with-email').click (e) ->
  e.preventDefault()
  $('#login-overlay').addClass 'reveal-email'

$('.logged-out #primary-add').click (e) ->
  e.preventDefault()
  $('#login').click()


$('#join').magnificPopup
  type:'inline'
  midClick: true

$('#footer-logout').magnificPopup
  type:'inline'
  midClick: true

$('#create-an-account').magnificPopup
  type:'inline'
  midClick: true

$( document ).on "click", ".message-box", (e) ->
  $(this).remove()

$( document ).on  "click", ".logged-out .login-required", (e) ->
  e.preventDefault()
  $.magnificPopup.open
    items:
      src: '#login-overlay',
      type: 'inline'


$( document ).on "click", ".dislike", (e) ->
  e.preventDefault()
  $.magnificPopup.open
    items:
      src: '#login-overlay',
      type: 'inline'