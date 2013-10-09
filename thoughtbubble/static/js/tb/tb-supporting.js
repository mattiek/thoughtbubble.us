$(document).ready(function(){
$('a.supporting').on('click', function(e){
    e.preventDefault();
    $target = $(e.target);
    while (!$target.attr('href'))
     $target = $target.parent();

    $.ajax({
        url: $target.attr('href'),
        success: function(data) {
            if (data.status == 'removed') {
                $target.removeClass('activated');
                $(document.body).trigger({type: 'support:count', target: $target, count: data.count});
//                $('.support-number').html(data.count);
            } else if (data.status == 'added') {
                $target.addClass('activated');
//                $('.support-number').html(data.count);
                $(document.body).trigger({type: 'support:count', target: $target, count: data.count});
            } else {

            }
        }
    })
});
});