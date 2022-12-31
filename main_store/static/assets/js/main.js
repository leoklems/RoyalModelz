$(document).ready(function() {
    $("#hm__menu__btn").click(function(event) {
            event.preventDefault();
            $('.hm__nav').toggleClass('hm__nav__triggered');
            $('.fa-bars').toggleClass('fa-times');
            $('.hm__menu__btn_link').toggleClass('hm__menu__btn__trig');

        })
        // $("#hm_nav_cat_outs").hover(function(event) {
    $("#hm_nav_cat_outs").click(function(event) {
        event.preventDefault();
        $('.hm_nav_cat').toggleClass('hm_nav_cat_triggered');
        // $('.fa-bars').toggleClass('fa-times');
        // $('.fa-angle-right').toggleClass('fa-angle-down');
        // if ($(this).children[0].attr('class') == '.fas fa-angle-right') {
        //     $(this.children[0]).attr('class', '.fas fa-angle-down');
        // } else {
        //     $(this.children[0]).attr('class', '.fas fa-angle-right');
        // }

        if ($('#hm_nav_cat_outs i').attr('class') == 'fas fa-arrow-right') {
            $('#hm_nav_cat_outs i').attr('class', 'fas fa-arrow-down');
        } else {
            $('#hm_nav_cat_outs i').attr('class', 'fas fa-arrow-right');
        }

    })
    $("#hm_nav_cat_items").click(function(event) {
        // event.preventDefault();
        $('.hm_nav_cat').toggleClass('hm_nav_cat_triggered');
        $('.fa-bars').toggleClass('fa-times');

    })
    $(".we-do").one('inview', function(event, visible) {
        if (visible == true) {
            $(".we-do-icon").fadeIn(4500);
        }
    });
    $("#hm__nav__contact_us").click(function(event) {
        // event.preventDefault();
        // controling the contact us menu button link
        $('.hm__nav').removeClass('hm__nav__triggered');
        $('.fa-bars').toggleClass('fa-times');

    })
    $(".hm_nav_cat").click(function(event) {
        // event.preventDefault();
        // controling the contact us menu button link
        $('.hm_nav_cat').removeClass('hm_nav_cat_triggered');
        $('.hm__nav').toggleClass('hm__nav__triggered');
        // $('.fa-arrow-right').toggleClass('fa-arrow-down');

    })
    $("#about-link").click(function(event) {
        // event.preventDefault();
        $('.menu-item').removeClass('menu-triggered');
        $('.fa-bars').toggleClass('fa-times');
        $('.menu_wrd').toggleClass('menu_wrd_trigg');

    })
    currentSlide();
    // scroller();
    // scrollSlides();

});

let slideIndex = 0;

function plusSlides(n) {

    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.left = "unset";
    }
    if (n >= slides.length) {
        slideIndex = 1;
    }
    if (n < 1) {
        slideIndex = slides.length;
    }
    slideIndex += n;
    console.log(slideIndex)
    slideIndex++;



    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    slides[slideIndex - 1].style.left = 0;
    // showSlides();

}

function currentSlide() {
    showSlides();
}

function showSlides() {
    // console.log(slideIndex)
    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;



    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    slides[slideIndex - 1].style.display = "grid";
    setTimeout(showSlides, 7000);

}

function scrollSlides() {

    // console.log(slideIndex)
    let i = 0;
    let slides = document.getElementsByClassName("mySlides");
    // for (i = 0; i < slides.length; i++) {
    //     slides[i].style.left = "unset";
    // }

    console.log(i)
    console.log(slides.length)

    function doNothing() {
        let mess = "good boy"
    }

    while (i < slides.length) {
        setTimeout(doNothing, 10000)
        let left = document.querySelector('.hm_slides_container');
        left.scrollBy(350, 0);
        i++
        console.log(i)
    }

    console.log('done')
        // slideIndex++;



    // if (slideIndex > slides.length) {
    //     slideIndex = 1;
    // }
    // slides[slideIndex - 1].style.left = 0;
    setTimeout(scrollSlides, 10000);

}

// $(function() {
//     var scroller = $('#scroller div.innerScrollArea');
//     var scrollerContent = scroller.children('ul');
//     scrollerContent.children().clone().appendTo(scrollerContent);
//     var curX = 0;
//     scrollerContent.children().each(function() {
//         var $this = $(this);
//         $this.css('left', curX);
//         curX += $this.outerWidth(true);
//     });
//     var fullW = curX / 2;
//     var viewportW = scroller.width();

//     // Scrolling speed management
//     var controller = { curSpeed: 0, fullSpeed: 2 };
//     var $controller = $(controller);
//     var tweenToNewSpeed = function(newSpeed, duration) {
//         if (duration === undefined)
//             duration = 600;
//         $controller.stop(true).animate({ curSpeed: newSpeed }, duration);
//     };

//     // Pause on hover
//     scroller.hover(function() {
//         tweenToNewSpeed(0);
//     }, function() {
//         tweenToNewSpeed(controller.fullSpeed);
//     });

//     // Scrolling management; start the automatical scrolling
//     var doScroll = function() {
//         var curX = scroller.scrollLeft();
//         var newX = curX + controller.curSpeed;
//         if (newX > fullW * 2 - viewportW)
//             newX -= fullW;
//         scroller.scrollLeft(newX);
//     };
//     setInterval(doScroll, 20);
//     tweenToNewSpeed(controller.fullSpeed);
// });

function scroller() {
    let scroller = $('#mySlides');
    let scrollerContent = scroller.children();
    let curX = 0;

    scrollerContent.children().each(function() {
        var $this = $(this);
        $this.css('left', curX);
        curX += $this.outerWidth(true);
    });


    var fullW = curX / 2;
    var viewportW = scroller.width();

    // Scrolling speed management
    var controller = { curSpeed: 0, fullSpeed: 2 };
    var $controller = $(controller);
    var tweenToNewSpeed = function(newSpeed, duration) {
        if (duration === undefined)
            duration = 600;
        $controller.stop(true).animate({ curSpeed: newSpeed }, duration);
        console.log(duration)
    };

    scroller.hover(function() {
        tweenToNewSpeed(0);
    }, function() {
        tweenToNewSpeed(controller.fullSpeed);
    });

    // Scrolling management; start the automatical scrolling
    var doScroll = function() {
        let curX = scroller.scrollLeft();
        let newX = curX + controller.curSpeed;
        if (newX > fullW * 2 - viewportW)
            newX -= fullW;
        scroller.scrollLeft(newX);
        console.log("done")
    };
    setInterval(doScroll, 20);
    tweenToNewSpeed(controller.fullSpeed);
}