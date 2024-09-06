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
                    span.style.transitionDelay = `${index * 50}ms`;
                    element.appendChild(span);
                });
                element.innerHTML += "&nbsp;";
            }
        }, 500);
        setTimeout(() => {
            element.classList.add('visible');
        }, 700);
    }

    function animateImage(element, src, alt) {
        element.classList.remove('visible');
        
        setTimeout(() => {
            element.innerHTML = '';
            const img = document.createElement('img');
            img.src = src;
            img.alt = alt;
            img.decoding = 'async';
            img.loading = 'eager';
            element.appendChild(img);
            element.classList.add('visible');
        }, 500);
    }

    function changeText() {
        const newText = textOptions[currentIndex];
        animateText(h1Element, newText.h1);
        animateText(pElement, newText.p);
        animateImage(imgElement, newText.img, newText.h1);

        currentIndex = (currentIndex + 1) % textOptions.length;
    }

    // Function to start content animation
    function startContentAnimation() {
        // Initial animation
        changeText();

        // Change text every 5 seconds
        setInterval(changeText, 5000);
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

	// Contact Us
	$('#contact-us').on('submit', send_message)

	function send_message(e) {
		e.preventDefault();
	
		const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
	
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
				// Handle Success
				$(".form_message").text(JSON.stringify(result.message));
			}
			else if (result.error) {
				// Handle error
				$(".form_message").text(JSON.stringify(result.error));
			}
		})
		.catch(error => {
			console.error('Error: ', error);
			$(".form_message").text("An error occurred. Please try again later.");
		});
	}
});

