$('#id_what_for').chosen({disable_search_threshold: 10})
$('#id_where').chosen({disable_search_threshold: 10000})
$('#id_what_kind').chosen({disable_search_threshold: 10000})

    //  Focus auto-focus fields
    $('.auto-focus:first').focus();

    //  Initialize auto-hint fields
    $('INPUT.auto-hint, TEXTAREA.auto-hint').focus(function(){
        if($(this).val() == $(this).attr('title')){
            $(this).val('');
            $(this).removeClass('auto-hint');
        }
    });

    $('INPUT.auto-hint, TEXTAREA.auto-hint').blur(function(){
        if($(this).val() == '' && $(this).attr('title') != ''){
            $(this).val($(this).attr('title'));
            $(this).addClass('auto-hint');
        }
    });

    $('INPUT.auto-hint, TEXTAREA.auto-hint').each(function(){
        if($(this).attr('title') == ''){ return; }
        if($(this).val() == ''){ $(this).val($(this).attr('title')); }
        else { $(this).removeClass('auto-hint'); }
    });


var options = {
    resize: 10 * 1024, //resize images using a canvas element until they're under 10KB
    quality: 0.6, //JPEG compression, defaults to 0.8
    decode: true //use window.atob to base64 decode before checking size
};

$('#id_pic1, #id_pic2, #id_pic3, #id_pic4').imagePreviewInput({ resize: 30 * 1024, decode: true, quality: 0.5 }).on('load', function(e, data) {
    var $preview = $(e.target).css('display', 'inline-block'),
        $img = $preview.find('img');
    if (!$img.length) {
        $img = $('<img/>').appendTo($preview);
    }

    $img.attr('src', data);
});