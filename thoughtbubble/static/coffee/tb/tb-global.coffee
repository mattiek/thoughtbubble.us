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


$('.share-fb').on('click', (e) ->
  e.preventDefault()
  fbDataShareCopy = this.getAttribute("data-share-copy")
  fbDataShareImage = this.getAttribute("data-share-image")
  fbDataShareCaption = this.getAttribute("data-share-caption")
  fbDataShareName = this.getAttribute("data-share-name")
  fbDataShareLink = this.getAttribute("data-share-link")

  if (window.location.protocol == 'https:')
    fbDataShareImage = fbDataShareImage.replace('http:','https:')

  FB.ui(
    link : fbDataShareLink
    method:"feed"
    name: fbDataShareName
    caption:  fbDataShareCaption
    description: fbDataShareCopy
    display:"popup"
    picture: fbDataShareImage
  )
)

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