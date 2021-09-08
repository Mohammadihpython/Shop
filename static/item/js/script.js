// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code
    
    // hero carousel
    $('.tz-hero-area').owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        autoplay: true,
        nav: false,
        navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
        dots: true,
    });
    
    // featured product carousel
    $(".product-sync-init").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        draggable: false,
        arrows: false,
        dots: false,
        fade: true,
        asNavFor: ".product-sync-nav"
    });
    $(".product-sync-nav").slick({
        dots: false,
        arrows: false,
        infinite: true,
        prevArrow: '<button class="slick-prev"><i class="fas fa-arrow-left"></i></button>',
        nextArrow: '<button class="slick-next"><i class="fas fa-arrow-right"></i></button>',
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: ".product-sync-init",
        focusOnSelect: true,
        draggable: false
    });
    
    // zone carousel
    $('.zone-carousel').owlCarousel({
        loop: true,
        margin: 15,
        items: 5,
        autoplay: true,
        nav: true,
        navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 3
            },
            1000: {
                items: 5
            }
        }
    });
    
    // brand carousel
    $('.tz-brand-carousel').owlCarousel({
        loop: true,
        margin: 15,
        items: 4,
        autoplay: true,
        nav: true,
        navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 3
            },
            1000: {
                items: 4
            }
        }
    });
    
    // top-of-the-week carousel
    $('.top-of-the-week-carousel').owlCarousel({
        loop: true,
        margin: 0,
        items: 2,
        autoplay: true,
        nav: false,
        navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
        dots: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 1
            },
            1000: {
                items: 2
            }
        }
    });
    
    
    // Countdown
    $("[data-countdown]").each(function () {
        var $this = $(this),
            finalDate = $(this).data("countdown");
        $this.countdown(finalDate, function (event) {
            $this.html(event.strftime('<span class="cdown day">%-D <p>Days</p></span> <span class="cdown hour">%-H <p>Hours</p></span> <span class="cdown minutes">%M <p>Mins</p></span> <span class="cdown second">%S <p>Sec</p></span>'));
        });
    });
    
    $(".filter-button").click(function(){
        var value = $(this).attr('data-filter');
        
        if(value == "all")
        {
            //$('.filter').removeClass('hidden');
            $('.filter').show('1000');
        }
        else
        {
//            $('.filter[filter-item="'+value+'"]').removeClass('hidden');
//            $(".filter").not('.filter[filter-item="'+value+'"]').addClass('hidden');
            $(".filter").not('.'+value).hide();
            $('.filter').filter('.'+value).show();
            
        }
    });
    
            // bs modal problem issue fix
      
          $(".modal").on("shown.bs.modal", function (e) {
            $(".slick-slider").slick("setPosition");
          });
    
    
//    // magnificPopup image
//    $('.item-thumb').magnificPopup({
//        type: 'image',
//        gallery: {
//            enabled: true
//        },
//    });    
        
    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });

	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if

}); 
// jquery end