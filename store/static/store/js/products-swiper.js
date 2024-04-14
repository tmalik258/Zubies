var swiper_products = new Swiper(".productsSwiper", {
	// grabCursor: true,
	slidesPerView: 5,
	// centeredSlides: true,
	// centeredSlidesBounds: true,
	// slideToClickedSlide: true,
	// autoplay: {
	// 	delay: 2700,
    //     disableOnInteraction: false,
	// },
	// breakpoints: {
	// 	"@0.00": {
	// 		slidesPerView: 1,
	// 		spaceBetween: 15,
	//   },
	//   "@0.75": {
	// 	slidesPerView: 3,
	//   },
	// },
	spaceBetween: 15,
	pagination: {
		el: ".swiper-pagination",
		clickable: true,
		// renderBullet: function (index, className) {
		// 	return '<span class="' + className + '">' + "</span>";
		// },
	},
	keyboard: true,
});