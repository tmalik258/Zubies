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
				// Reset to main menu when closing
				resetMenu();
			}, 200);
		}
	});

    function resetMenu() {
        document.querySelectorAll(".sub-menu").forEach(submenu => {
            submenu.classList.remove("submenu-open");
			submenu.parentElement.querySelector('.category-link .letter:last-child').textContent = '+'
        });
        document.querySelectorAll(".main-menu > .menu-item").forEach(item => {
            item.style.display = "";
        });
    }

    document.querySelectorAll(".category-link").forEach(link => {
        link.addEventListener("click", function(e) {
			const categoryId = this.getAttribute("data-category");
            const submenu = document.querySelector(`#submenu-${categoryId}`);
			
			if (!(submenu.classList.contains("submenu-open"))) {
				e.preventDefault();
			}

			if (submenu) {
				submenu.classList.add("submenu-open");
                hideOtherMenuItems(submenu);
            }

			this.querySelector('.letter:last-child').textContent = '';
        });
    });

    document.querySelectorAll(".back-button").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            const currentSubmenu = this.closest(".sub-menu");
            const parentMenuItem = currentSubmenu.closest(".menu-item");
            const parentSubmenu = parentMenuItem.parentElement.closest(".sub-menu");

            currentSubmenu.classList.remove("submenu-open");

            if (parentSubmenu) {
                showDirectChildren(parentSubmenu);
            } else {
                resetMenu();
            }
        });
    });

    function hideOtherMenuItems(activeSubmenu) {
        const menuItems = activeSubmenu.closest('.menu-item').parentElement.children;
        Array.from(menuItems).forEach(item => {
            if (item !== activeSubmenu.closest('.menu-item')) {
                item.style.display = 'none';
            }
        });
    }

    function showDirectChildren(submenu) {
        const menuItems = submenu.querySelector('ul').children;
        Array.from(menuItems).forEach(item => {
            item.style.display = '';
        });
        submenu.classList.add("submenu-open");
    }

	document.querySelectorAll("#menu-container a").forEach((link) => {
		const text = link.textContent;

		if (text.includes(" ")) {
			const words = text.split(" ");
			let html = "";
			for (let word of words) {
				html +=
					word
						.split("")
						.map(
							(letter, index) =>
								`<span class="letter" style="--letter-index: ${index}">${letter}</span>`
						)
						.join("") + " ";
			}
			link.innerHTML = html;
		} else {
			link.innerHTML = text
				.split("")
				.map(
					(letter, index) =>
						`<span class="letter" style="--letter-index: ${index}">${letter}</span>`
				)
				.join("");
		}
	});

	// Add click event listener to all contact-us links
    document.querySelectorAll('a[href*="#contact-section"]').forEach(link => {
        link.addEventListener('click', function(e) {
			rootElement.removeAttribute("menu-open");
			rootElement.setAttribute("menu-closed", "");
			menuOpen = false;
			// Reset to main menu when closing
			resetMenu();
        });
    });
})(jQuery);

window.addEventListener("load", () => {
	const loadingElement = document.querySelector(".loading");
	const animatedElements = loadingElement.querySelectorAll(
		":is(.st0, .st2, .st4)"
	);

	// Function to check if all animations have completed their first cycle
	const checkAnimationsComplete = () => {
		return Array.from(animatedElements).every((el) => {
			const animationDuration = parseFloat(
				getComputedStyle(el).animationDuration
			);
			return (
				el.getAnimations()[0].currentTime >= animationDuration * 1000
			);
		});
	};

	// Function to add 'hide' class
	const hideLoader = () => {
		if (checkAnimationsComplete()) {
			loadingElement.classList.add("hide");
			$("body").css("overflow", "initial");
			// Check if URL contains a hash
			if (window.location.hash === '#contact-section') {
				scrollToContact();
			}
		} else {
			requestAnimationFrame(hideLoader);
		}
	};

	// Start checking for animation completion
	hideLoader();
});

function scrollToContact() {
	const contactSection = document.querySelector('#contact-us');
	if (contactSection) {
		setTimeout(() => {
			contactSection.scrollIntoView({
				behavior: 'smooth'
			});
		}, 100); // Small delay to ensure DOM is ready
	}
}

// SHOW SCROLL UP
window.addEventListener("scroll", scrollUp);

function scrollUp() {
	const scrollUpBtn = $("#scroll-up");
	$(scrollUpBtn).click(() => {
		scrollToTop();
	});
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
		const easeInOutQuad =
			progress < 0.5
				? 2 * progress * progress
				: -1 + (4 - 2 * progress) * progress; // Ease-in-out function for smoother scrolling
		window.scrollTo(0, start - start * easeInOutQuad);

		if (progress < 1) {
			requestAnimationFrame(scrollStep);
		}
	}

	requestAnimationFrame(scrollStep);
}

// Lenis Basic GSAP js setup
// if(window.innerWidth > "768") {
// 	const lenis = new Lenis();
	
// 	lenis.on("scroll", ScrollTrigger.update);
	
// 	gsap.ticker.add((time) => {
// 		lenis.raf(time * 1000);
// 	});
	
// 	gsap.ticker.lagSmoothing(0);
// }
