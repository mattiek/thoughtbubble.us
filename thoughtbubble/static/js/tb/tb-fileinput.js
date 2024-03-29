
var options = {
    resize: 10 * 1024, //resize images using a canvas element until they're under 10KB
    quality: 0.6, //JPEG compression, defaults to 0.8
    decode: true //use window.atob to base64 decode before checking size
};

$('.file-picker-input').imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', function(e, data) {
    var $preview = $(e.target).css('display', 'inline-block'),
        $img = $preview.find('img');
    if (!$img.length) {
        $img = $('<div class="cloak"><img/></div>').appendTo($preview);
        $img = $('img',$img);
    }

    $img.attr('src', data);
});