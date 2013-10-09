$('.commenting').on('click', function(e) {

});


// Event subscribing
$(document.body).on('idea:support:count', function(e){
    var $count = e.target.parents('.idea-cap').find('.support-star');
    $count.html(e.count);
});