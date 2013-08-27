

$('#id_captcha_choicefield img').click(function(e) {
    $('#id_captcha').val($(e.target).attr('data-choice'));
})