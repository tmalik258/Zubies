document.addEventListener('DOMContentLoaded', function() {
    const loaderElement = document.querySelector('.loading');
    const h1Element = document.querySelector('.carousel .text h1');
    const pElement = document.querySelector('.carousel .text p');
    const imgElement = document.querySelector('.carousel .carousel-image');
    let currentIndex = 0;
    let isInitialLoad = true;
    const preloadedImages = new Map();

    function animateText(element, text) {
        element.classList.remove('visible');
        setTimeout(() => {
            element.innerHTML = '';
            
            const words = text.split(" ");
        
            for (const word of words) {
                word.split('').forEach((letter, index) => {
                    const span = document.createElement('span');
                    span.textContent = letter;
                    span.classList.add('letter');
                    span.style.transitionDelay = `${index * 70}ms`;
                    element.appendChild(span);
                });
                element.innerHTML += "&nbsp;";
            }
        }, 700);
        setTimeout(() => {
            element.classList.add('visible');
        }, 900);
    }

    function animateImage(element, item) {
		const { img:src, h1:alt, href } = item;
        element.classList.remove('visible');
        
        // Create new image element
        const img = new Image();
        img.src = src;
        img.alt = alt;
        img.decoding = 'async';

        // Check if image is already preloaded and complete
        const preloadedImg = preloadedImages.get(src);
        const isPreloaded = preloadedImg && preloadedImg.complete;

        // Function to show the image
        const showImage = () => {
            setTimeout(() => {
                element.innerHTML = '';
                element.appendChild(img);
				if (href)
					element.setAttribute('href', href)
				else
					element.setAttribute('disabled', 'true')
                element.classList.add('visible');
            }, 500);
        };

        // If preloaded and complete, show immediately (will load from cache)
        if (isPreloaded) {
            // Image is cached, will load instantly
            img.onload = showImage;
            // If somehow already complete, show immediately
            if (img.complete) {
                showImage();
            }
        } else {
            // Wait for image to load
            img.onload = () => {
                // Cache the image for future use
                preloadedImages.set(src, img);
                showImage();
            };

            img.onerror = () => {
                console.error(`Failed to load image: ${src}`);
                // Show element even if image fails to load
                element.classList.add('visible');
            };
        }
    }

    function changeText() {
        const item = textOptions[currentIndex];
        animateText(h1Element, item.h1);
        animateText(pElement, item.p);
        animateImage(imgElement, item);

        currentIndex = (currentIndex + 1) % textOptions.length;
    }

        // Preload images in background without blocking
    function preloadImages() {
        textOptions.forEach((option, index) => {
            // Skip first image as it's already loaded
            if (index === 0) return;

            const img = new Image();
            img.src = option.img;
            img.decoding = 'async';
            img.loading = 'lazy';
            img.onload = () => {
                preloadedImages.set(option.img, img);
            };
            img.onerror = () => {
                console.error(`Failed to preload image: ${option.img}`);
            };
        });
    }

    // Start content animation immediately with first item
    function startContentAnimation() {
        // Show first content immediately
        if (isInitialLoad) {
            isInitialLoad = false;
            const firstItem = textOptions[0];

            // Function to show first content (both image and text together)
            const showFirstContent = () => {
                // Show text
                animateText(h1Element, firstItem.h1);
                animateText(pElement, firstItem.p);

                // Show image
                if (firstItem.href)
                    imgElement.setAttribute('href', firstItem.href)
                else
                    imgElement.setAttribute('disabled', 'true')
                imgElement.classList.add('visible');
            };

            // Check if image already exists in DOM (from HTML) and is loaded
            const existingImg = imgElement.querySelector('img');
            if (existingImg) {
                // Check if image is already loaded
                if (existingImg.complete && existingImg.naturalHeight !== 0) {
                    // Image is already loaded, cache it and show content immediately
                    preloadedImages.set(firstItem.img, existingImg);
                    showFirstContent();
                } else {
                    // Image is loading, wait for it then show content
                    existingImg.addEventListener('load', () => {
                        preloadedImages.set(firstItem.img, existingImg);
                        showFirstContent();
                    }, { once: true });

                    // Fallback: if image fails to load, show content anyway
                    existingImg.addEventListener('error', () => {
                        showFirstContent();
                    }, { once: true });
                }
            } else {
                // No image in DOM, create and load it
                const firstImg = new Image();
                firstImg.src = firstItem.img;
                firstImg.alt = firstItem.h1;
                firstImg.decoding = 'async';
                firstImg.loading = 'eager';
                firstImg.onload = () => {
                    preloadedImages.set(firstItem.img, firstImg);
                    imgElement.innerHTML = '';
                    imgElement.appendChild(firstImg);
                    showFirstContent();
                };
                firstImg.onerror = () => {
                    // Show content even if image fails
                    showFirstContent();
                };
            }

            currentIndex = 1;
        }

        // Change text every 5 seconds
        setInterval(changeText, 5000);

        // Preload remaining images in background
        preloadImages();
    }

    // Hide loader and start content animation
    function hideLoaderAndStartContent() {
        loaderElement.addEventListener('animationend', function() {
            startContentAnimation();
        }, { once: true });
    }

    // Check if the loader has already completed at least one animation cycle
    const loaderSVG = loaderElement.querySelector('svg');
    if (loaderSVG) {
        const animatedPath = loaderSVG.querySelector('.st0, .st2, .st4');
        if (animatedPath) {
            // Use the animationiteration event to detect when the first cycle is complete
            animatedPath.addEventListener('animationiteration', function() {
                hideLoaderAndStartContent();
            }, { once: true });
        } else {
            // Fallback in case the SVG structure is different
            hideLoaderAndStartContent();
        }
    } else {
        // Fallback in case the loader structure is different
        hideLoaderAndStartContent();
    }

	// Optimize ScrollTrigger performance
	gsap.registerPlugin(ScrollTrigger);

	// Reduce ScrollTrigger refresh rate for better performance
	ScrollTrigger.config({
		autoRefreshEvents: "visibilitychange,DOMContentLoaded,load"
	});

	const elements = document.querySelectorAll(".appear");

	// Use requestAnimationFrame to batch DOM reads/writes
	requestAnimationFrame(() => {
		elements.forEach((el) => {
			gsap.set(el, {
				clipPath: "inset(100% 100% 0 0)",
				opacity: 0,
				willChange: "clip-path, opacity"
			})

			const trigger = gsap.to(el, {
				scrollTrigger: {
					trigger: el,
					start: 'top bottom',
					end: 'bottom 80%',
					scrub: 0.5, // Reduced from true for better performance
					once: false, // Allow reverse animation
					markers: false,
					refreshPriority: -1, // Lower priority for better performance
					invalidateOnRefresh: false // Prevent unnecessary recalculations
				},
				clipPath: "inset(0% 0% 0 0)",
				opacity: 1,
				ease: "power1.out",
				onComplete: () => {
					// Remove will-change after animation for better performance
					el.style.willChange = "auto";
				}
			});

			// Clean up on unmount for better memory management
			window.addEventListener('beforeunload', () => {
				trigger.kill();
			});
		})
	})


	// Subscribe
	$('#form-subscribe').on('submit', function (e) {
		e.preventDefault();

		const submitButton = $(this).find('button[type="submit"]');
		const form = $(this);

		submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...');
		submitButton.prop('disabled', true);

		$.ajax({
			type: "POST",
			url: subscribe_url,
			data: {
				email: e.target.email.value,
				csrfmiddlewaretoken: e.target.csrfmiddlewaretoken.value,
				action: 'subscribe'
			},
			success: function (response) {
				$('#form-subscribe').html(`<h2>${response.message}</h2>`);
				$('#error-message').remove();
			},
			error: function (xhr, errmessage, err) {
				submitButton.html('Subscribe');
				submitButton.prop('disabled', false);

				let errorMessage = 'An error occurred. Please try again.';
				if (xhr.responseJSON && xhr.responseJSON.message) {
					errorMessage = xhr.responseJSON.message;
				}
				$('#form-subscribe').after(`<h2 id="error-message">${errorMessage}</h2>`);
				console.error('Error:', err);
			}
		});
	})


	// Contact Us
	$('#contact-us').on('submit', send_message);
	
	function send_message(e) {
		e.preventDefault();
		
		const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
		const contact_btn = $(this).find('button[type="submit"]');

		contact_btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...')
		contact_btn.prop('disabled', true);

		fetch(contact_url, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrf_token,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				fname: e.target.fname.value,
				lname: e.target.lname.value,
				email: e.target.email.value,
				message: e.target.message.value,
			}),
		})
		.then(response => {
			if (!response.ok) {
				// Network error
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(result => {
			if(result.message) {
				$(".form_message").text(JSON.stringify(result.message));
				// Reset form fields
				$("#contact-us")[0].reset();
			}
			else if (result.error) {
				// Handle error
				$(".form_message").text(JSON.stringify(result.error));
				contact_btn.html('Send')
				contact_btn.prop('disabled', false);
			}
			contact_btn.html('Send')
			contact_btn.prop('disabled', false);
		})
		.catch(error => {
			console.error('Error: ', error);
			$(".form_message").text("An error occurred. Please try again later.");
			contact_btn.html('Send')
			contact_btn.prop('disabled', false);
		});
	}
});

