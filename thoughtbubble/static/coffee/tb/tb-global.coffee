$('#login').magnificPopup
  type:'inline'
  midClick: true

$('#login-overlay .submit.login').click (e) ->
  e.preventDefault()
  $('#login-error').html ''
  url = $('#overlay-login-form').attr 'action'
  $.post url, $('#overlay-login-form').serialize(), (response) ->
      if (response.success)
        window.location.reload( false );
      else
        $('#login-error').html 'Incorrect user/password credentials.'


$('#login-with-email').click (e) ->
  e.preventDefault()
  $('#login-overlay').addClass 'reveal-email'

$('[data-view=logged-out] #primary-add').click (e) ->
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

$( document ).on  "click", "[data-view=logged-out] .login-required", (e) ->
  e.preventDefault()
  $.magnificPopup.open
    items:
      src: '#login-overlay',
      type: 'inline'

playDinoSound  = ->
  buffer = window.dinoSoundBuffer
  source = window.context.createBufferSource()
  source.buffer = buffer
  source.connect(window.context.destination)
  source.start(0)

$( document ).on "click", ".dislike", (e) ->
  e.preventDefault()
  $.magnificPopup.open
    items:
      src: '#dislike-overlay',
      type: 'inline'
    callbacks:
      open: () ->
        playDinoSound()


$(document).on("click", "#dino_comment", (e) ->
  $.magnificPopup.close()
)

#window.addEventListener('load', init, false)

$(document).ready ->
  init()

init = ->
  try
    window.dinoSoundBuffer = null;

#    // Fix up prefixing
    window.AudioContext = window.AudioContext || window.webkitAudioContext
    window.context = new AudioContext()

    onError = (e) ->
      console.log(e)

    loadDinoSound = (url) ->
      request = new XMLHttpRequest()
      request.open('GET', url, true)
      request.responseType = 'arraybuffer'

#      // Decode asynchronously
      request.onload = () ->
        window.context.decodeAudioData(request.response, (buffer) ->
          window.dinoSoundBuffer = buffer
        , onError)
      request.send()
    loadDinoSound(dinoSoundURL)

  catch e
    console.log 'no sound'


#$('.share-fb').on('click', (e) ->
#  e.preventDefault()
#  fbDataShareCopy = this.getAttribute("data-share-copy")
#  fbDataShareImage = this.getAttribute("data-share-image")
#  fbDataShareCaption = this.getAttribute("data-share-caption")
#  fbDataShareName = this.getAttribute("data-share-name")
#  fbDataShareLink = this.getAttribute("data-share-link")
#
#  if (window.location.protocol == 'https:')
#    fbDataShareImage = fbDataShareImage.replace('http:','https:')
#
#  FB.ui(
#    link : fbDataShareLink
#    method:"feed"
#    name: fbDataShareName
#    caption:  fbDataShareCaption
#    description: fbDataShareCopy
#    display:"popup"
#    picture: fbDataShareImage
#  )
#)

$('.image-popup-no-margins').magnificPopup(
  type: 'image'
  closeOnContentClick: true
  closeBtnInside: false
  fixedContentPos: true
  mainClass: 'mfp-no-margins mfp-with-zoom'
  image:
    verticalFit: true
  zoom:
    enabled: true
    duration: 300
)


#getCookie = (name)->
#  cookieValue = null
#  if document.cookie && document.cookie != ''
#    cookies = document.cookie.split(';')
#    for i in cookies
#      cookie = jQuery.trim(i)
##    // Does this cookie string begin with the name we want?
#      if (cookie.substring(0, name.length + 1) == (name + '='))
#        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
#        break;
#  cookieValue
#
#csrfSafeMethod = (method)->
##// these HTTP methods do not require CSRF protection
#  (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
#
#sameOrigin = (url)->
#  #// test that a given url is a same-origin URL
#  #// url could be relative or scheme relative or absolute
# host = document.location.host; #// host + port
# protocol = document.location.protocol;
# sr_origin = '//' + host;
# origin = protocol + sr_origin;
#  #// Allow absolute or scheme relative URLs to same origin
# (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url))
## or any other URL that isn't scheme relative or absolute i.e relative.
#
#
#$.ajaxSetup(
#  beforeSend: (xhr, settings) ->
#    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url))
##      // Send the token to same-origin, relative URLs only.
##      // Send the token only if the method warrants CSRF protection
##      // Using the CSRFToken value acquired earlier
#      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
#);