// Generated by CoffeeScript 1.7.1
var init, playDinoSound;

$('#login').magnificPopup({
  type: 'inline',
  midClick: true,
  callbacks: {
    beforeOpen: function() {
      if (snapper) {
        return snapper.close('left');
      }
    }
  }
});

$('#login-overlay .submit.login').click(function(e) {
  var url;
  e.preventDefault();
  $('#login-error').html('');
  url = $('#overlay-login-form').attr('action');
  return $.post(url, $('#overlay-login-form').serialize(), function(response) {
    if (response.success) {
      return window.location.reload(false);
    } else {
      $('#login-error').html('Incorrect user/password credentials.');
      if ($('html.thought-mobile')) {
        return $(window).scrollTop();
      }
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

playDinoSound = function() {
  var buffer, source;
  buffer = window.dinoSoundBuffer;
  source = window.context.createBufferSource();
  source.buffer = buffer;
  source.connect(window.context.destination);
  return source.start(0);
};

$(document).on("click", ".dislike", function(e) {
  e.preventDefault();
  return $.magnificPopup.open({
    items: {
      src: '#dislike-overlay',
      type: 'inline'
    },
    callbacks: {
      open: function() {
        return playDinoSound();
      }
    }
  });
});

$(document).on("click", "#dino_comment", function(e) {
  return $.magnificPopup.close();
});

$(document).ready(function() {
  return init();
});

init = function() {
  var e, loadDinoSound, onError;
  try {
    window.dinoSoundBuffer = null;
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    window.context = new AudioContext();
    onError = function(e) {
      return console.log(e);
    };
    loadDinoSound = function(url) {
      var request;
      request = new XMLHttpRequest();
      request.open('GET', url, true);
      request.responseType = 'arraybuffer';
      request.onload = function() {
        return window.context.decodeAudioData(request.response, function(buffer) {
          return window.dinoSoundBuffer = buffer;
        }, onError);
      };
      return request.send();
    };
    return loadDinoSound(dinoSoundURL);
  } catch (_error) {
    e = _error;
    return console.log('no sound');
  }
};

$('.image-popup-no-margins').magnificPopup({
  type: 'image',
  closeOnContentClick: true,
  closeBtnInside: false,
  fixedContentPos: true,
  mainClass: 'mfp-no-margins mfp-with-zoom',
  image: {
    verticalFit: true
  },
  zoom: {
    enabled: true,
    duration: 300
  }
});
