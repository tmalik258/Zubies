var swiper_grid = new Swiper(".categories-grid-swiper", {
	grabCursor: true,
	slidesPerView: 3,
	centeredSlides: true,
	centeredSlidesBounds: true,
	slideToClickedSlide: true,
	autoplay: {
		delay: 2700,
        disableOnInteraction: false,
	},
	breakpoints: {
		"@0.00": {
			slidesPerView: 1,
			spaceBetween: 15,
			grid: {
				rows: 2,
			},
	  },
	  "@0.75": {
		slidesPerView: 3,
		// spaceBetween: 20,
	  },
	},
	spaceBetween: 15,
	pagination: {
		el: ".swiper-pagination",
		clickable: true,
		renderBullet: function (index, className) {
			return '<span class="' + className + '">' + "</span>";
		},
	},
	// mousewheel: true,
	keyboard: true,
});