$(document).ready(function() {
    $("#hm__menu__btn").click(function(event) {
            event.preventDefault();
            $('.hm__sidebar').toggleClass('hm__sidebar__triggered');
            $('.fa-bars').toggleClass('fa-times');
            $('.hm__menu__btn').toggleClass('hm__menu__btn__trig');
            // $('.menu_wrd').toggleClass('menu_wrd_trigg');

        })
        // $(".we-do").one('inview', function(event, visible) {
        //     if (visible == true) {
        //         $(".we-do-icon").fadeIn(4500);
        //     }
        // });
        // $("#service-link").click(function(event) {
        //     // event.preventDefault();
        //     $('.menu-item').removeClass('menu-triggered');
        //     $('.fa-align-left').toggleClass('fa-times');
        //     $('.menu_wrd').toggleClass('menu_wrd_trigg');

    // })
    // $("#about-link").click(function(event) {
    //     // event.preventDefault();
    //     $('.menu-item').removeClass('menu-triggered');
    //     $('.fa-align-left').toggleClass('fa-times');
    //     $('.menu_wrd').toggleClass('menu_wrd_trigg');

    // })

});