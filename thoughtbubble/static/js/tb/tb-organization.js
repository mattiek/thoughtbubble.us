

$(function(){
    var mySwiper = $('.swiper-container').swiper({
        //Your options here:
        mode:'horizontal',
        loop: false

        //etc..
    });

    $('.right-news, .left-news').on("click", function(e){
        e.preventDefault();
        var $t = $(e.currentTarget);
        if ($t.hasClass('left-news')) {
            mySwiper.swipePrev();
            $('.right-news').addClass('has');
            if (mySwiper.activeIndex == 0) {
                $('.left-news').removeClass('has');
            }

        }
        else {
            mySwiper.swipeNext();
            $('.left-news').addClass('has');
            if (mySwiper.activeIndex == ($('.swiper-wrapper li').length - 1)) {
                $('.right-news').removeClass('has');
            }
        }
    });

    if (($('.swiper-wrapper li').length > 1)) {
        $('.right-news').addClass('has');
    }
})


