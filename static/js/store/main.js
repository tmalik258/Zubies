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
	$(window).scroll(function () {
		if ($(this).scrollTop() > 100) {
			$(".back-to-top").fadeIn("slow");
		} else {
			$(".back-to-top").fadeOut("slow");
		}
	});
	$(".back-to-top").click(function () {
		$("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
		return false;
	});

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
