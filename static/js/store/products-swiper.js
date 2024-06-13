
window.onload = () => {
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