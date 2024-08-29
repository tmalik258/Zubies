(function ($) {
	"use strict";

	// Dropdown on mouse hover
	$(document).ready(function () {
		function toggleNavbarMethod() {
			if ($(window).width() > 992) {
				$(".navbar .dropdown")
					.on("mouseover", function () {
						$(".dropdown-toggle", this).trigger("click");
					})
					.on("mouseout", function () {
						$(".dropdown-toggle", this).trigger("click").blur();
					});
			} else {
				$(".navbar .dropdown").off("mouseover").off("mouseout");
			}
		}
		toggleNavbarMethod();
		$(window).resize(toggleNavbarMethod);
	});

	// Back to top button
	$(".back-to-top").fadeOut("slow");
	// $(window).scroll(function () {
	// 	if ($(this).scrollTop() > 100) {
	// 		$(".back-to-top").fadeIn("slow");
	// 	} else {
	// 		$(".back-to-top").fadeOut("slow");
	// 	}
	// });
	// $(".back-to-top").click(function () {
	// 	$("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
	// 	// $(".back-to-top").fadeOut("slow");
	// 	return false;
	// });

	// Menu Button
	const menuButton = document.querySelector("#menu-button");
	const rootElement = document.documentElement;
	let menuOpen = false;

	menuButton.addEventListener("click", () => {
		if (!menuOpen) {
			if (rootElement.hasAttribute("menu-closed"))
				rootElement.removeAttribute("menu-closed");
			rootElement.setAttribute("menu-open", "");
			menuOpen = true;
		} else {
			// Play reverse animations before removing the attribute
			setTimeout(() => {
				rootElement.removeAttribute("menu-open");
				rootElement.setAttribute("menu-closed", "");
				menuOpen = false;
			}, 200); // Delay matches the longest reverse animation duration (1s)
		}
	});

	document.querySelectorAll("#menu-container a").forEach((link) => {
		const text = link.textContent;
		if (text.includes(" ")) {
			const words = text.split(" ");
			let html = "";
			for (let word of words) {
				html += word.split("").map((letter, index) => `<span class="letter" style="--letter-index: ${index}">${letter}</span>`).join("") + " ";
			}
			link.innerHTML = html;
		}
		else {
			link.innerHTML = text
				.split("")
				.map(
					(letter, index) =>
						`<span class="letter" style="--letter-index: ${index}">${letter}</span>`
				)
				.join("");
		}
	});
})(jQuery);

window.addEventListener('load', () => {
    const loadingElement = document.querySelector('.loading');
    const animatedElements = loadingElement.querySelectorAll(':is(.st0, .st2, .st4)');

    // Function to check if all animations have completed their first cycle
    const checkAnimationsComplete = () => {
        return Array.from(animatedElements).every(el => {
            const animationDuration = parseFloat(getComputedStyle(el).animationDuration);
            return el.getAnimations()[0].currentTime >= animationDuration * 1000;
        });
    };

    // Function to add 'hide' class
    const hideLoader = () => {
        if (checkAnimationsComplete()) {
            loadingElement.classList.add('hide');
			$('body').css('overflow', 'initial');
        } else {
            requestAnimationFrame(hideLoader);
        }
    };

    // Start checking for animation completion
    hideLoader();
});

// SHOW SCROLL UP
window.addEventListener("scroll", scrollUp);

function scrollUp() {
	const scrollUpBtn = $("#scroll-up");
	$(scrollUpBtn).click(() => {scrollToTop()});
	if (this.scrollY >= 350) {
		$(scrollUpBtn).fadeIn("slow");
	} else $(scrollUpBtn).fadeOut("slow");
}

function scrollToTop() {
	const scrollDuration = 300; // Set the total scroll duration (in milliseconds)
	const start = window.scrollY;
	const startTime = performance.now();

	function scrollStep(timestamp) {
		const currentTime = timestamp - startTime;
		const progress = Math.min(currentTime / scrollDuration, 1); // Calculate progress (0 to 1)
		const easeInOutQuad = progress < 0.5 
			? 2 * progress * progress 
			: -1 + (4 - 2 * progress) * progress; // Ease-in-out function for smoother scrolling
		window.scrollTo(0, start - (start * easeInOutQuad));

		if (progress < 1) {
			requestAnimationFrame(scrollStep);
		}
	}

	requestAnimationFrame(scrollStep);
}