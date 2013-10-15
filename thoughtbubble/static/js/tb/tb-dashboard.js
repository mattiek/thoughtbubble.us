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
