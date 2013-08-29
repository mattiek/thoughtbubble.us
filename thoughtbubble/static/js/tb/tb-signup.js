

$('#id_captcha_choicefield img').click(function(e) {
    $('#id_captcha').val($(e.target).attr('data-choice'));
})

//$('#add-photo').fileInput();
var options = {
    resize: 10 * 1024, //resize images using a canvas element until they're under 10KB
    quality: 0.6, //JPEG compression, defaults to 0.8
    decode: true //use window.atob to base64 decode before checking size
};

$('#add-photo').imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', function(e, data) {
    var $preview = $('#add-photo').css('display', 'inline-block'),
        $img = $preview.find('img');
    if (!$img.length) {
        $img = $('<img/>').appendTo($preview);
    }

    $img.attr('src', data);
});