document.addEventListener('DOMContentLoaded', function() {

    const h1Element = document.querySelector('.arrival .text h1');
    const pElement = document.querySelector('.arrival .text p');
    const imgElement = document.querySelector('.arrival .arrival-image');
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

    // Initial animation
    changeText();

    // Change text every 5 seconds
    setInterval(changeText, 5000);
});