//$('#add-photo').fileInput();
var options = {
    resize: 10 * 1024, //resize images using a canvas element until they're under 10KB
    quality: 0.6, //JPEG compression, defaults to 0.8
    decode: true //use window.atob to base64 decode before checking size
};


var previewThumbs = function(e, data) {
    var $preview = $(e.target).css('display', 'inline-block'),
        $img = $preview.find('img');
    if (!$img.length) {
        $img = $('<div class="cloak"><img/></div>').appendTo($preview);
        $img = $('img',$img);
    }

    $img.attr('src', data);

    if ($(e.target).next().length < 1) {
        var $tar = $(e.target);

        if ($tar.attr('data-index') /* && Number($tar.attr('data-index')) < 4 */) {
            var nextIndex = Number($tar.attr('data-index')) + 1,
                prefix = $tar.attr('data-prefix');

            $tar.after('<div id="' + prefix + '-picture_' + nextIndex + '" name="' + prefix +'-picture_' + nextIndex +'" class="picture" data-index="' +nextIndex + '"></div>');

            $('#' + prefix + '-picture_' + nextIndex).imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', previewThumbs);
        }
    }
}

$('.picture').imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', previewThumbs);


$('#id_logo').imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', function(e, data) {
    var $preview = $(e.target).css('display', 'inline-block'),
        $img = $preview.find('img');
    if (!$img.length) {
        $img = $('<img/>').appendTo($preview);
    }

    $img.attr('src', data);
});