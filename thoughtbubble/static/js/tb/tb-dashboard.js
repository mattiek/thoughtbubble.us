$('#edit-button').on('click', function(e){
    e.preventDefault();
    $(e.target).parent().addClass('editing');
});

$('#cancel-button').on('click', function(e){
    e.preventDefault();
    $(e.target).parent().removeClass('editing');
});

$('#save-button').on('click', function(e){
    e.preventDefault();
    $('#update-info').submit();
});


$('#picture a').magnificPopup({
    type:'inline',
    midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
});