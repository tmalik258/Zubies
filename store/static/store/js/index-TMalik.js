document.onreadystatechange = function (e) {
    if (document.readyState === 'complete') {
        if (window.innerWidth > 750)
        {
            $('#carouselExampleIndicators').height(window.innerHeight - 40);
            $('.d-block').height(window.innerHeight - 40);
        }
    }
}

window.onload = function () {
    // script.js
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

    function handleThemeChange(event) {
        if (event.matches) {
            // Switch to dark theme
            $('img.navbar-logo').attr('src', imageUrl);
            $('#logo_heading').attr('src', imageUrl);
        } else {
            // Switch to light theme
            document.body.classList.remove('dark-theme');
        }
    }

    // Check initial theme preference and apply appropriate theme
    handleThemeChange(window.matchMedia('(prefers-color-scheme: dark)'));

    // Listen for changes in the preferred color scheme
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange);


    // Add to Newsletter
    $(document).on('click', '#subcribe-btn', function (e) {
        e.preventDefault();
        $(this).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...')
        var csrfToken = "{{ csrf_token }}";
        $.ajax({
            type: "POST",
            url: "{% url 'more:subscribe' %}",
            data: {
                email: $('input[type="email"][name="email"]#newsletter1').val(),
                csrfmiddlewaretoken: csrfToken,
                action: 'subscribe'
            },
            success: function (response) {
                $('#newsletter').html(response);
            },
            error: function (xhr, errmessage, err) {
                console.log(err);
                $('#newsletter').html('Error: Try Again');
            }
        });
    })

    if (window.innerWidth > 750) {
        $('.nav-item.dropdown .nav-link').hover(function () {
                // over
                let menu = $(this).siblings('.dropdown-menu');
                menu.addClass('show');
                $(this).prop('ariaExpanded', true);
                $(this).addClass('show');
            }, function () {
                // out
                let menu = $(this).siblings('.dropdown-menu');
                menu.removeClass('show');
                $(this).prop('ariaExpanded', false);
                $(this).removeClass('show');
            }
        );
        $('.dropdown-menu').hover(function (e) {
                // over
                $(this).addClass('show');
                let nav_item = e.target.previousElementSibling;
                nav_item.firstChild.addClass('show');
                $(nav_item).children().addClass('show');
                $(nav_item).children().prop('ariaExpanded', true);
            }, function (e) {
                // out
                $(this).removeClass('show');
                let nav_item = e.target.previousElementSibling;
                $(nav_item).find('.nav-link').removeClass('show');
                $(nav_item).find('.nav-link').prop('ariaExpanded', false);
            }
        );
    }
    $('.searchBtn').on('click', () => {
        $('.searchBox').addClass('active');
        $('.search').addClass('active');
    })

    $('.searchBox input').focusout(() => {
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    })

    $('.closeBtn').click(function (e) {
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    });

    $('.menuToggle').on('click', () => {
        $('#navigation0').toggleClass('active');
        $('.searchBox').removeClass('active');
        $('.search').removeClass('active');
    })

    var swiperImages = new Swiper(".itemImageSwiper", {
		// effect: "cube",
        grabCursor: true,
        lazy: true,
        loop: true,
        zoom: true,
        spaceBetween: 10,
        // cubeEffect: {
        //     shadow: true,
        //     slideShadows: true,
        //     shadowOffset: 5,
        //     shadowScale: 0.7,
        // },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
          },
		
	  });
}

window.onscroll = function () {
    if ((window.innerHeight + window.scrollY >= window.innerHeight + 50) && (window.innerHeight + window.scrollY < document.body.offsetHeight)) {
        // $('body').css('background', 'blue');
        $('.navigation').css({visibility: 'visible', opacity: 1});
    }
    else
        $('.navigation').css({visibility: 'hidden', opacity: 0});
    // if (window.innerHeight + window.scrollY >= document.body.offsetHeight)
    // {
    //     $('.navigation').css({visibility: 'hidden', opacity: 0});
    // }
    // else
    //     $('.navigation').css({visibility: 'visible', opacity: 1});
    
}

function nav(view) {
    $('.list').each(function (indexInArray, valueOfElement) {
        $('.list').eq(indexInArray).removeClass('active');
    });
    $(view).addClass('active');
}