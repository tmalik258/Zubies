document.addEventListener('DOMContentLoaded', function() {
    const loaderElement = document.querySelector('.loading');
    const h1Element = document.querySelector('.carousel .text h1');
    const pElement = document.querySelector('.carousel .text p');
    const imgElement = document.querySelector('.carousel .carousel-image');
    let currentIndex = 0;

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
        
        const img = new Image();
        img.src = src;
        img.alt = alt;
        // img.decoding = 'async';
        img.loading = 'eager';

        img.onload = () => {
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

        img.onerror = () => {
            console.error(`Failed to load image: ${src}`);
            // Optionally, you can set a placeholder image here
        };
    }

    function changeText() {
        const item = textOptions[currentIndex];
        animateText(h1Element, item.h1);
        animateText(pElement, item.p);
        animateImage(imgElement, item);

        currentIndex = (currentIndex + 1) % textOptions.length;
    }

    // Function to start content animation
    function startContentAnimation() {
        // Ensure all initial images are loaded before starting the animation
        Promise.all(textOptions.map(option => {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.src = option.img;
                img.onload = resolve;
                img.onerror = reject;
            });
        })).then(() => {
            // Initial animation
            changeText();
            // Change text every 5 seconds
            setInterval(changeText, 5000);
        }).catch(error => {
            console.error('Failed to load all images:', error);
        });
    }

    // Hide loader and start content animation
    function hideLoaderAndStartContent() {
        // loaderElement.classList.add('hide');
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

	const elements = document.querySelectorAll(".appear");

	elements.forEach((el) => {
		gsap.set(el, {
			clipPath: "inset(100% 100% 0 0)",
			opacity: 0
		})

		gsap.to(el, {
			scrollTrigger: {
				trigger: el,
				start: 'top bottom',
				end: 'bottom 80%',
				scrub: true
			},
			clipPath: "inset(0% 0% 0 0)",
			opacity: 1
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

